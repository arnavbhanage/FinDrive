import { useState } from "react";
import "./App.css";

function App() {
  const [carPrice, setCarPrice] = useState("");
  const [downPayment, setDownPayment] = useState("");
  const [interestRate, setInterestRate] = useState("");
  const [tenure, setTenure] = useState("");
  const [income, setIncome] = useState("");
setResult(data);
  const handleCalculate = () => {
    const data = {
      monthlyPayment: 500,
      totalInterest: 12000,
      totalPayment: 20000
    };
    setResult(data);
  };

  return (
    <div className="container">
      <h1>FinDrive</h1>
      <h2>Vehicle Finance Analyzer</h2>

      interestRate,
      tenure,
    });
  };

  return (
    <div className="container">
      <h1>FinDrive</h1>
      <h2>Vehicle Finance Analyzer</h2>

      <input
        type="number"
        placeholder="Vehicle Price"
        value={carPrice}
        onChange={(e) => setCarPrice(e.target.value)}
      />

      <input
        type="number"
        placeholder="Down Payment"
        value={downPayment}
        onChange={(e) => setDownPayment(e.target.value)}
      />

      <input
        type="number"
        placeholder="Interest Rate (%)"
        value={interestRate}
        onChange={(e) => setInterestRate(e.target.value)}
      />

      <input
        type="number"
        placeholder="Loan Tenure (Years)"
        value={tenure}
        onChange={(e) => setTenure(e.target.value)}
      />

      <button onClick={handleCalculate}>
        Analyze Deal
      </button>
    </div>
  );
}
{result && (
  <div>
    <h3>Results</h3>
    <p>Monthly Payment: ₹{result.monthlyPayment}</p>
    <p>Total Interest: ₹{result.totalInterest}</p>
    <p>Total Payment: ₹{result.totalPayment}</p>
  </div>
)}
export default App;

fetch(@app.route("/calculate")){
  carPrice,
  downPayment,
  interestRate,
  tenure,
  income

