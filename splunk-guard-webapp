import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from requests.auth import HTTPBasicAuth

# ---- SPLUNK CONFIGURATION ----
SPLUNK_HOST = st.secrets["splunk_host"]   
USERNAME = st.secrets["splunk_username"]
PASSWORD = st.secrets["splunk_password"]

# Disable SSL Warnings for self-signed certs
requests.packages.urllib3.disable_warnings()

# ---- Function to Query Splunk REST API ----
def splunk_search(query):
    search_url = f"{SPLUNK_HOST}/services/search/jobs"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {"search": f"search {query}", "exec_mode": "blocking", "output_mode": "json"}

    response = requests.post(search_url, auth=HTTPBasicAuth(USERNAME, PASSWORD),
                             headers=headers, data=payload, verify=False)
    
    if response.status_code != 201:
        st.error(f"Search failed: {response.text}")
        return pd.DataFrame()

    sid = response.json().get("sid")
    results_url = f"{SPLUNK_HOST}/services/search/jobs/{sid}/results?output_mode=json"
    
    result = requests.get(results_url, auth=HTTPBasicAuth(USERNAME, PASSWORD), verify=False)
    
    if result.status_code != 200:
        st.error("Failed to fetch results.")
        return pd.DataFrame()

    rows = result.json().get("results", [])
    return pd.DataFrame(rows)

# ---- Streamlit UI ----
st.set_page_config(page_title="Splunk-Guard Threat Monitor", layout="wide")
st.title("🔐 Splunk-Guard: Real-Time Threat Monitoring")

# ---- Sidebar ----
st.sidebar.header("Data Type Selection")
data_choice = st.sidebar.radio("View Data for:", ["USB Logs", "VPN Logs"])

# ---- USB Section ----
if data_choice == "USB Logs":
    st.header("📊 USB Write Volume Over Time")
    usb_data = splunk_search(
        r'index=splunk_guard sourcetype=usb_logs '
        r'| rex field=_raw "^(?<device_id>[^,]+),(?<bytes_written>\d+),(?<timestamp>.+)$" '
        r'| eval bytes_written=tonumber(bytes_written) '
        r'| timechart span=1h sum(bytes_written) as total_written'
    )

    if not usb_data.empty:
        usb_data["time"] = pd.to_datetime(usb_data["_time"])
        fig = px.line(usb_data, x="time", y="total_written",
                      title="USB Write Volume (Hourly)", markers=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No USB data available or query returned no results.")

# ---- VPN Section ----
elif data_choice == "VPN Logs":
    st.header("🌍 VPN Logins Overview")

    vpn_country = splunk_search(r'index=vpn sourcetype=vpn | stats count by country')
    if not vpn_country.empty:
        fig = px.pie(vpn_country, names='country', values='count', title="VPN Logins by Country")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No VPN country data available.")

    st.subheader("👤 VPN Logins by Username")
    vpn_user = splunk_search(r'index=vpn sourcetype=vpn | stats count by username')
    if not vpn_user.empty:
        fig = px.bar(vpn_user, x='username', y='count', color='count',
                     title="VPN Logins by User")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No VPN login data available.")

st.info("⚡ Powered by Splunk REST API | Real-time Threat Visibility")

