import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import requests
from requests.auth import HTTPBasicAuth

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Splunk-Guard Hybrid Threat Dashboard", layout="wide")
st.title("🔐 Splunk-Guard: Flexible Threat Detection System")

DATA_MODE = st.sidebar.radio(
    "Choose Data Source:",
    ["Live Splunk Data", "Upload CSV Files", "Demo Mode (Sample Data)"]
)
data_choice = st.sidebar.selectbox("Choose Data Type", ["USB Data", "VPN Data"])
st.sidebar.markdown("---")

# ---------------- SAMPLE DATA ----------------
sample_usb = pd.DataFrame({
    "timestamp": pd.date_range(start="2024-01-01", periods=10, freq="H"),
    "device_id": [f"usb{i}" for i in range(10)],
    "bytes_written": [100, 300, 150, 500, 200, 800, 400, 700, 300, 900]
})

sample_vpn = pd.DataFrame({
    "username": ["alice", "bob", "charlie", "dave"],
    "ip_address": ["192.168.1.1", "10.0.0.2", "172.16.0.3", "8.8.8.8"],
    "country": ["US", "IN", "DE", "UK"],
    "latitude": [40.7, 28.6, 52.5, 51.5],
    "longitude": [-74.0, 77.2, 13.4, -0.1],
    "timestamp": pd.date_range(start="2024-01-01", periods=4, freq="H"),
    "anomaly_label": [0, 1, 0, 1],
    "geo_distance_from_home": [0, 1200, 0, 5000]
})

# ---------------- SPLUNK CONNECTION ----------------
try:
    SPLUNK_HOST = st.secrets["splunk_host"]
    USERNAME = st.secrets["splunk_username"]
    PASSWORD = st.secrets["splunk_password"]
except Exception:
    SPLUNK_HOST = "your_splunk_host"
    USERNAME = "your_username"
    PASSWORD = "your_password"

requests.packages.urllib3.disable_warnings()

# ---------------- SPLUNK FUNCTION ----------------
def splunk_search(query):
    try:
        url = f"{SPLUNK_HOST}/services/search/jobs"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {"search": f"search {query}", "exec_mode": "blocking", "output_mode": "json"}

        resp = requests.post(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), headers=headers, data=payload, verify=False)
        sid = resp.json().get("sid")
        results_url = f"{SPLUNK_HOST}/services/search/jobs/{sid}/results?output_mode=json"

        res = requests.get(results_url, auth=HTTPBasicAuth(USERNAME, PASSWORD), verify=False)
        rows = res.json().get("results", [])
        return pd.DataFrame(rows)

    except Exception as e:
        st.error(f"Error connecting to Splunk: {e}")
        return pd.DataFrame()

# ---------------- USB SECTION ----------------
if data_choice == "USB Data":
    st.header("📊 USB Write Volume & Anomaly Detection")

    usb_data = pd.DataFrame()

    if DATA_MODE == "Demo Mode (Sample Data)":
        usb_data = sample_usb.copy()

    elif DATA_MODE == "Upload CSV Files":
        file = st.file_uploader("Upload USB Logs CSV (device_id, bytes_written, timestamp)", type=["csv"])
        if file:
            usb_data = pd.read_csv(file)
            expected = {"device_id", "bytes_written", "timestamp"}
            if not expected.issubset(usb_data.columns):
                st.error("CSV must contain columns: device_id, bytes_written, timestamp.")
                usb_data = pd.DataFrame()
            else:
                usb_data["timestamp"] = pd.to_datetime(usb_data["timestamp"])
                usb_data["bytes_written"] = pd.to_numeric(usb_data["bytes_written"], errors="coerce").fillna(0)

    elif DATA_MODE == "Live Splunk Data":
        usb_data = splunk_search(
            r'index=splunk_guard sourcetype=usb_logs '
            r'| rex field=_raw "^(?<device_id>[^,]+),(?<bytes_written>\d+),(?<timestamp>.+)$" '
            r'| eval bytes_written=tonumber(bytes_written) '
            r'| table device_id, bytes_written, timestamp'
        )
        if not usb_data.empty:
            usb_data["timestamp"] = pd.to_datetime(usb_data["timestamp"])
            usb_data["bytes_written"] = pd.to_numeric(usb_data["bytes_written"], errors="coerce").fillna(0)

    if not usb_data.empty:
        fig = px.line(usb_data, x="timestamp", y="bytes_written", color="device_id", title="USB Write Volume Trend", markers=True)
        st.plotly_chart(fig, use_container_width=True)

        threshold = usb_data["bytes_written"].mean() + 2 * usb_data["bytes_written"].std()
        outliers = usb_data[usb_data["bytes_written"] > threshold]
        st.subheader(f"⚠️ Outliers Detected: {len(outliers)}")
        st.dataframe(outliers)
        if not outliers.empty:
            csv = outliers.to_csv(index=False)
            st.download_button("Download Outlier Report", csv, "usb_anomalies.csv", "text/csv")

