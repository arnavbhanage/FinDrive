def calculate_emi(
        car_price,
    down_payment,
    interest_rate,
    tenure_years
):
    loan_amount = car_price - down_payment
    monthly_interest_rate = interest_rate / (12 * 100)
    tenure_months = tenure_years * 12

    if monthly_interest_rate == 0:
        emi = loan_amount / tenure_months
    else:
        emi = loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** tenure_months / ((1 + monthly_interest_rate) ** tenure_months - 1)

    return emi
