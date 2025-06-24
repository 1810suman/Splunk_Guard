# Setup Instructions

## Requirements
- Splunk Enterprise (Free Tier acceptable)
- Splunk Machine Learning Toolkit (MLTK)
- Access to Splunk Search & Reporting and Dashboard Studio

## Setup Steps
1. **Data Upload**
   - Upload `usb_logs.csv` to `index=splunk_guard`, `sourcetype=usb_logs`.
   - Upload `vpn_logs.csv` to `index=vpn`, `sourcetype=vpn`.

2. **Field Extractions (If required)**
   - USB Logs: Extract `device_id`, `bytes_written`, `timestamp`
   - VPN Logs: Extract `username`, `geo_distance_from_home`

3. **Model Training (Run in Splunk Search)**

   **USB Anomaly Model:**
   ```spl
   index=splunk_guard sourcetype=usb_logs
   | rex field=_raw "^(?<device_id>[^,]+),(?<bytes_written>\d+),(?<timestamp>.+)$"
   | eval bytes_written=tonumber(bytes_written)
   | where isnotnull(bytes_written) AND bytes_written > 0
   | fit DensityFunction bytes_written by device_id threshold=0.01 into usb_anomaly_model
   ```

   **VPN Anomaly Model:**
   ```spl
   index=vpn sourcetype=vpn
   | fields username geo_distance_from_home
   | where isnotnull(geo_distance_from_home) AND geo_distance_from_home > 0
   | fit DensityFunction geo_distance_from_home by username threshold=0.001 into vpn_anomaly_model
   ```

4. **Anomaly Detection (Run Separately)**

   **USB Outlier Detection:**
   ```spl
   index=splunk_guard sourcetype=usb_logs
   | rex field=_raw "^(?<device_id>[^,]+),(?<bytes_written>\d+),(?<timestamp>.+)$"
   | eval bytes_written=tonumber(bytes_written)
   | apply usb_anomaly_model
   | where isOutlier=1
   | table device_id, bytes_written, timestamp
   ```

   **VPN Outlier Detection:**
   ```spl
   index=vpn sourcetype=vpn
   | fields username geo_distance_from_home
   | apply vpn_anomaly_model
   | where isOutlier=1
   | table username, geo_distance_from_home
   ```

5. **Dashboards**
   - Import JSON files from `dashboards/` via Splunk Dashboard Studio.

6. **Alerts**
   - Define alerts using SPL in `spl_queries/alert_definitions.md`.
