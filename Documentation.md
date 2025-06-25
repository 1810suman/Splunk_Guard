<!DOCTYPE html>
<html>
<body>

<h1>🔐 Splunk-Guard: Lightweight Anomaly Detection for USB & VPN Events</h1>

<h2>📌 Problem Statement</h2>
<p>Modern organizations face growing risks from insider threats, USB data theft, and unauthorized VPN access. Enterprise security tools are often expensive or complex, leaving smaller teams vulnerable without affordable alternatives.</p>

<h2>🎯 Solution Overview</h2>
<p><strong>Splunk-Guard</strong> provides a lightweight, easy-to-use dashboard leveraging Splunk's free version and Machine Learning Toolkit (MLTK) for:</p>
<ul>
    <li>✅ Detecting unusual USB write activity (potential data exfiltration)</li>
    <li>✅ Identifying VPN logins from distant or suspicious locations (potential credential misuse)</li>
    <li>✅ Visual dashboards and downloadable anomaly reports</li>
</ul>

<h2>👤 Target Users</h2>
<ul>
    <li>Small to mid-sized businesses</li>
    <li>Security teams with limited resources</li>
    <li>IT administrators monitoring insider threats</li>
    <li>Educational institutions demonstrating security use-cases</li>
</ul>

<h2>🔗 How It Works with Splunk</h2>
<ul>
    <li><strong>Data Ingestion:</strong> Simulated or real USB and VPN logs are indexed into Splunk.</li>
    <li><strong>Feature Extraction:</strong> Fields such as <code>device_id</code>, <code>bytes_written</code>, <code>username</code>, and <code>geo_distance_from_home</code> are extracted using SPL queries.</li>
    <li><strong>Anomaly Detection:</strong> Statistical outliers are detected using MLTK models (e.g., DensityFunction).</li>
    <li><strong>Visualization & Alerts:</strong> Dashboards highlight anomalies with charts, tables, and real-time alerts.</li>
</ul>

<h2>💡 Key Benefits</h2>
<ul>
    <li>No paid Splunk license required for core functionality</li>
    <li>Minimal setup, works on basic infrastructure</li>
    <li>Easily extendable for other log sources</li>
    <li>Supports real-time monitoring and offline demo modes</li>
</ul>

<h2>🛠️ Deployment Options</h2>
<ul>
    <li><strong>Live Mode:</strong> Connects to your Splunk instance via REST API</li>
    <li><strong>CSV Upload:</strong> Allows manual upload of USB or VPN log files</li>
    <li><strong>Demo Mode:</strong> Uses built-in synthetic data for demos and offline testing</li>
</ul>

<h2>🚀 Steps to Use the Application</h2>
<ol>
    <li>Open the Streamlit app using the provided web link</li>
    <li>Select the desired <strong>Data Type</strong> (USB Data or VPN Data) from the sidebar</li>
    <li>Choose your <strong>Data Source</strong>: Live Splunk, CSV Upload, or Demo Mode</li>
    <li>Interactive visualizations and anomaly reports will load automatically</li>
</ol>

<h2>📂 Project Structure</h2>
<ul>
    <li><code>app.py</code> - Main Streamlit application file</li>
    <li><code>data/</code> - Sample datasets for Demo Mode</li>
    <li><code>Splunk_Guard/</code> - Example SPL queries for Splunk</li>
    <li><code>alerts/</code> - Optional preconfigured alerts for Splunk (Live mode)</li>
    <li><code>requirements.txt</code> - Requirements of the project</li>
    <li><code>demos_app.py</code> - Demo for Splunk</li>
</ul>

<h2>⚠️ Notes</h2>
<ul>
    <li>Ensure valid Splunk credentials are configured in <code>secrets.toml</code> for Live mode</li>
    <li>Demo Mode works entirely offline with synthetic data for evaluations</li>
    <li>Sample data can be downloaded from this repo only</li>
    <li>This tool is intended for demonstration and educational purposes only</li>
</ul>

<h2>📊 Features Summary</h2>
<ul>
    <li>USB Data: Visualizes write volume trends, detects anomalies based on high activity</li>
    <li>VPN Data: Displays login distribution by country and user, flags geographic anomalies</li>
    <li>Downloadable CSV reports for detected anomalies</li>
</ul>

<hr>
<p><strong>Splunk-Guard</strong> - Demonstrating accessible security monitoring for all teams.</p>

</body>
</html>
