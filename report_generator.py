import csv, io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

FIELDS = ["ssid","bssid","channel","signal","encryption","wps","pmf","risk","findings","last_seen"]

def csv_report(rows):
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=FIELDS, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()

def pdf_report(rows):
    out = io.BytesIO()
    pdf = canvas.Canvas(out, pagesize=letter)
    width, height = letter
    y = height - 48
    pdf.setTitle("Wi-Fi Security Assessment")
    pdf.setFont("Helvetica-Bold", 16); pdf.drawString(40, y, "Wi-Fi Security Assessment"); y -= 28
    pdf.setFont("Helvetica", 9); pdf.drawString(40, y, f"Access points assessed: {len(rows)}"); y -= 24
    for ap in rows:
        line = f"{ap['ssid'] or '(hidden)'} | {ap['bssid']} | {ap['encryption']} | Risk: {ap['risk']}"
        pdf.drawString(40, y, line[:110]); y -= 13
        if y < 50: pdf.showPage(); y = height - 48; pdf.setFont("Helvetica", 9)
    pdf.save()
    return out.getvalue()
