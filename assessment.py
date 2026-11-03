def assess_password_policy(minimum_length, upper, lower, number, symbol, mfa):
    findings = []
    try:
        length = int(minimum_length)
    except (TypeError, ValueError):
        length = 0
    if length < 12: findings.append("Set a minimum length of at least 12 characters.")
    if not upper: findings.append("Require or encourage uppercase characters.")
    if not lower: findings.append("Require or encourage lowercase characters.")
    if not number: findings.append("Require or encourage numbers.")
    if not symbol: findings.append("Require or encourage symbols.")
    if not mfa: findings.append("Enable multi-factor authentication where available.")
    score = max(0, 100 - 15 * sum((length < 12, not upper, not lower, not number, not symbol)) - 20 * (not mfa))
    return {"score": score, "rating": "Strong" if score >= 80 else "Needs improvement" if score >= 50 else "Weak", "findings": findings}

def assess_ap(ap):
    encryption = str(ap.get("encryption", "Unknown")).upper()
    findings = []
    if "OPEN" in encryption or encryption in ("NONE", ""): findings.append("Open network; enable WPA2-AES or WPA3.")
    elif "WEP" in encryption or "WPA1" in encryption: findings.append("Legacy encryption; migrate to WPA2-AES or WPA3.")
    elif "WPA2" in encryption: findings.append("Prefer WPA3 where clients support it; use a unique passphrase.")
    if ap.get("wps"): findings.append("Disable WPS if not required.")
    if "WPA3" in encryption and not ap.get("pmf"): findings.append("Verify Protected Management Frames (PMF).")
    if not findings: findings.append("No basic configuration concern detected from available passive metadata.")
    risk = "High" if any("Open" in f or "Legacy" in f for f in findings) else "Medium" if any("Disable" in f or "Prefer" in f or "Verify" in f for f in findings) else "Low"
    return {"risk": risk, "findings": findings}
