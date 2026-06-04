import { useState } from "react";
import "./App.css";

function App() {
  const [carPrice, setCarPrice] = useState("");
  const [downPayment, setDownPayment] = useState("");
  const [interestRate, setInterestRate] = useState("");
  const [tenure, setTenure] = useState("");

  const handleCalculate = () => {
    console.log({
      carPrice,
      downPayment,
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

export default App;