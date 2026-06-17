from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from services.calculator import (
    calculate_emi, deal_score, depreciation_value, pros, cons
)
from reports.pdf_gen import generate_pdf_report
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Store for temporary calculations
calculation_cache = {}

@app.route("/")
def home():
    return {"message": "FinDrive API - Vehicle Finance Analyzer"}

@app.route("/calculate", methods=["POST"])
def calculate():
    """Calculate EMI and affordability score"""
    try:
        data = request.json
        
        car_price = float(data.get('carPrice', 0))
        down_payment = float(data.get('downPayment', 0))
        interest_rate = float(data.get('interestRate', 0))
        tenure_years = float(data.get('tenure', 0))
        monthly_income = float(data.get('income', 0))
        monthly_expenses = float(data.get('monthlyExpenses', 0))
        
        if car_price <= 0 or tenure_years <= 0 or interest_rate < 0:
            return jsonify({"error": "Invalid input values"}), 400
        
        # Calculations
        loan_amount = car_price - down_payment
        emi = calculate_emi(car_price, down_payment, interest_rate, tenure_years)
        score = deal_score(car_price, down_payment, interest_rate, tenure_years, 
                          monthly_income, monthly_expenses)
        
        tenure_months = int(tenure_years * 12)
        total_payment = emi * tenure_months
        total_interest = total_payment - loan_amount
        
        # Calculate EMI to income ratio
        emi_to_income_ratio = (emi / monthly_income * 100) if monthly_income > 0 else 0
        
        # Determine affordability status
        if emi_to_income_ratio < 30:
            affordability_status = "Highly Affordable"
            affordability_note = "The EMI is very comfortable relative to your income."
        elif emi_to_income_ratio < 50:
            affordability_status = "Moderately Affordable"
            affordability_note = "The EMI is reasonable but requires careful budget management."
        else:
            affordability_status = "Stretching Budget"
            affordability_note = "The EMI may strain your finances. Consider higher down payment or longer tenure."
        
        # Get depreciation value (for 3 years)
        depreciation_years = 3
        depreciation = depreciation_value(car_price, 0, depreciation_years)
        
        # Get pros and cons
        pros_text = pros(emi, monthly_income)
        cons_text = cons(emi, monthly_income)
        
        # Prepare complete report data
        report_data = {
            'car_price': car_price,
            'down_payment': down_payment,
            'loan_amount': loan_amount,
            'interest_rate': interest_rate,
            'tenure_years': tenure_years,
            'emi': emi,
            'score': score,
            'monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
            'emi_to_income_ratio': emi_to_income_ratio,
            'total_payment': total_payment,
            'total_interest': total_interest,
            'affordability_status': affordability_status,
            'affordability_note': affordability_note,
            'depreciation': depreciation,
            'depreciation_years': depreciation_years,
            'pros': pros_text,
            'cons': cons_text,
            'calculated_at': datetime.now().isoformat()
        }
        
        # Cache the calculation
        session_id = datetime.now().timestamp()
        calculation_cache[str(session_id)] = report_data
        
        return jsonify({
            'success': True,
            'session_id': str(session_id),
            'data': report_data
        })
    
    except Exception as e:
        print(f"Error in calculate: {str(e)}")
        return jsonify({"error": f"Calculation error: {str(e)}"}), 400

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    """Generate PDF report from calculation data"""
    try:
        data = request.json
        session_id = data.get('session_id')
        
        # Get cached calculation or use provided data
        if session_id and session_id in calculation_cache:
            report_data = calculation_cache[session_id]
        else:
            report_data = data.get('data', {})
        
        if not report_data:
            return jsonify({"error": "No calculation data provided"}), 400
        
        # Generate PDF
        pdf_filename = f"/tmp/findrive_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        generate_pdf_report(report_data, pdf_filename)
        
        if not os.path.exists(pdf_filename):
            return jsonify({"error": "PDF generation failed"}), 500
        
        return send_file(
            pdf_filename,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"FinDrive_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
    
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return jsonify({"error": f"PDF generation error: {str(e)}"}), 500

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)