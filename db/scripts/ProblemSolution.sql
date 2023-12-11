SELECT
    l.id AS loan_id,
    l.borrower_id,
    l.date_of_release AS loan_date_of_release,
    l.term,
    l.loan_amount AS LoanAmount,
    l.downpayment,
    b.state,
    b.city,
    b.zip_code AS zipcode,
    l.payment_frequency,
    l.maturity_date,
    COALESCE(SUM(GREATEST(0, EXTRACT(DAY FROM AGE(CURRENT_DATE, ps.expected_payment_date)))), 0) AS current_days_past_due,
    MAX(ps.expected_payment_date) FILTER (WHERE ps.expected_payment_date <= CURRENT_DATE) AS last_due_date,
    MAX(lp.date_paid) AS last_repayment_date,
    COALESCE(SUM(ps.expected_payment_amount) FILTER (WHERE ps.expected_payment_date <= CURRENT_DATE), 0) AS amount_at_risk,
    b.credit_score AS borrower_credit_score,
    COALESCE(SUM(lp.amount_paid), 0) AS total_amount_paid,
    COALESCE(SUM(ps.expected_payment_amount), 0) AS total_amount_expected
FROM
    loans l
JOIN
    borrowers b ON l.borrower_id = b.id
LEFT JOIN
    payment_schedule ps ON l.id = ps.loan_id
LEFT JOIN
    loan_payment lp ON l.id = lp.loan_id
GROUP BY
    l.id, l.borrower_id, l.date_of_release, l.term, l.loan_amount, l.downpayment, b.state, b.city, b.zip_code, l.payment_frequency, l.maturity_date, b.credit_score
