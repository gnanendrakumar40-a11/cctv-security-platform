import React, { useState, useEffect } from "react";
import "./App.css";

const API_BASE = "http://127.0.0.1:8000";

export default function App() {
  const [targetIp, setTargetIp] = useState("127.0.0.1");
  const [port, setPort] = useState("8081");
  const [scans, setScans] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loadingScan, setLoadingScan] = useState(false);
  const [exporting, setExporting] = useState(false);

  // Fetch scans and alerts on load
  useEffect(() => {
    fetchScans();
    fetchAlerts();

    // Auto-poll ML Behavioral Alerts every 4 seconds
    const interval = setInterval(fetchAlerts, 4000);
    return () => clearInterval(interval);
  }, []);

  const fetchScans = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/scans`);
      if (res.ok) {
        const data = await res.json();
        setScans(data);
      }
    } catch (err) {
      console.error("Failed to fetch scan logs:", err);
    }
  };

  const fetchAlerts = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/alerts`);
      if (res.ok) {
        const data = await res.json();
        setAlerts(data);
      }
    } catch (err) {
      console.error("Failed to fetch ML alerts:", err);
    }
  };

  const handleExecuteAudit = async (e) => {
    e.preventDefault();
    setLoadingScan(true);
    try {
      const res = await fetch(`${API_BASE}/api/scans`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          target_ip: targetIp,
          port: parseInt(port, 10),
        }),
      });

      if (res.ok) {
        await fetchScans();
      } else {
        alert("Scan execution failed. Verify target authorization.");
      }
    } catch (err) {
      console.error("Audit request failed:", err);
      alert("Could not reach backend API.");
    } finally {
      setLoadingScan(false);
    }
  };

  const handleExportReport = async () => {
    setExporting(true);
    try {
      const res = await fetch(`${API_BASE}/api/reports/export`);
      if (!res.ok) {
        throw new Error("Backend export endpoint failed.");
      }
      const data = await res.json();
      
      // Download payload as formatted JSON
      const blob = new Blob([JSON.stringify(data, null, 2)], {
        type: "application/json",
      });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `cctv_vapt_security_report_${Date.now()}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Failed to export security report:", err);
      alert("Error generating report. Ensure backend endpoint is online.");
    } finally {
      setExporting(false);
    }
  };

  const getPostureBadgeClass = (posture) => {
    switch (posture?.toUpperCase()) {
      case "CRITICAL":
      case "HIGH":
        return "badge-high";
      case "MEDIUM":
        return "badge-medium";
      case "LOW":
      case "INFO":
        return "badge-info";
      default:
        return "badge-info";
    }
  };

  return (
    <div className="dashboard-container">
      {/* Header Section */}
      <header className="dashboard-header">
        <div>
          <h1>CCTV / DVR Automated VAPT & Threat Monitoring</h1>
          <p className="subtitle">
            National Technical Research Organisation (NTRO) Security Pipeline
          </p>
        </div>
        <div>
          <button
            className="btn-export"
            onClick={handleExportReport}
            disabled={exporting}
          >
            {exporting ? "Generating..." : "📥 Export Audit Report"}
          </button>
        </div>
      </header>

      {/* Audit Action Box */}
      <section className="card form-card">
        <h3>Run Automated VAPT Audit</h3>
        <form onSubmit={handleExecuteAudit} className="audit-form">
          <input
            type="text"
            placeholder="Target IP (e.g. 127.0.0.1)"
            value={targetIp}
            onChange={(e) => setTargetIp(e.target.value)}
            required
          />
          <input
            type="number"
            placeholder="Port (e.g. 8081)"
            value={port}
            onChange={(e) => setPort(e.target.value)}
            required
          />
          <button type="submit" className="btn-primary" disabled={loadingScan}>
            {loadingScan ? "Scanning..." : "Execute Audit"}
          </button>
        </form>
      </section>

      {/* Multi-Pane SOC View */}
      <div className="grid-split">
        {/* Left Pane: Vulnerability Scans */}
        <section className="card">
          <div className="section-title">
            <h3>Vulnerability Scans Recorded ({scans.length})</h3>
          </div>
          <div className="table-responsive">
            <table>
              <thead>
                <tr>
                  <th>Target</th>
                  <th>Posture</th>
                  <th>Score</th>
                  <th>Banner</th>
                </tr>
              </thead>
              <tbody>
                {scans.length === 0 ? (
                  <tr>
                    <td colSpan="4" className="empty-cell">
                      No scan history logged yet.
                    </td>
                  </tr>
                ) : (
                  scans.map((s, idx) => (
                    <tr key={s.id || idx}>
                      <td>
                        <code>
                          {s.target_ip}:{s.port}
                        </code>
                      </td>
                      <td>
                        <span
                          className={`badge ${getPostureBadgeClass(s.posture)}`}
                        >
                          {s.posture}
                        </span>
                      </td>
                      <td>{s.score}</td>
                      <td className="banner-cell">{s.banner || "N/A"}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </section>

        {/* Right Pane: ML Anomaly Feeds */}
        <section className="card">
          <div className="section-title">
            <h3>ML Traffic Anomaly Alerts ({alerts.length})</h3>
          </div>
          <div className="table-responsive">
            <table>
              <thead>
                <tr>
                  <th>Device</th>
                  <th>Status</th>
                  <th>Confidence</th>
                  <th>Details</th>
                </tr>
              </thead>
              <tbody>
                {alerts.length === 0 ? (
                  <tr>
                    <td colSpan="4" className="empty-cell">
                      No active anomalies detected.
                    </td>
                  </tr>
                ) : (
                  alerts.map((a, idx) => (
                    <tr key={a.id || idx}>
                      <td>
                        <code>{a.device_ip}</code>
                      </td>
                      <td>
                        <span className="badge badge-alert">{a.status}</span>
                      </td>
                      <td>{a.threat_score?.toFixed(2)}</td>
                      <td className="details-cell">{a.details}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
}