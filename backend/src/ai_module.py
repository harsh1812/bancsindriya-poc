import numpy as np

class Predictor:
    """
    Very small statistical anomaly detector:
    - compute mean/std of avg_latency over history
    - mark anomaly if latest point > mean + 3*std
    Returns (is_anomaly, score=zscore, details)
    """
    def __init__(self):
        pass

    def check(self, metrics):
        if not metrics:
            return False, 0.0, {"reason": "no data"}
        latencies = np.array([m["avg_latency"] for m in metrics], dtype=float)
        mean = float(np.mean(latencies))
        std = float(np.std(latencies)) + 1e-9
        latest = float(latencies[-1])
        z = (latest - mean) / std
        is_anom = z > 3.0
        details = {"metric": "avg_latency", "mean": mean, "std": std, "latest": latest, "zscore": float(z)}
        return bool(is_anom), float(z), details
