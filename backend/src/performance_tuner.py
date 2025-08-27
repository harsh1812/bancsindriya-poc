from root_cause_analysis import analyze_root_cause

def suggest_tuning(metrics):
    rc = analyze_root_cause(metrics)
    mapping = {
        "CPU_SPIKE": [
            "Investigate hot threads and top processes",
            "Scale up replicas or move non-critical jobs to off-peak times",
            "Enable CPU throttling for batch jobs"
        ],
        "DB_LOCK": [
            "Identify long-running queries and add appropriate indexes",
            "Increase DB connection pool limits carefully",
            "Reschedule heavy batch jobs to avoid overlap"
        ],
        "BATCH_OVERLAP": [
            "Reschedule overlapping batch jobs to non-overlapping windows",
            "Add guard rails to prevent simultaneous runs",
            "Reduce batch parallelism / increase replicas for processing"
        ],
        "UNKNOWN": [
            "Collect more data and check logs",
            "Run deeper diagnostic (AWR / trace) if possible"
        ],
        "NO_DATA": ["No metrics available to suggest tuning"]
    }
    return mapping.get(rc, mapping["UNKNOWN"])
