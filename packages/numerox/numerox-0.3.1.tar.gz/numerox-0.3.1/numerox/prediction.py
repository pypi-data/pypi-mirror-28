import sys

import pandas as pd
import numpy as np

from numerox.metrics import metrics_per_era
from numerox.metrics import metrics_per_name
from numerox.metrics import pearsonr
from numerox.metrics import ks_2samp
from numerox.metrics import concordance

if sys.version_info[0] == 2:
    base_string = basestring
else:
    base_string = str

HDF_PREDICTION_KEY = 'numerox_prediction'


class Prediction(object):

    def __init__(self, df=None):
        self.df = df

    @property
    def names(self):
        "List (copy) of names in prediction object"
        if self.df is None:
            return []
        return self.df.columns.tolist()

    def rename(self, mapper):
        """
        Rename prediction name(s).

        Parameters
        ----------
        mapper : {dict-like, str}
            You can rename using a dictionary with old name as key, new as
            value. Or, if the prediction contains a single name, then `mapper`
            can be a string containing the new name.

        Returns
        -------
        renamed : Prediction
            A copy of the prediction with renames names.
        """
        if isinstance(mapper, base_string):
            if self.shape[1] != 1:
                raise ValueError("prediction must contain a single name")
            mapper = {self.names[0]: mapper}
        df = self.df.rename(columns=mapper, copy=True)
        return Prediction(df)

    def drop(self, name):
        "Drop name (str) or names (e.g. a list of names) from prediction"
        df = self.df.drop(columns=name)
        return Prediction(df)

    @property
    def ids(self):
        "View of ids as a numpy str array"
        return self.df.index.values

    @property
    def y(self):
        "View of y as a 2d numpy float array"
        return self.df.values

    def ynew(self, y_array):
        "Copy of prediction but with prediction.y=`y_array`"
        if y_array.shape != self.shape:
            msg = "`y_array` must have the same shape as prediction"
            raise ValueError(msg)
        df = pd.DataFrame(data=y_array,
                          index=self.df.index.copy(deep=True),
                          columns=self.df.columns.copy())
        return Prediction(df)

    def iter(self):
        "Yield a prediction object with only one model at a time"
        for name in self.names:
            yield self[name]

    def merge_arrays(self, ids, y, name):
        "Merge numpy arrays `ids` and `y` with name `name`"
        df = pd.DataFrame(data={name: y}, index=ids)
        prediction = Prediction(df)
        return self.merge(prediction)

    def merge(self, prediction):
        "Merge prediction"
        if prediction.df.shape[1] != 1:
            raise NotImplementedError("TODO: handle more than one model")
        name = prediction.names[0]
        if self.df is None:
            # empty prediction
            df = prediction.df
        elif name not in self:
            # inserting predictions from a model not already in report
            df = pd.merge(self.df, prediction.df, how='outer',
                          left_index=True, right_index=True)
        else:
            # add more ys from a model whose name already exists
            y = self.df[name]
            y = y.dropna()
            s = prediction.df.iloc[:, 0]
            s = s.dropna()
            s = pd.concat([s, y], join='outer', ignore_index=False,
                          verify_integrity=True)
            df = s.to_frame(name)
            df = pd.merge(self.df, df, how='outer', on=name,
                          left_index=True, right_index=True)
        return Prediction(df)

    def save(self, path_or_buf, compress=True):
        "Save prediction as an hdf archive; raises if nothing to save"
        if self.df is None:
            raise ValueError("Prediction object is empty; nothing to save")
        if compress:
            self.df.to_hdf(path_or_buf, HDF_PREDICTION_KEY,
                           complib='zlib', complevel=4)
        else:
            self.df.to_hdf(path_or_buf, HDF_PREDICTION_KEY)

    def to_csv(self, path_or_buf=None, decimals=6, verbose=False):
        "Save a csv file of predictions; predictin must contain only one name"
        if self.shape[1] != 1:
            raise ValueError("prediction must contain a single name")
        df = self.df.iloc[:, 0].to_frame('probability')
        df.index.rename('id', inplace=True)
        float_format = "%.{}f".format(decimals)
        df.to_csv(path_or_buf, float_format=float_format)
        if verbose:
            print("Save {}".format(path_or_buf))

    def summary(self, data):
        df = self.summary_df(data)
        df = df.round(decimals={'logloss': 6, 'auc': 4, 'acc': 4, 'ystd': 4})
        with pd.option_context('display.colheader_justify', 'left'):
            print(df.to_string(index=True))

    def summary_df(self, data):

        if self.shape[1] != 1:
            raise ValueError("prediction must contain a single name")

        # metrics
        metrics, regions = metrics_per_era(data, self, region_as_str=True)
        metrics = metrics.drop(['era', 'name'], axis=1)

        # additional metrics
        region_str = ', '.join(regions)
        nera = metrics.shape[0]
        logloss = metrics['logloss']
        consis = (logloss < np.log(2)).mean()
        sharpe = (np.log(2) - logloss).mean() / logloss.std()

        # summary of metrics
        m1 = metrics.mean(axis=0).tolist() + ['region', region_str]
        m2 = metrics.std(axis=0).tolist() + ['eras', nera]
        m3 = metrics.min(axis=0).tolist() + ['sharpe', sharpe]
        m4 = metrics.max(axis=0).tolist() + ['consis', consis]
        data = [m1, m2, m3, m4]

        # make dataframe
        columns = metrics.columns.tolist() + ['stats', '']
        df = pd.DataFrame(data=data,
                          index=['mean', 'std', 'min', 'max'],
                          columns=columns)

        return df

    def metrics_per_era(self, data, metrics=['logloss', 'auc', 'acc', 'ystd'],
                        era_as_str=True):
        "DataFrame containing given metrics versus era (as index)"
        metrics, regions = metrics_per_era(data, self, columns=metrics,
                                           era_as_str=era_as_str)
        metrics.index = metrics['era']
        metrics = metrics.drop(['era'], axis=1)
        return metrics

    def performance(self, data, sort_by='logloss'):
        df, info = self.performance_df(data)
        if sort_by == 'logloss':
            df = df.sort_values(by='logloss', ascending=True)
        elif sort_by == 'auc':
            df = df.sort_values(by='auc', ascending=False)
        elif sort_by == 'acc':
            df = df.sort_values(by='acc', ascending=False)
        elif sort_by == 'ystd':
            df = df.sort_values(by='ystd', ascending=False)
        elif sort_by == 'sharpe':
            df = df.sort_values(by='sharpe', ascending=False)
        elif sort_by == 'consis':
            df = df.sort_values(by=['consis', 'logloss'],
                                ascending=[False, True])
        else:
            raise ValueError("`sort_by` name not recognized")
        df = df.round(decimals={'logloss': 6, 'auc': 4, 'acc': 4, 'ystd': 4,
                                'sharpe': 4, 'consis': 4})
        info_str = ', '.join(info['region']) + '; '
        info_str += '{} eras'.format(len(info['era']))
        print(info_str)
        with pd.option_context('display.colheader_justify', 'left'):
            print(df.to_string(index=True))

    def performance_df(self, data, era_as_str=True, region_as_str=True):
        cols = ['logloss', 'auc', 'acc', 'ystd', 'sharpe', 'consis']
        metrics, info = metrics_per_name(data,
                                         self,
                                         columns=cols,
                                         era_as_str=era_as_str,
                                         region_as_str=region_as_str)
        return metrics, info

    def dominance(self, data, sort_by='logloss'):
        "Mean (across eras) of fraction of models bested per era"
        df = self.dominance_df(data)
        df = df.sort_values([sort_by], ascending=[False])
        df = df.round(decimals=4)
        with pd.option_context('display.colheader_justify', 'left'):
            print(df.to_string(index=True))

    def dominance_df(self, data):
        "Mean (across eras) of fraction of models bested per era"
        columns = ['logloss', 'auc', 'acc']
        mpe, regions = metrics_per_era(data, self, columns=columns)
        dfs = []
        for i, col in enumerate(columns):
            pivot = mpe.pivot(index='era', columns='name', values=col)
            names = pivot.columns.tolist()
            a = pivot.values
            n = a.shape[1] - 1.0
            if n == 0:
                raise ValueError("Must have at least two names")
            m = []
            for j in range(pivot.shape[1]):
                if col == 'logloss':
                    z = (a[:, j].reshape(-1, 1) < a).sum(axis=1) / n
                else:
                    z = (a[:, j].reshape(-1, 1) > a).sum(axis=1) / n
                m.append(z.mean())
            df = pd.DataFrame(data=m, index=names, columns=[col])
            dfs.append(df)
        df = pd.concat(dfs, axis=1)
        return df

    def concordance(self, data):
        "Less than 0.12 is passing; data should be the full dataset."
        return concordance(data, self)

    def correlation(self, name=None):
        "Correlation of predictions; by default reports given for each model"
        if name is None:
            names = self.names
        else:
            names = [name]
        z = self.df.values
        znames = self.names
        idx = np.isfinite(z.sum(axis=1))
        z = z[idx]
        z = (z - z.mean(axis=0)) / z.std(axis=0)
        for name in names:
            print(name)
            idx = znames.index(name)
            corr = np.dot(z[:, idx], z) / z.shape[0]
            index = (-corr).argsort()
            for ix in index:
                zname = znames[ix]
                if name != zname:
                    print("   {:.4f} {}".format(corr[ix], zname))

    def originality(self, submitted_names):
        "Which models are original given the models already submitted?"

        # predictions of models already submitted
        ys = self.df[submitted_names].values

        # models that have not been submitted; we will report on these
        names = self.names
        names = [m for m in names if m not in submitted_names]

        # originality
        df = pd.DataFrame(index=names, columns=['corr', 'ks', 'original'])
        for name in names:
            corr = True
            ks = True
            y = self.df[name].values
            for i in range(ys.shape[1]):
                if corr and pearsonr(y, ys[:, i]) > 0.95:
                    corr = False
                if ks and ks_2samp(y, ys[:, i]) <= 0.03:
                    ks = False
            df.loc[name, 'corr'] = corr
            df.loc[name, 'ks'] = ks
            df.loc[name, 'original'] = corr and ks

        return df

    def compare(self, data, prediction):
        "Compare performance of predictions with the same names"
        cols = ['logloss1', 'logloss2', 'win1',
                'corr', 'maxdiff', 'ystd1', 'ystd2']
        comp = pd.DataFrame(columns=cols)
        names = []
        for name in self.names:
            if name in prediction:
                names.append(name)
        if len(names) == 0:
            return comp
        ids = data.ids
        df1 = self.loc[ids]
        df2 = prediction.loc[ids]
        p1 = self[names]
        p2 = prediction[names]
        m1 = p1.metrics_per_era(data, metrics=['logloss', 'auc', 'ystd'],
                                era_as_str=False)
        m2 = p2.metrics_per_era(data, metrics=['logloss', 'auc', 'ystd'],
                                era_as_str=False)
        for name in names:

            m1i = m1[m1.name == name]
            m2i = m2[m2.name == name]

            if (m1i.index != m2i.index).any():
                raise IndexError("Can only handle aligned eras")

            logloss1 = m1i.logloss.mean()
            logloss2 = m2i.logloss.mean()
            win1 = (m1i.logloss < m2i.logloss).mean()

            y1 = df1[name].y.reshape(-1)
            y2 = df2[name].y.reshape(-1)

            corr = np.corrcoef(y1, y2)[0, 1]
            maxdiff = np.abs(y1 - y2).max()
            ystd1 = y1.std()
            ystd2 = y2.std()

            m = [logloss1, logloss2, win1, corr, maxdiff, ystd1, ystd2]
            comp.loc[name] = m

        return comp

    def copy(self):
        "Copy of prediction"
        if self.df is None:
            return Prediction(None)
        # df.copy(deep=True) doesn't copy index. So:
        df = self.df
        df = pd.DataFrame(df.values.copy(),
                          df.index.copy(deep=True),
                          df.columns.copy())
        return Prediction(df)

    def __getitem__(self, name):
        "Prediction indexing is by model name(s)"
        if isinstance(name, base_string):
            p = Prediction(self.df[name].to_frame(name))
        else:
            p = Prediction(self.df[name])
        return p

    def __setitem__(self, name, prediction):
        "Add (or replace) a prediction by name"
        if prediction.df.shape[1] != 1:
            raise ValueError("Can only insert a single model at a time")
        prediction.df.columns = [name]
        self.df = self.merge(prediction).df

    @property
    def loc(self):
        "indexing by row ids"
        return Loc(self)

    def __add__(self, prediction):
        "Merge predictions"
        return self.merge(prediction)

    def __iadd__(self, prediction):
        "Merge predictions"
        return self.merge(prediction)

    def __contains__(self, name):
        "Is `name` already in prediction? True or False"
        return name in self.df

    def __eq__(self, prediction):
        "Check if prediction objects are equal or not; order matters"
        if self.df is None and prediction.df is None:
            return True
        return self.df.equals(prediction.df)

    @property
    def size(self):
        if self.df is None:
            return 0
        return self.df.size

    @property
    def shape(self):
        if self.df is None:
            return (0, 0)
        return self.df.shape

    def __len__(self):
        "Number of rows"
        if self.df is None:
            return 0
        return self.df.__len__()

    def __repr__(self):
        shape = self.shape
        if shape[1] == 0:
            frac_miss = 0.0
        else:
            frac_miss = self.df.isna().mean()[0]
        fmt = 'Prediction({} rows x {} names; {:.4f} missing)'
        return fmt.format(shape[0], shape[1], frac_miss)


def load_prediction(filename):
    "Load prediction object from hdf archive"
    df = pd.read_hdf(filename, key=HDF_PREDICTION_KEY)
    return Prediction(df)


class Loc(object):
    "Utility class for the loc method."

    def __init__(self, prediction):
        self.prediction = prediction

    def __getitem__(self, index):
        return Prediction(self.prediction.df.loc[index])
