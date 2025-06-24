import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from requests.auth import HTTPBasicAuth

# --- App Config ---
st.set_page_config(page_title="Splunk-Guard", layout="wide")
st.title("🔐 Splunk-Guard: Real-Time Threat Monitoring")

# --- Mode Toggle ---
mode = st.sidebar.radio("Select Mode:", ["Demo Mode (Sample Data)", "Live Mode (Connect to Splunk)"])

# --- Demo Sample Data ---
sample_usb = pd.DataFrame({
    "time": pd.date_range(start="2024-01-01", periods=10, freq="H"),
    "total_written": [100, 300, 150, 500, 200, 800, 400, 700, 300, 900]
})

sample_vpn_country = pd.DataFrame({
    "country": ["US", "IN", "DE", "UK", "AU"],
    "count": [50, 30, 20, 15, 5]
})

sample_vpn_user = pd.DataFrame({
    "username": ["alice", "bob", "charlie", "dave"],
    "count": [10, 25, 5, 20]
})


# --- Live Splunk Query Function ---
def splunk_search(query):
    splunk_host = st.secrets["splunk_host"]
    username = st.secrets["splunk_username"]
    password = st.secrets["splunk_password"]

    url = f"{splunk_host}/services/search/jobs"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {"search": f"search {query}", "exec_mode": "blocking", "output_mode": "json"}

    try:
        resp = requests.post(url, auth=HTTPBasicAuth(username, password), headers=headers, data=payload, verify=False)
        sid = resp.json().get("sid")
        results_url = f"{splunk_host}/services/search/jobs/{sid}/results?output_mode=json"

        res = requests.get(results_url, auth=HTTPBasicAuth(username, password), verify=False)
        rows = res.json().get("results", [])
        return pd.DataFrame(rows)

    except Exception as e:
        st.error(f"Error connecting to Splunk: {e}")
        return pd.DataFrame()


# --- Data Type Selection ---
data_choice = st.sidebar.selectbox("Choose Data Type", ["USB Data", "VPN Data"])

# --- USB Section ---
if data_choice == "USB Data":
    st.header("📊 USB Write Volume Over Time")

    if mode == "Demo Mode (Sample Data)":
        fig = px.line(sample_usb, x="time", y="total_written", title="USB Write Volume Trend", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    else:
        usb_data = splunk_search(
            r'index=splunk_guard sourcetype=usb_logs '
            r'| rex field=_raw "^(?<device_id>[^,]+),(?<bytes_written>\d+),(?<timestamp>.+)$" '
            r'| eval bytes_written=tonumber(bytes_written) '
            r'| timechart span=1h sum(bytes_written) as total_written'
        )
        if not usb_data.empty:
            usb_data["time"] = pd.to_datetime(usb_data["_time"])
            fig = px.line(usb_data, x="time", y="total_written", title="USB Write Volume Trend", markers=True)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No USB data found.")

# --- VPN Section ---
if data_choice == "VPN Data":
    st.header("🌍 VPN Login Distribution by Country")

    if mode == "Demo Mode (Sample Data)":
        fig = px.pie(sample_vpn_country, names="country", values="count", title="VPN Logins by Country")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("👤 VPN Logins by Username")
        fig2 = px.bar(sample_vpn_user, x="username", y="count", color="count", title="VPN Logins by User")
        st.plotly_chart(fig2, use_container_width=True)

    else:
        vpn_country = splunk_search(r'index=vpn sourcetype=vpn | stats count by country')
        if not vpn_country.empty:
            fig = px.pie(vpn_country, names="country", values="count", title="VPN Logins by Country")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No VPN country data found.")

        st.subheader("👤 VPN Logins by Username")
        vpn_user = splunk_search(r'index=vpn sourcetype=vpn | stats count by username')
        if not vpn_user.empty:
            fig2 = px.bar(vpn_user, x="username", y="count", color="count", title="VPN Logins by User")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("No VPN user data found.")

# --- Footer ---
st.info("⚡ This dashboard works in both Demo Mode (static data) and Live Splunk Mode (requires Splunk REST API).")

