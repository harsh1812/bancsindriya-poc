import threading
import time
import random
from collections import deque

class MetricsCollector:
    """
    Simulates per-second metrics and keeps a rolling buffer in memory.
    Each metric is a dict: {ts, tx_count, avg_latency, cpu}
    """
    def __init__(self, maxlen=3600):
        self.lock = threading.Lock()
        self.data = deque(maxlen=maxlen)
        self._running = True
        t = threading.Thread(target=self._generate_loop, daemon=True)
        t.start()

    def _generate_loop(self):
        while self._running:
            ts = time.time()
            base_tx = 100 + random.randint(-12, 12)
            avg_latency = max(5, random.gauss(120, 18))
            cpu = max(3, random.gauss(50, 8))
            # small chance to produce an anomaly spike
            if random.random() < 0.02:
                avg_latency *= random.uniform(2.5, 6.0)
                cpu += random.uniform(15, 30)
                # sometimes tx drops with lock-like behavior
                if random.random() < 0.3:
                    base_tx = max(1, int(base_tx * 0.2))
            item = {"ts": ts, "tx_count": int(base_tx), "avg_latency": float(avg_latency), "cpu": float(cpu)}
            with self.lock:
                self.data.append(item)
            time.sleep(1)

    def get_latest(self, n=60):
        with self.lock:
            return list(self.data)[-n:]
