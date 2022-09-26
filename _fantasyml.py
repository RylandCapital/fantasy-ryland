import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import scipy
    
    
def _neutralize(self, df, columns, by, proportion=1.0):
    scores = df[columns]
    exposures = df[by].values
    scores = scores - proportion * exposures.dot(
            np.linalg.pinv(exposures).dot(scores))
    return scores / scores.std(ddof=0)

def _normalize(self, df):
    X = (df.rank(method="first") - 0.5) / len(df)
    return scipy.stats.norm.ppf(X)

def normalize_and_neutralize(self, df, columns, by, proportion=1.0):
    # Convert the scores to a normal distribution
    df[columns] = self._normalize(df[columns])
    df[columns] = self._neutralize(df, columns, by, proportion)
    return df[columns]

def neuterPredictions(self, proportion):
    df = self.tournamentdf.set_index('id').join(
            self.prediction_upload_df.set_index('id'))
    features = [c for c in self.tournamentdf if c.startswith("feature")]
    df['preds_neutralized'] =  df.groupby("era").apply(
        lambda x: rc.normalize_and_neutralize(x, ['prediction'],
                                                features, proportion))
    scaler = MinMaxScaler()
    df["prediction"] = scaler.fit_transform(
            df[["preds_neutralized"]])
    return df[["prediction"]].reset_index()