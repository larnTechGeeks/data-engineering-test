-- +goose Up
CREATE TABLE borrowers(
    id              VARCHAR(40)     PRIMARY KEY,
    state           VARCHAR(100),
    city            VARCHAR(100),
    zip_code        VARCHAR(100),
    credit_score    DECIMAL(14, 4)
);

CREATE TABLE loans(
    id                  VARCHAR(40)     PRIMARY KEY,
    borrower_id         VARCHAR(40)     NOT NULL    REFERENCES borrowers(id),
    date_of_release     DATE            NOT NULL,
    term                INTEGER         NOT NULL,
    interest_rate       DECIMAL(14, 4),
    loan_amount         DECIMAL(14, 4),
    downpayment         DECIMAL(14, 4),
    payment_frequency   DECIMAL(14, 4)  NOT NULL,
    maturity_date       DATE            NOT NULL
);

CREATE TABLE payment_schedule(
    id                      VARCHAR(40)     PRIMARY KEY,
    loan_id                 VARCHAR(40)     NOT NULL    REFERENCES loans(id),
    expected_payment_date   DATE            NOT NULL,
    expected_payment_amount DECIMAL(14, 4)         NOT NULL
);

CREATE TABLE loan_payment(
    id              VARCHAR(40)     PRIMARY KEY,
    loan_id         VARCHAR(40)     NOT NULL    REFERENCES loans(id),
    amount_paid     DECIMAL(14, 4)  NOT NULL,
    date_paid       DATE            NOT NULL
);

-- +goose Down
DROP TABLE IF EXISTS loan_payment;
DROP TABLE IF EXISTS payment_schedule;
DROP TABLE IF EXISTS loans;
DROP TABLE IF EXISTS borrowers;