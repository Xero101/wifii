import sqlite3
from assessment import assess_ap

DEMO = [
 {"ssid":"Lab-Staff","bssid":"02:11:22:33:44:50","channel":"36","signal":-48,"encryption":"WPA2-Personal","wps":False,"pmf":False},
 {"ssid":"Guest-WiFi","bssid":"02:11:22:33:44:51","channel":"6","signal":-64,"encryption":"Open","wps":False,"pmf":False},
 {"ssid":"IoT-Lab","bssid":"02:11:22:33:44:52","channel":"11","signal":-71,"encryption":"WPA2-PSK","wps":True,"pmf":False},
 {"ssid":"Secure-Lab","bssid":"02:11:22:33:44:53","channel":"149","signal":-55,"encryption":"WPA3-SAE","wps":False,"pmf":True},
]

def connect(path):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    return db

def init_db(path, demo=False):
    with connect(path) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS access_points (
            bssid TEXT PRIMARY KEY, ssid TEXT NOT NULL DEFAULT '', channel TEXT DEFAULT '',
            signal INTEGER, encryption TEXT DEFAULT 'Unknown', wps INTEGER DEFAULT 0,
            pmf INTEGER DEFAULT 0, risk TEXT DEFAULT 'Medium', findings TEXT DEFAULT '',
            last_seen TEXT DEFAULT CURRENT_TIMESTAMP)""")
        if demo and db.execute("SELECT COUNT(*) FROM access_points").fetchone()[0] == 0:
            upsert_aps(path, DEMO)

def upsert_aps(path, rows):
    with connect(path) as db:
        for ap in rows:
            evaluation = assess_ap(ap)
            db.execute("""INSERT INTO access_points(bssid,ssid,channel,signal,encryption,wps,pmf,risk,findings,last_seen)
             VALUES(?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP) ON CONFLICT(bssid) DO UPDATE SET
             ssid=excluded.ssid,channel=excluded.channel,signal=excluded.signal,encryption=excluded.encryption,
             wps=excluded.wps,pmf=excluded.pmf,risk=excluded.risk,findings=excluded.findings,last_seen=CURRENT_TIMESTAMP""",
             (ap["bssid"], ap.get("ssid",""), str(ap.get("channel","")), ap.get("signal"), ap.get("encryption","Unknown"), int(bool(ap.get("wps"))), int(bool(ap.get("pmf"))), evaluation["risk"], "; ".join(evaluation["findings"])))

def list_aps(path):
    with connect(path) as db:
        return [dict(r) for r in db.execute("SELECT * FROM access_points ORDER BY CASE risk WHEN 'High' THEN 0 WHEN 'Medium' THEN 1 ELSE 2 END, ssid")]

def count_aps(path):
    with connect(path) as db:
        return db.execute("SELECT COUNT(*) FROM access_points").fetchone()[0]
