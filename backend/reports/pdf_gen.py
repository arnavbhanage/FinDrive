from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Image, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from datetime import datetime
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

def create_pie_chart(data_dict, title, filename):
    """Create a pie chart and save as image"""
    fig, ax = plt.subplots(figsize=(6, 4), facecolor='white')
    colors_list = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    ax.pie(data_dict.values(), labels=data_dict.keys(), autopct='%1.1f%%',
           colors=colors_list, startangle=90, textprops={'fontsize': 10})
    ax.set_title(title, fontsize=12, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    return filename

def create_bar_chart(months, values, title, filename, ylabel="Amount (₹)"):
    """Create a bar chart and save as image"""
    fig, ax = plt.subplots(figsize=(7, 4), facecolor='white')
    bars = ax.bar(months, values, color='#4ECDC4', edgecolor='#2C9A9E', linewidth=1.5)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'₹{int(height):,}',
                ha='center', va='bottom', fontsize=9)
    
    ax.set_title(title, fontsize=12, fontweight='bold', pad=20)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.set_xlabel('Month', fontsize=10)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{int(x/1000)}K'))
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    return filename

def create_amortization_chart(monthly_payments, title, filename):
    """Create amortization schedule visualization"""
    fig, ax = plt.subplots(figsize=(7, 4), facecolor='white')
    months = list(range(1, len(monthly_payments) + 1))
    ax.plot(months, monthly_payments, marker='o', color='#FF6B6B', 
            linewidth=2, markersize=4, label='Monthly Payment')
    ax.fill_between(months, monthly_payments, alpha=0.3, color='#FF6B6B')
    
    ax.set_title(title, fontsize=12, fontweight='bold', pad=20)
    ax.set_xlabel('Month', fontsize=10)
    ax.set_ylabel('Amount (₹)', fontsize=10)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{int(x/1000)}K'))
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    return filename

