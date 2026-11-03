# Wi-Fi Security Dashboard MVP v1.0

A small Flask dashboard for authorized lab use. It reads passive access point metadata from Kismet, stores assessment records in SQLite, offers a password policy checklist (never accepts a real password), and exports PDF/CSV reports. It does not crack passwords, capture credentials, transmit probes, or perform active attacks.

## Included pages

- Overview: AP count and basic risk summary.
- Wi-Fi Discovery: read-only import from Kismet's `devices/all_devices.json` API.
- Password Assessment: evaluates policy settings only; submitted values are not stored.
- AP Security: summarizes encryption, WPS and PMF indicators from available metadata.
- Reports: download CSV or PDF.

## Raspberry Pi 5 / Kali Linux

Use Python 3.11 or newer. Install system prerequisites (package names may vary by Kali image):

```bash
sudo apt update
sudo apt install -y python3 python3-venv
unzip wifi-security-dashboard.zip
cd wifi-security-dashboard
cp .env.example .env
chmod +x run.sh
./run.sh
```

Open `http://127.0.0.1:5000`. The default binds to localhost. To access from another device on a trusted lab network, set `FLASK_HOST=0.0.0.0` in `.env` and restrict access with your firewall. Set a unique `SECRET_KEY` before use.

## Demo and Kismet modes

Demo mode is enabled by default (`DEMO_MODE=1`) and seeds illustrative AP records on first launch. To use Kismet, configure and start Kismet separately, then set `DEMO_MODE=0`, `KISMET_URL` and optionally `KISMET_API_KEY` in `.env`. Use the API key mechanism configured in your Kismet instance. Visit Wi-Fi Discovery and click **Refresh from Kismet**. The client makes only a GET request to the device listing endpoint.

SQLite is created automatically at `DATABASE_PATH` (default `wifi.db`). Back it up while the app is stopped.

## Notes and limitations

Kismet field availability depends on its version and capture source. AP security checks are heuristic indicators, not a full audit; missing WPS/PMF metadata is not proof that a feature is disabled. Findings should be verified against authorized AP configuration. The built-in Flask server is intended for a local lab MVP, not public exposure.
