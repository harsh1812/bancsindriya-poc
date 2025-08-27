import React, { useEffect, useState } from "react";

function MetricsTable({ metrics }) {
  return (
    <table border="1" cellPadding="6">
      <thead>
        <tr><th>ts</th><th>tx_count</th><th>avg_latency</th><th>cpu</th></tr>
      </thead>
      <tbody>
        {metrics.map((m, i) => (
          <tr key={i}>
            <td>{new Date(m.ts * 1000).toLocaleTimeString()}</td>
            <td>{m.tx_count}</td>
            <td>{m.avg_latency.toFixed(1)}</td>
            <td>{m.cpu.toFixed(1)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default function App() {
  const [metrics, setMetrics] = useState([]);
  const [health, setHealth] = useState(null);
  const [rca, setRca] = useState(null);
  const [tuning, setTuning] = useState([]);

  async function fetchAll() {
    try {
      const m = await fetch("http://localhost:8000/metrics").then(r=>r.json());
      setMetrics(m);
      const h = await fetch("http://localhost:8000/health").then(r=>r.json());
      setHealth(h);
      const r = await fetch("http://localhost:8000/root_cause").then(r=>r.json());
      setRca(r.root_cause);
      const t = await fetch("http://localhost:8000/tune").then(r=>r.json());
      setTuning(t.tuning_suggestions);
    } catch (e) {
      console.error(e);
    }
  }

  useEffect(() => {
    fetchAll();
    const id = setInterval(fetchAll, 2000);
    return () => clearInterval(id);
  }, []);

  return (
    <div style={{padding:20, fontFamily:'Arial'}}>
      <h1>BancsINDRIYA+ POC</h1>

      <h2>Health</h2>
      {health ? (
        <div>
          <b>Anomaly:</b> {String(health.anomaly)} &nbsp; <b>score:</b> {health.score.toFixed(2)}
          <pre>{JSON.stringify(health.details, null, 2)}</pre>
        </div>
      ) : <div>Loading...</div>}

      <h2>Root Cause</h2>
      <div>{rca || "Loading..."}</div>

      <h2>Tuning Suggestions</h2>
      <ul>
        {tuning.map((s, i) => <li key={i}>{s}</li>)}
      </ul>

      <h2>Recent Metrics (latest 20)</h2>
      <MetricsTable metrics={metrics.slice(-20).reverse()} />
    </div>
  );
}
