<!DOCTYPE html>
<html>

<body>

<h1>🔐 Splunk-Guard: Lightweight ML-Powered Threat Detection</h1>

<p><strong>Splunk-Guard</strong> is a hybrid, ML-driven threat detection system for monitoring USB activity and VPN login anomalies. Built using Splunk's free version, the Machine Learning Toolkit (MLTK), and an interactive <a href="https://splunkguard-jhwvq3nyktjevytf7tjjye.streamlit.app/" target="_blank">Streamlit Web Dashboard</a>, it provides affordable threat detection for smaller teams, prototypes, and educational use.</p>

<p>▶️ <strong>Watch Demo:</strong> <a href="https://www.youtube.com/watch?v=B4yl0_dWzko" target="_blank">YouTube Overview Video</a></p>
<p>🌐 <strong>Try the Live App:</strong> <a href="https://splunkguard-jhwvq3nyktjevytf7tjjye.streamlit.app/" target="_blank">Splunk-Guard Web Dashboard</a></p>

<hr>

<h2>🚀 Project Highlights</h2>
<ul>
  <li>Detects abnormal USB write patterns to flag potential data exfiltration</li>
  <li>Identifies suspicious VPN logins from unusual or distant locations</li>
  <li>Streamlit Web App for interactive anomaly detection, even without Splunk</li>
  <li>Splunk dashboards and alerts included for real-time enterprise monitoring</li>
  <li>Leverages free Splunk tools — No paid plugins required</li>
</ul>

<hr>

<h2>⚡ Features</h2>
<ul>
  <li><strong>USB Anomaly Detection:</strong> Detects unusual spikes in per-device write volumes</li>
  <li><strong>VPN Login Anomalies:</strong> Flags geo-distance outliers for potential credential misuse</li>
  <li><strong>Modes:</strong> 
    <ul>
      <li>Live Mode — Connects to your Splunk backend via REST API</li>
      <li>CSV Upload — Analyze your own USB or VPN logs</li>
      <li>Demo Mode — Uses built-in synthetic data for offline testing</li>
    </ul>
  </li>
  <li>Interactive charts, anomaly reports, and CSV exports</li>
</ul>

<hr>

<h2>📂 Project Structure</h2>
<pre>
├── .devcontainer/                # VSCode Devcontainer settings
├── .streamlit/                   # Streamlit config files (secrets.toml)
├── Splunk_Guard/                 # Core Splunk content (dashboards, models)
│   ├── dashboards/               # Splunk Studio dashboard JSON exports
│   ├── mltk_configs/             # Model guides for Splunk MLTK
│   ├── spl_queries/              # SPL scripts for field extraction & models
|   ├── screenshots/              # Backened preview images for judges/users
|   └── sample_data/              # Example USB and VPN log files
├── app.py                        # Final Streamlit Web Application foe local system use
├── demos_app.py                  # Alternate Streamlit demo version for public usage
├── requirements.txt              # Python dependencies
├── README.md                     # Project overview (this file)
├── LICENSE                       # MIT License
</pre>

<hr>

<h2>🛠️ Setup & Usage</h2>

<h3>Streamlit Web App</h3>
<ol>
  <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
  <li>Update <code>.streamlit/secrets.toml</code> with Splunk credentials (for Live mode)</li>
  <li>Run the app: <code>streamlit run app.py</code></li>
  <li>Or use the public link: <a href="https://splunkguard-jhwvq3nyktjevytf7tjjye.streamlit.app/" target="_blank">Splunk-Guard Web Dashboard</a></li>
</ol>

<h3>Splunk Backend (Optional)</h3>
<ol>
  <li>Install Splunk Enterprise (Free Trial) + Machine Learning Toolkit (MLTK)</li>
  <li>Ingest <code>usb_logs.csv</code> and <code>vpn_logs.csv</code> into indexes (e.g., <code>splunk_guard</code>, <code>vpn</code>)</li>
  <li>Use provided SPL scripts for field extraction and anomaly model training</li>
  <li>Import dashboards from <code>Splunk_Guard/dashboards/</code></li>
  <li>Configure alerts using queries in <code>spl_queries/</code></li>
</ol>

<hr>

<h2>📊 Example Visuals</h2>
<ul>
  <li>🔌 USB Write Volume Trends and Outlier Detection</li>
  <li>🌍 VPN Login Geo Distribution and Distance-Based Anomalies</li>
  <li>📈 User and Device-Level Activity Charts</li>
</ul>

<p>Screenshots available in the <code>screenshots/</code> folder.</p>

<hr>

<h2>💡 Real-World Use Cases</h2>
<ul>
  <li>Insider Threat Detection — Unusual USB activity suggests data exfiltration</li>
  <li>Credential Misuse Alerts — VPN logins from suspicious geo-locations</li>
  <li>Security Demos — Showcase Splunk's ML capabilities with real-world examples</li>
</ul>

<hr>

<h2>⚠️ Disclaimer</h2>
<p>Splunk-Guard is intended for research, educational, and prototype purposes. It is not production-hardened. Perform extensive security validation before enterprise deployment.</p>

<hr>

<h2>📝 License</h2>
<p>Released under the MIT License. See <code>LICENSE</code> for full terms.</p>

</body>
</html>
