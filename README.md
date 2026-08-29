# 🛡️ Automated VAPT & Behavioral Threat Monitoring Platform for CCTV / DVR Systems

> **Problem Statement Alignment (NTRO):** Automated Vulnerability Assessment and Penetration Testing (VAPT) and real-time behavioral traffic anomaly detection for IP surveillance cameras and digital video recorders.

---

## 📌 Architecture Overview

The system consists of four integrated modules:

* **VAPT Scanner Engine (`scanner/`):** Performs TCP socket analysis, banner grabbing, HTTP response inspection, and CVSS-aligned risk scoring based on CVE patterns.
* **ML Anomaly Detection (`ml/`):** Uses an Isolation Forest unsupervised model to analyze telemetry streams (packet rates, throughput, session bursts) and score anomaly confidence.
* **Appliance & Traffic Simulator (`simulator/`):** Emulates a live Hikvision surveillance target with an interactive HTTP management console (`:8081`) and generates simulated volumetric and authentication attacks.
* **SOC Monitoring Dashboard (`frontend/` & `backend/`):** FastAPI backend powered by SQLite with a React dark-mode Security Operations Center (SOC) dashboard.

---

## 🚀 Quick Setup & Execution

### **Prerequisites**
* Python 3.10+
* Node.js 18+

### **1. Start the Backend API**
```powershell
python -m uvicorn backend.main:app --port 8000 --reload