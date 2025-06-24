<h1>🔐 Splunk-Guard: Lightweight ML-Powered Threat Detection</h1>

<p><strong>Splunk-Guard</strong> is a lightweight, ML-driven threat detection system built entirely with Splunk's free tools and the Machine Learning Toolkit (MLTK). It demonstrates how to monitor USB and VPN activities for anomalies without costly security platforms.</p>

<p>▶️ <strong>Watch Demo:</strong> <a href="https://www.youtube.com/watch?v=B4yl0_dWzko" target="_blank">YouTube Demo Video</a></p>
<p>🌐 <strong>Try Live App:</strong> <a href="https://splunkguard-kmzqnlsegnwukfn75u9vle.streamlit.app/" target="_blank">Splunk-Guard Web Dashboard</a></p>

<hr>

<h2>🚀 Project Highlights</h2>
<ul>
  <li>Detects unusual USB write operations to flag potential data exfiltration</li>
  <li>Identifies suspicious VPN logins from distant or unfamiliar locations</li>
  <li>Interactive Splunk dashboards with real-time monitoring</li>
  <li>Fully built using free Splunk + MLTK — No paid plugins required</li>
  <li>Ideal for research, learning, and SMB security monitoring prototypes</li>
</ul>

<hr>

<h2>⚡ Features</h2>
<ul>
  <li><strong>USB Anomaly Detection</strong>: ML model monitors per-device USB write volumes for outliers</li>
  <li><strong>VPN Login Detection</strong>: Flags unexpected login distances or locations per user</li>
  <li><strong>Custom Dashboards</strong>: Real-time visualization of threats</li>
  <li><strong>Alerts</strong>: Automated notifications when anomalies are detected</li>
</ul>

<hr>

<h2>📂 Project Structure</h2>
<pre>
├── data/                  # Contains USB and VPN log datasets (.csv)
├── dashboards/            # Dashboard JSON files (Splunk Studio exports)
├── alerts/                # Preconfigured Splunk alert SPL queries
├── spl/                   # SPL scripts for model training, applying models
├── LICENSE                # MIT License for open-source use
├── README.md              # Project overview and usage
</pre>

<hr>

<h2>🛠️ Setup Instructions</h2>
<ol>
  <li>Install Splunk Enterprise (Free Trial) and Splunk Machine Learning Toolkit (MLTK)</li>
  <li>Ingest <code>usb_logs.csv</code> and <code>vpn_logs.csv</code> to indexes (e.g., <code>splunk_guard</code> and <code>vpn</code>)</li>
  <li>Use provided SPL to extract fields and train models</li>
  <li>Deploy dashboards from <code>dashboards/</code></li>
  <li>Configure alerts using provided queries</li>
</ol>

<hr>

<h2>📊 Example Dashboards</h2>
<ul>
  <li>🔌 USB Anomalies Table & Line Chart</li>
  <li>🌍 VPN Login Outlier Detection with Geo-Distance</li>
  <li>📈 User/Device Activity Trends</li>
</ul>

<hr>

<h2>💡 Real-World Use Cases</h2>
<ul>
  <li>Insider Threat Detection via abnormal USB activity</li>
  <li>Credential Compromise Alerts on unexpected VPN usage</li>
  <li>Early Warning for suspicious data exfiltration attempts</li>
</ul>

<hr>

<h2>⚠️ Disclaimer</h2>
<p><strong>Splunk-Guard</strong> is for research, educational, and demonstration use only. It is not production-hardened. Deployments in critical environments require thorough testing and security validation.</p>

<hr>

<h2>📝 License</h2>
<p>Released under the <strong>MIT License</strong>. See <code>LICENSE</code> for details.</p>
