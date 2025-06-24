# Alert SPL Examples

**USB Anomaly Alert:**
```spl
index=splunk_guard sourcetype=usb_logs
| rex field=_raw "^(?<device_id>[^,]+),(?<bytes_written>\d+),(?<timestamp>.+)$"
| eval bytes_written=tonumber(bytes_written)
| apply usb_anomaly_model
| where isOutlier=1
```

**VPN Anomaly Alert:**
```spl
index=vpn sourcetype=vpn
| fields username geo_distance_from_home
| apply vpn_anomaly_model
| where isOutlier=1
```