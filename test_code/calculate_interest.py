def calculate_compound_interest(principal, rate, years, compounds_per_year=12):
    """
    Calculate compound interest for a loan or savings account.
    """
    if principal <= 0 or rate < 0 or years < 0:
        raise ValueError("Invalid input values")

    # Convert annual rate to decimal
    r = rate / 100

    # Compound interest formula: A = P(1 + r/n)^(nt)
    amount = principal * (1 + r / compounds_per_year) ** (compounds_per_year * years)

    interest_earned = amount - principal

    return {
        "principal": principal,
        "final_amount": round(amount, 2),
        "interest_earned": round(interest_earned, 2),
        "rate_percent": rate,
        "years": years
    }


def calculate_monthly_payment(loan_amount, annual_rate, loan_term_months):
    """
    Calculate monthly payment for a fixed-rate loan.
    Used for auto loans, personal loans, and mortgages.
    """
    monthly_rate = (annual_rate / 100) / 12

    if monthly_rate == 0:
        return loan_amount / loan_term_months

    payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** loan_term_months) / (
                (1 + monthly_rate) ** loan_term_months - 1)

    return round(payment, 2)