import { useState } from "react";
import "./App.css";

function App() {
  const [carPrice, setCarPrice] = useState("");
  const [downPayment, setDownPayment] = useState("");
  const [interestRate, setInterestRate] = useState("");
  const [tenure, setTenure] = useState("");
  const [income, setIncome] = useState("");
  const [monthlyExpenses, setMonthlyExpenses] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState("");
  const [sessionId, setSessionId] = useState(null);

  const handleCalculate = async () => {
    setError("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:5000/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          carPrice: parseFloat(carPrice),
          downPayment: parseFloat(downPayment),
          interestRate: parseFloat(interestRate),
          tenure: parseFloat(tenure),
          income: parseFloat(income),
          monthlyExpenses: parseFloat(monthlyExpenses)
        })
      });

      if (!response.ok) {
        throw new Error("Calculation failed");
      }

      const data = await response.json();
      if (data.success) {
        setResult(data.data);
        setSessionId(data.session_id);
      } else {
        setError(data.error || "Calculation failed");
      }
    } catch (err) {
      setError(err.message || "Failed to calculate. Please check your inputs.");
    } finally {
      setLoading(false);
    }
  };

  const handleGeneratePDF = async () => {
    if (!sessionId || !result) {
      setError("Please calculate first");
      return;
    }

    setGenerating(true);
    setError("");

    try {
      const response = await fetch("http://localhost:5000/generate-pdf", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          session_id: sessionId,
          data: result
        })
      });

      if (!response.ok) {
        throw new Error("PDF generation failed");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `FinDrive_Report_${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError(err.message || "Failed to generate PDF");
    } finally {
      setGenerating(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 70) return "#27AE60";
    if (score >= 50) return "#F39C12";
    return "#E74C3C";
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  };

  return (
    <div className="app">
      <div className="container">
        <h1>FinDrive</h1>
        <h2>Vehicle Finance Analyzer</h2>

        <div className="input-section">
          <h3>Enter Your Details</h3>

          <input
            type="number"
            placeholder="Vehicle Price (₹)"
            value={carPrice}
            onChange={(e) => setCarPrice(e.target.value)}
            disabled={loading || generating}
          />

          <input
            type="number"
            placeholder="Down Payment (₹)"
            value={downPayment}
            onChange={(e) => setDownPayment(e.target.value)}
            disabled={loading || generating}
          />

          <input
            type="number"
            placeholder="Interest Rate (%)"
            value={interestRate}
            onChange={(e) => setInterestRate(e.target.value)}
            disabled={loading || generating}
            step="0.1"
          />

          <input
            type="number"
            placeholder="Loan Tenure (Years)"
            value={tenure}
            onChange={(e) => setTenure(e.target.value)}
            disabled={loading || generating}
            step="0.5"
          />

          <input
            type="number"
            placeholder="Monthly Income (₹)"
            value={income}
            onChange={(e) => setIncome(e.target.value)}
            disabled={loading || generating}
          />

          <input
            type="number"
            placeholder="Monthly Expenses (₹)"
            value={monthlyExpenses}
            onChange={(e) => setMonthlyExpenses(e.target.value)}
            disabled={loading || generating}
          />

          <button 
            onClick={handleCalculate}
            disabled={loading || generating}
            className="btn-primary"
          >
            {loading ? "Calculating..." : "Analyze Deal"}
          </button>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {result && (
          <div className="results-section">
            <h3>Analysis Results</h3>

            <div className="score-card">
              <h4>Affordability Score</h4>
              <p className="score" style={{ color: getScoreColor(result.score) }}>
                {result.score.toFixed(1)}/100
              </p>
              <p className="status">{result.affordability_status}</p>
            </div>

            <div className="results-grid">
              <div className="result-item">
                <label>Monthly EMI</label>
                <p className="value">{formatCurrency(result.emi)}</p>
              </div>

              <div className="result-item">
                <label>Total Interest</label>
                <p className="value">{formatCurrency(result.total_interest)}</p>
              </div>

              <div className="result-item">
                <label>Total Payment</label>
                <p className="value">{formatCurrency(result.total_payment)}</p>
              </div>

              <div className="result-item">
                <label>Loan Amount</label>
                <p className="value">{formatCurrency(result.loan_amount)}</p>
              </div>

              <div className="result-item">
                <label>EMI to Income Ratio</label>
                <p className="value">{result.emi_to_income_ratio.toFixed(1)}%</p>
              </div>

              <div className="result-item">
                <label>Vehicle Depreciation (3Y)</label>
                <p className="value">{formatCurrency(result.depreciation)}</p>
              </div>
            </div>

            {result.pros && (
              <div className="pros">
                <h4>✓ Advantages</h4>
                <p>{result.pros}</p>
              </div>
            )}

            {result.cons && (
              <div className="cons">
                <h4>✗ Considerations</h4>
                <p>{result.cons}</p>
              </div>
            )}

            <button 
              onClick={handleGeneratePDF}
              disabled={generating}
              className="btn-pdf"
            >
              {generating ? "Generating PDF..." : "📥 Download Report (PDF)"}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

