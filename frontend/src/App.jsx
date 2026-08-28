import React, { useState, useEffect } from "react"

const API_BASE = "http://127.0.0.1:8000"

export default function App() {
  const [scans, setScans] = useState([])
  const [alerts, setAlerts] = useState([])
  const [targetIp, setTargetIp] = useState("127.0.0.1")
  const [targetPort, setTargetPort] = useState(8081)
  const [loading, setLoading] = useState(false)

  const fetchData = async () => {
    try {
      const scansRes = await fetch(`${API_BASE}/api/scans`)
      if (scansRes.ok) {
        const scanData = await scansRes.json()
        setScans(scanData)
      }
      
      const alertsRes = await fetch(`${API_BASE}/api/alerts`)
      if (alertsRes.ok) {
        const alertData = await alertsRes.json()
        setAlerts(alertData)
      }
    } catch (err) {
      console.error("Failed to connect to backend engine:", err)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 4000)
    return () => clearInterval(interval)
  }, [])

  const triggerScan = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/api/scans`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target_ip: targetIp, target_port: parseInt(targetPort) })
      })
      if (res.ok) {
        await fetchData()
      }
    } catch (err) {
      alert("Failed to initiate scan: " + err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="dashboard-container">
      <div className="header-banner">
        <h1>Surveillance VAPT & ML Threat Center</h1>
        <p>Real-Time Surveillance Security Assessment & Behavioral Anomaly Engine</p>
      </div>

      <div className="card" style={{ marginBottom: "20px" }}>
        <h2>Run Automated VAPT Audit</h2>
        <form onSubmit={triggerScan} className="form-group">
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
            value={targetPort}
            onChange={(e) => setTargetPort(e.target.value)}
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? "Auditing Target..." : "Execute Audit"}
          </button>
        </form>
      </div>

      <div className="grid-layout">
        <div className="card">
          <h2>Vulnerability Scans Recorded ({scans.length})</h2>
          <table className="data-table">
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
                <tr><td colSpan="4" style={{ textAlign: "center" }}>No scans logged yet</td></tr>
              ) : (
                scans.map((scan) => (
                  <tr key={scan.id}>
                    <td>{scan.target_ip}:{scan.target_port}</td>
                    <td>
                      <span className={`badge ${scan.risk_level === "CRITICAL" ? "critical" : scan.risk_level === "HIGH" ? "high" : "normal"}`}>
                        {scan.risk_level}
                      </span>
                    </td>
                    <td>{scan.risk_score}</td>
                    <td>{scan.device_banner}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        <div className="card">
          <h2>ML Traffic Anomaly Alerts ({alerts.length})</h2>
          <table className="data-table">
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
                <tr><td colSpan="4" style={{ textAlign: "center" }}>No active anomaly threats</td></tr>
              ) : (
                alerts.map((alert) => (
                  <tr key={alert.id}>
                    <td>{alert.device_ip}</td>
                    <td>
                      <span className="badge critical">{alert.status}</span>
                    </td>
                    <td>{alert.threat_score}</td>
                    <td>{alert.details}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}