def generate_pdf_report(data, filename):
    """Generate a comprehensive PDF report with charts and styling"""
    doc = SimpleDocTemplate(
        filename,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        title="FinDrive Vehicle Finance Report"
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        borderPadding=5,
        borderColor=colors.HexColor('#4ECDC4'),
        borderWidth=1,
        borderRadius=3,
        backColor=colors.HexColor('#F0F9F9')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['BodyText'],
        fontSize=10,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=6,
        leading=14
    )
    
    content = []
    
    # Header section
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("FinDrive", title_style))
    content.append(Paragraph("Vehicle Finance Analysis Report", subtitle_style))
    content.append(Spacer(1, 0.1*inch))
    content.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}", 
                             ParagraphStyle('date', parent=styles['Normal'], fontSize=9, 
                                          textColor=colors.HexColor('#95A5A6'), alignment=TA_CENTER)))
    content.append(Spacer(1, 0.3*inch))
    
    # Executive Summary Section
    content.append(Paragraph("Executive Summary", heading_style))
    
    score = data.get('score', 0)
    score_color = '#27AE60' if score >= 70 else '#F39C12' if score >= 50 else '#E74C3C'
    
    summary_text = f"""
    <b>Affordability Score:</b> <font color="{score_color}"><b>{score:.1f}/100</b></font><br/>
    <b>Monthly EMI:</b> ₹{data.get('emi', 0):,.0f}<br/>
    <b>Loan Amount:</b> ₹{data.get('loan_amount', 0):,.0f}<br/>
    <b>Down Payment:</b> ₹{data.get('down_payment', 0):,.0f}<br/>
    <b>Total Amount to Pay:</b> ₹{data.get('total_payment', 0):,.0f}<br/>
    <b>Interest Amount:</b> ₹{data.get('total_interest', 0):,.0f}
    """
    content.append(Paragraph(summary_text, normal_style))
    content.append(Spacer(1, 0.2*inch))
    
    # Financial Details Table
    content.append(Paragraph("Financial Details", heading_style))
    table_data = [
        ['Parameter', 'Value'],
        ['Vehicle Price', f"₹{data.get('car_price', 0):,.0f}"],
        ['Down Payment', f"₹{data.get('down_payment', 0):,.0f}"],
        ['Loan Amount', f"₹{data.get('loan_amount', 0):,.0f}"],
        ['Interest Rate', f"{data.get('interest_rate', 0):.2f}%"],
        ['Tenure', f"{data.get('tenure_years', 0)} Years"],
        ['Monthly EMI', f"₹{data.get('emi', 0):,.0f}"],
        ['Total Interest', f"₹{data.get('total_interest', 0):,.0f}"],
        ['Total Payment', f"₹{data.get('total_payment', 0):,.0f}"],
    ]
    
    table = Table(table_data, colWidths=[3*inch, 2.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4ECDC4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8F9F9')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9F9')]),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
    ]))
    content.append(table)
    content.append(Spacer(1, 0.2*inch))
    
    # Affordability Analysis
    content.append(Paragraph("Affordability Analysis", heading_style))
    affordability_text = f"""
    <b>Monthly Income:</b> ₹{data.get('monthly_income', 0):,.0f}<br/>
    <b>EMI to Income Ratio:</b> {data.get('emi_to_income_ratio', 0):.1f}%<br/>
    <b>Status:</b> <font color="{score_color}"><b>{data.get('affordability_status', 'Moderate')}</b></font><br/>
    <b>Assessment:</b> {data.get('affordability_note', 'Please review the finance details')}
    """
    content.append(Paragraph(affordability_text, normal_style))
    content.append(Spacer(1, 0.2*inch))
    
    # Charts section
    content.append(PageBreak())
    content.append(Paragraph("Financial Analysis Charts", heading_style))
    content.append(Spacer(1, 0.15*inch))
    
    # Cost Breakdown Pie Chart
    try:
        pie_filename = '/tmp/cost_breakdown.png'
        cost_data = {
            'Principal': data.get('loan_amount', 0),
            'Interest': data.get('total_interest', 0),
            'Down Payment': data.get('down_payment', 0)
        }
        if sum(cost_data.values()) > 0:
            create_pie_chart(cost_data, 'Total Cost Breakdown', pie_filename)
            content.append(Image(pie_filename, width=5*inch, height=3.5*inch))
            content.append(Spacer(1, 0.1*inch))
    except Exception as e:
        print(f"Error creating pie chart: {e}")
    
    # Payment Schedule
    content.append(Spacer(1, 0.2*inch))
    try:
        bar_filename = '/tmp/payment_schedule.png'
        months = ['M1', 'M6', 'M12', 'M24', 'M36', 'M60']
        payments = [data.get('emi', 0) * 1, data.get('emi', 0) * 6, 
                   data.get('emi', 0) * 12, data.get('emi', 0) * 24,
                   data.get('emi', 0) * 36, data.get('emi', 0) * 60]
        create_bar_chart(months, payments, 'Cumulative Payment Schedule', bar_filename, 'Cumulative Amount (₹)')
        content.append(Image(bar_filename, width=5.5*inch, height=3.5*inch))
    except Exception as e:
        print(f"Error creating bar chart: {e}")
    
    content.append(Spacer(1, 0.2*inch))
    
    # Pros and Cons
    content.append(PageBreak())
    content.append(Paragraph("Analysis & Recommendations", heading_style))
    
    if data.get('pros'):
        content.append(Paragraph("<b>✓ Advantages:</b>", 
                                ParagraphStyle('subheading', parent=styles['Normal'], 
                                             fontSize=11, textColor=colors.HexColor('#27AE60'),
                                             fontName='Helvetica-Bold')))
        content.append(Paragraph(data.get('pros', ''), normal_style))
        content.append(Spacer(1, 0.15*inch))
    
    if data.get('cons'):
        content.append(Paragraph("<b>✗ Considerations:</b>", 
                                ParagraphStyle('subheading', parent=styles['Normal'], 
                                             fontSize=11, textColor=colors.HexColor('#E74C3C'),
                                             fontName='Helvetica-Bold')))
        content.append(Paragraph(data.get('cons', ''), normal_style))
        content.append(Spacer(1, 0.15*inch))
    
    # Depreciation Information
    if 'depreciation' in data:
        content.append(Spacer(1, 0.15*inch))
        content.append(Paragraph("<b>Vehicle Depreciation:</b>", 
                                ParagraphStyle('subheading', parent=styles['Normal'], 
                                             fontSize=11, textColor=colors.HexColor('#3498DB'),
                                             fontName='Helvetica-Bold')))
        deprec_text = f"After {data.get('depreciation_years', 1)} year(s), your vehicle will be worth approximately <b>₹{data.get('depreciation', 0):,.0f}</b>"
        content.append(Paragraph(deprec_text, normal_style))
    
    # Footer
    content.append(Spacer(1, 0.4*inch))
    footer_text = """
    <i>This report is generated by FinDrive for informational purposes only. Please consult with a financial advisor 
    before making any investment decisions. The calculations are based on the provided information and may vary based on 
    actual terms and conditions offered by lenders.</i>
    """
    content.append(Paragraph(footer_text, 
                            ParagraphStyle('footer', parent=styles['Normal'], 
                                         fontSize=8, textColor=colors.HexColor('#95A5A6'),
                                         alignment=TA_CENTER, leading=10)))
    
    # Build PDF
    doc.build(content)