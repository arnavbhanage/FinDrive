from reportlab.platypus import SimpleDocTemplate, Paragraph, Flowable
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf_report(data, filename):
    # Create a PDF document
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    content: list[Flowable] = [
        Paragraph("FinDrive Vehicle Report", styles["Title"]),
        Paragraph(f"Score: {data['score']}", styles["BodyText"]),
        Paragraph(f"EMI: ₹{data['emi']}", styles["BodyText"]),
    ]

    doc.build(content)

sample = {
    "score": 82,
    "emi": 18000
}

# FIX: Pass 'sample' (data) first, then the filename
generate_pdf_report(sample, "report.pdf")

@app.route("/generate-report")
def generate_report_route():
    return send_file(
    "report.pdf",
    as_attachment=True
)