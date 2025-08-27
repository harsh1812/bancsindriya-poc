from fastapi import FastAPI
from ai_module import Predictor
from metrics_collector import MetricsCollector
from root_cause_analysis import analyze_root_cause
from performance_tuner import suggest_tuning

app = FastAPI(title="BancsINDRIYA+ POC")

collector = MetricsCollector()     # starts a background thread that simulates metrics
predictor = Predictor()

@app.get("/metrics")
def get_metrics(n: int = 60):
    """Return last n metrics (default 60 samples)."""
    return collector.get_latest(n)

@app.get("/health")
def health_check():
    """Return a simple anomaly check (True/False) and score/details."""
    metrics = collector.get_latest(60)
    is_anom, score, details = predictor.check(metrics)
    return {"anomaly": bool(is_anom), "score": float(score), "details": details}

@app.get("/root_cause")
def root_cause():
    metrics = collector.get_latest(60)
    cause = analyze_root_cause(metrics)
    return {"root_cause": cause}

@app.get("/tune")
def tune():
    metrics = collector.get_latest(60)
    suggestions = suggest_tuning(metrics)
    return {"tuning_suggestions": suggestions}
