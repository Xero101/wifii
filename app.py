import os
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from config import Config
from database import init_db, list_aps, upsert_aps, count_aps
from kismet_client import KismetClient
from assessment import assess_password_policy, assess_ap
from report_generator import csv_report, pdf_report

app = Flask(__name__)
app.config.from_object(Config)
init_db(app.config["DATABASE_PATH"], app.config["DEMO_MODE"])

def current_aps():
    return list_aps(app.config["DATABASE_PATH"])

@app.get("/")
def overview():
    aps = current_aps()
    risks = {"high": sum(a["risk"] == "High" for a in aps), "medium": sum(a["risk"] == "Medium" for a in aps), "low": sum(a["risk"] == "Low" for a in aps)}
    return render_template("overview.html", aps=aps, risks=risks, demo=app.config["DEMO_MODE"])

@app.route("/discovery", methods=["GET", "POST"])
def discovery():
    message = None
    if request.method == "POST":
        try:
            rows = KismetClient(app.config["KISMET_URL"], app.config["KISMET_API_KEY"], app.config["KISMET_TIMEOUT"]).fetch_access_points()
            upsert_aps(app.config["DATABASE_PATH"], rows)
            message = f"Imported {len(rows)} access points from Kismet."
        except Exception as exc:
            message = f"Kismet read failed: {exc}"
    return render_template("discovery.html", aps=current_aps(), message=message, demo=app.config["DEMO_MODE"])

@app.route("/password", methods=["GET", "POST"])
def password():
    result = None
    if request.method == "POST":
        result = assess_password_policy(request.form.get("minimum_length", ""), request.form.get("require_upper") == "on", request.form.get("require_lower") == "on", request.form.get("require_number") == "on", request.form.get("require_symbol") == "on", request.form.get("require_mfa") == "on")
    return render_template("password.html", result=result)

@app.get("/ap-security")
def ap_security():
    return render_template("ap_security.html", aps=current_aps())

@app.get("/reports")
def reports():
    return render_template("reports.html", count=count_aps(app.config["DATABASE_PATH"]))

@app.get("/export.csv")
def export_csv():
    return Response(csv_report(current_aps()), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=wifi-security-report.csv"})

@app.get("/export.pdf")
def export_pdf():
    return Response(pdf_report(current_aps()), mimetype="application/pdf", headers={"Content-Disposition": "attachment; filename=wifi-security-report.pdf"})

@app.get("/health")
def health():
    return {"status": "ok", "demo": app.config["DEMO_MODE"], "aps": count_aps(app.config["DATABASE_PATH"])}

if __name__ == "__main__":
    app.run(host=app.config["FLASK_HOST"], port=app.config["FLASK_PORT"], debug=app.config["FLASK_DEBUG"])
