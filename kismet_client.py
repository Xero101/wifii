import requests

class KismetClient:
    """Passive, read-only client for Kismet's devices/all_devices endpoint."""
    def __init__(self, base_url, api_key="", timeout=8):
        self.base_url, self.timeout = base_url.rstrip("/"), timeout
        self.session = requests.Session()
        if api_key:
            self.session.headers["KISMET"] = api_key

    def fetch_access_points(self):
        response = self.session.get(self.base_url + "/devices/all_devices.json", timeout=self.timeout)
        response.raise_for_status()
        payload = response.json()
        rows = payload.values() if isinstance(payload, dict) else payload
        result = []
        for row in rows:
            dot11 = row.get("dot11", {})
            if not dot11 and not row.get("kismet.device.base.macaddr"): continue
            encryption = row.get("kismet.device.base.crypt", "Unknown")
            ssid_data = row.get("kismet.device.base.ssid", {})
            ssid = row.get("kismet.device.base.name", "")
            if not ssid and isinstance(ssid_data, dict):
                ssid = ssid_data.get("kismet.common.ssid", "")
            result.append({
                "ssid": ssid,
                "bssid": row.get("kismet.device.base.macaddr", ""),
                "channel": row.get("kismet.device.base.channel", ""),
                "signal": row.get("kismet.device.base.signal", {}).get("kismet.common.signal.last_signal") if isinstance(row.get("kismet.device.base.signal"), dict) else None,
                "encryption": str(encryption),
                "wps": "WPS" in str(row).upper(),
                "pmf": "WPA3" in str(encryption).upper(),
            })
        return [r for r in result if r["bssid"]]
