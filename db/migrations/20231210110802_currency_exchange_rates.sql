-- +goose Up
CREATE TABLE currency_exchange_rates(
    id                      BIGSERIAL       PRIMARY KEY,
    timestamp               TIMESTAMPTZ     NOT NULL    DEFAULT  clock_timestamp(),
    currency_from           VARCHAR(100)    NOT NULL    DEFAULT 'USD',
    USD_to_currency_rate    DECIMAL(14, 8),
    currency_to_USD_rate    DECIMAL(14, 8),
    currency_to             VARCHAR(100)    NOT NULL
);

-- +goose Down
DROP TABLE IF EXISTS currency_exchange_rates;
