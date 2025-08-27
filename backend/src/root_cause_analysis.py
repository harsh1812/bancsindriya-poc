def analyze_root_cause(metrics):
    """
    Simple rule-based RCA:
    - if CPU very high => CPU_SPIKE
    - if avg_latency very high and tx_count low => DB_LOCK
    - if many consecutive latency increases => BATCH_OVERLAP
    """
    if not metrics:
        return "NO_DATA"
    latest = metrics[-1]
    avg_cpu = sum(m["cpu"] for m in metrics) / len(metrics)
    avg_latency = sum(m["avg_latency"] for m in metrics) / len(metrics)
    tx_avg = sum(m["tx_count"] for m in metrics) / len(metrics)

    # rules (very simple)
    if avg_cpu > 80 or latest["cpu"] > 85:
        return "CPU_SPIKE"
    if latest["avg_latency"] > 500 and latest["tx_count"] < tx_avg * 0.5:
        return "DB_LOCK"
    # detect many recent increases in latency
    ups = 0
    for i in range(1, len(metrics)):
        if metrics[i]["avg_latency"] > metrics[i-1]["avg_latency"]:
            ups += 1
    if ups > len(metrics) * 0.6:
        return "BATCH_OVERLAP"
    return "UNKNOWN"
