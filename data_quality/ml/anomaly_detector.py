import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


class AnomalyDetector:
    """
    ML-based anomaly detector using Isolation Forest.
    Accepts a list of dicts (JSON records) and returns
    anomaly labels and scores for each record.
    """

    def __init__(self, contamination=0.1, random_state=42):
        """
        contamination: expected proportion of anomalies (0.0 - 0.5)
        """
        self.contamination = contamination
        self.random_state = random_state
        self.model = IsolationForest(
            contamination=self.contamination,
            random_state=self.random_state
        )
        self.scaler = StandardScaler()

    def _prepare_dataframe(self, records: list[dict]) -> pd.DataFrame:
        """
        Convert list of JSON records to a numeric DataFrame.
        Only numeric columns are used for detection.
        """
        df = pd.DataFrame(records)
        numeric_df = df.select_dtypes(include=[np.number])

        if numeric_df.empty:
            raise ValueError("No numeric columns found in the dataset.")

        # Drop columns with all NaN
        numeric_df = numeric_df.dropna(axis=1, how='all')

        # Fill remaining NaN with column mean
        numeric_df = numeric_df.fillna(numeric_df.mean())

        return numeric_df

    def detect(self, records: list[dict]) -> dict:
        """
        Run anomaly detection on a list of records.

        Returns a dict with:
          - total_records: int
          - anomalies_found: int
          - anomaly_indices: list of row indices flagged as anomalies
          - scores: list of anomaly scores per record
          - details: list of dicts with per-record results
        """
        df = self._prepare_dataframe(records)

        # Scale features
        scaled = self.scaler.fit_transform(df)

        # Fit and predict
        # IsolationForest returns: -1 = anomaly, 1 = normal
        predictions = self.model.fit_predict(scaled)
        scores = self.model.decision_function(scaled)  # Lower = more anomalous

        anomaly_indices = [
            int(i) for i, pred in enumerate(predictions) if pred == -1
        ]

        details = []
        for i, (pred, score) in enumerate(zip(predictions, scores)):
            details.append({
                "record_index": i,
                "is_anomaly": bool(pred == -1),
                "anomaly_score": round(float(score), 4),
                "original_record": records[i]
            })

        return {
            "total_records": len(records),
            "anomalies_found": len(anomaly_indices),
            "anomaly_indices": anomaly_indices,
            "scores": [round(float(s), 4) for s in scores],
            "details": details
        }