# ---------------- VPN SECTION ----------------
if data_choice == "VPN Data":
    st.header("🌍 VPN Login Pattern & Anomaly Detection")

    vpn_data = pd.DataFrame()

    if DATA_MODE == "Demo Mode (Sample Data)":
        vpn_data = sample_vpn.copy()

    elif DATA_MODE == "Upload CSV Files":
        file = st.file_uploader(
            "Upload VPN Logs CSV (username, ip_address, country, latitude, longitude, timestamp, anomaly_label, geo_distance_from_home)", type=["csv"]
        )
        if file:
            vpn_data = pd.read_csv(file)
            expected = {"username", "ip_address", "country", "latitude", "longitude", "timestamp", "anomaly_label", "geo_distance_from_home"}
            if not expected.issubset(vpn_data.columns):
                st.error(f"CSV must contain columns: {', '.join(expected)}")
                vpn_data = pd.DataFrame()
            else:
                vpn_data["timestamp"] = pd.to_datetime(vpn_data["timestamp"])
                vpn_data["geo_distance_from_home"] = pd.to_numeric(vpn_data["geo_distance_from_home"], errors="coerce").fillna(0)
                vpn_data["anomaly_label"] = pd.to_numeric(vpn_data["anomaly_label"], errors="coerce").fillna(0)

    elif DATA_MODE == "Live Splunk Data":
        vpn_data = splunk_search(
            r'index=vpn sourcetype=vpn '
            r'| table username, ip_address, country, latitude, longitude, timestamp, anomaly_label, geo_distance_from_home'
        )
        if not vpn_data.empty:
            vpn_data["timestamp"] = pd.to_datetime(vpn_data["timestamp"])
            vpn_data["geo_distance_from_home"] = pd.to_numeric(vpn_data["geo_distance_from_home"], errors="coerce").fillna(0)
            vpn_data["anomaly_label"] = pd.to_numeric(vpn_data["anomaly_label"], errors="coerce").fillna(0)

    if not vpn_data.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("VPN Logins by Country")
            fig = px.pie(vpn_data, names="country", title="Login Distribution by Country")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("VPN Logins by Username")
            counts = vpn_data["username"].value_counts().reset_index()
            counts.columns = ["username", "count"]
            fig2 = px.bar(counts, x="username", y="count", color="count", title="Logins per User")
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("🌐 Anomaly Detection based on Geo Distance")
        fig3 = px.scatter(vpn_data, x="geo_distance_from_home", y="username", color="anomaly_label",
                          title="Geo Distance from Home vs Anomaly Label", labels={"geo_distance_from_home": "Distance (km)"})
        st.plotly_chart(fig3, use_container_width=True)

        anomalies = vpn_data[vpn_data["anomaly_label"] == 1]
        st.subheader(f"⚠️ Total Anomalies Detected: {len(anomalies)}")
        st.dataframe(anomalies)
        if not anomalies.empty:
            csv = anomalies.to_csv(index=False)
            st.download_button("Download VPN Anomaly Report", csv, "vpn_anomalies.csv", "text/csv")

# ---------------- FOOTER ----------------
st.sidebar.success("Hybrid System Ready — Choose Mode & Data Type")
