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


def affordability_score(
        monthly_income,
    monthly_expenses,
    emi
):
    disposable_income = monthly_income - monthly_expenses
    if disposable_income <= 0:
        return 0

    score = (disposable_income - emi) / disposable_income * 100
    return max(0, min(score, 100))

def deal_score(
        car_price,
    down_payment,
    interest_rate,
    tenure_years,
    monthly_income,
    monthly_expenses
):
    emi = calculate_emi(car_price, down_payment, interest_rate, tenure_years)
    score = affordability_score(monthly_income, monthly_expenses, emi)
    return score



def depreciation_value(car_price, depreciation_rate, years):
    if years == 0.5:
        depreciation_rate = 0.05  # 5% for the first 6 months
    elif years == 1:
        depreciation_rate = 0.15  # 15% for the first year
    elif years == 2:
        depreciation_rate = 0.3  # 25% for the first 2 years
    elif years == 3:
        depreciation_rate = 0.4  # 40% for the first 3 years
    elif years > 3:
        depreciation_rate = 0.5  # 50% for more than 3 years


    remaining_value = car_price * (1 - depreciation_rate)
    return remaining_value

