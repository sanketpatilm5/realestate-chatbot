import React, { useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Legend,
  Tooltip,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Legend,
  Tooltip
);

// Correct API base (NO extra /chat/ here!)
const API_BASE =
  process.env.REACT_APP_API_BASE ||
  "https://realestate-chatbot-fdpo.onrender.com";

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    const userMsg = { role: "user", text: query };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      // 👉 Corrected POST request
      const res = await fetch(`${API_BASE}/api/chat/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();

      if (!res.ok) {
        setMessages((prev) => [
          ...prev,
          { role: "bot", text: data.error || "Something went wrong.", error: true },
        ]);
      } else {
        setMessages((prev) => [
          ...prev,
          { role: "bot", text: data.summary, data },
        ]);
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Network error", error: true },
      ]);
    } finally {
      setLoading(false);
      setQuery("");
    }
  };

  const renderChart = (data) => {
    if (!data || !data.chart) return null;

    const chartData = {
      labels: data.chart.labels,
      datasets: data.chart.datasets.map((ds) => ({
        ...ds,
        borderWidth: 2,
        tension: 0.25,
      })),
    };

    return (
      <div className="my-3">
        <h6>Trend Chart</h6>
        <Line data={chartData} />
      </div>
    );
  };

  const renderTable = (data) => {
    if (!data) return null;

    if (data.mode === "single" && data.table) {
      const rows = data.table;
      if (!rows.length) return null;
      const cols = Object.keys(rows[0]);

      return (
        <div className="table-responsive my-3">
          <h6>Filtered Data</h6>
          <table className="table table-sm table-striped">
            <thead>
              <tr>
                {cols.map((c) => (
                  <th key={c}>{c}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((r, idx) => (
                <tr key={idx}>
                  {cols.map((c) => (
                    <td key={c}>{r[c]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    }

    if (data.mode === "compare" && data.tables) {
      return (
        <div className="my-3">
          {Object.entries(data.tables).map(([area, rows]) => {
            if (!rows.length) return null;
            const cols = Object.keys(rows[0]);
            return (
              <div key={area} className="mb-3">
                <h6>Data for {area}</h6>
                <div className="table-responsive">
                  <table className="table table-sm table-striped">
                    <thead>
                      <tr>
                        {cols.map((c) => (
                          <th key={c}>{c}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {rows.map((r, idx) => (
                        <tr key={idx}>
                          {cols.map((c) => (
                            <td key={c}>{r[c]}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            );
          })}
        </div>
      );
    }

    return null;
  };

  const renderDownloadButton = (data) => {
    if (!data) return null;

    const rows =
      data.mode === "single"
        ? data.table || []
        : data.mode === "compare"
        ? Object.values(data.tables || {}).flat()
        : [];

    if (!rows || !rows.length) return null;

    const handleDownload = () => {
      const blob = new Blob([JSON.stringify(rows, null, 2)], {
        type: "application/json",
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "filtered_data.json";
      a.click();
      URL.revokeObjectURL(url);
    };

    return (
      <button className="btn btn-sm btn-outline-secondary my-2" onClick={handleDownload}>
        Download Data
      </button>
    );
  };

  return (
    <div className="container py-4">
      <h2 className="mb-3">Real Estate Analysis Chatbot</h2>
      <p className="text-muted">
        Try queries like: <code>Analyze Akurdi</code>,{" "}
        <code>Compare Ambegaon Budruk and Aundh demand trends</code>,{" "}
        <code>Show price growth for Akurdi over the last 3 years</code>.
      </p>

      <div className="card mb-3">
        <div className="card-body" style={{ maxHeight: "60vh", overflowY: "auto" }}>
          {messages.map((m, idx) => (
            <div key={idx} className={`mb-3 ${m.role === "user" ? "text-end" : "text-start"}`}>
              <div
                className={`d-inline-block p-2 rounded ${
                  m.role === "user"
                    ? "bg-primary text-white"
                    : m.error
                    ? "bg-danger text-white"
                    : "bg-light"
                }`}
                style={{ maxWidth: "80%" }}
              >
                {m.text}
              </div>

              {m.role === "bot" && m.data && (
                <div className="mt-2">
                  {renderChart(m.data)}
                  {renderTable(m.data)}
                  {renderDownloadButton(m.data)}
                </div>
              )}
            </div>
          ))}
          {messages.length === 0 && <div className="text-muted">Start by asking a question…</div>}
        </div>
      </div>

      <form onSubmit={handleSubmit} className="d-flex gap-2">
        <input
          type="text"
          className="form-control"
          placeholder="Type your real estate query..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          disabled={loading}
        />
        <button className="btn btn-primary" disabled={loading}>
          {loading ? "Analyzing..." : "Send"}
        </button>
      </form>
    </div>
  );
}

export default App;
