import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from pandas import DataFrame
from pandas.tseries.offsets import MonthEnd

class EDAPipeline:
    def __init__(self, dsn: str):
        self.engine = create_engine(dsn)

    def clean_borrowers_data(self, df: DataFrame) -> DataFrame:
        df['credit_score'] = pd.to_numeric(df['credit_score'], errors='coerce').fillna(0)
        return df

    def clean_invalid_date(self, date, original_date_str):
        if pd.isna(date):
            partial_date = pd.to_datetime(original_date_str, format='%m/%d/%Y', errors='coerce')
            if pd.notna(partial_date):
                last_day = partial_date + MonthEnd(1)
                return last_day
            else:
                return "2023-02-28"
        return date
    
    def clean_loans_data(self, df: DataFrame) -> DataFrame:
        df = df.drop_duplicates()
        df = df.fillna(0)
        date_format = "%m/%d/%Y"
        df['date_of_release'] = pd.to_datetime(df['date_of_release'], format=date_format, errors='coerce')
        df['maturity_date'] = pd.to_datetime(df['maturity_date'], format=date_format, errors='coerce')
        # df['maturity_date'] = df['maturity_date'].apply(self.clean_invalid_date)
        df['maturity_date'] = df.apply(lambda row: self.clean_invalid_date(row['maturity_date'], row['maturity_date']), axis=1)
        return df
    
    def clean_repayment_data(self, df: DataFrame) -> DataFrame:
        df = df.drop_duplicates()
        df = df.fillna(0)
        date_format = "%m/%d/%Y"
        df['date_paid'] = pd.to_datetime(df['date_paid'], format=date_format, errors='coerce')
        return df
    
    def clean_schedule_data(self, df: DataFrame) -> DataFrame:
        df = df.drop_duplicates()
        df = df.fillna(0)
        date_format = "%m/%d/%Y"
        df['expected_payment_date'] = pd.to_datetime(df['expected_payment_date'], format=date_format, errors='coerce')
        return df
    

    def insert_data(self, df: DataFrame, table) -> None:
        df.to_sql(table, con=self.engine, if_exists='append', index=False)

def main(dsn: str) -> None:
    pipeline = EDAPipeline(dsn)

    cwd = os.getcwd()

    borrowers_csv = os.path.join(cwd, 'db/scripts/data', 'borrowers.csv')
    loans_csv = os.path.join(cwd, 'db/scripts/data', 'loans.csv')
    repayment_csv = os.path.join(cwd, 'db/scripts/data', 'loan_payments.csv')
    schedule_csv = os.path.join(cwd, 'db/scripts/data', 'schedules.csv')
    # Borrowers Data
    borrowers_df = pd.read_csv(borrowers_csv)
    borrowers_df.columns = ['id', 'state', 'city', 'zip_code', 'credit_score']
    borrowers_df = pipeline.clean_borrowers_data(borrowers_df)

    # Loans Data
    loans_df = pd.read_csv(loans_csv)
    loans_df.columns = ['borrower_id', 'id', 'date_of_release', 'term', 'interest_rate', 
                  'loan_amount', 'downpayment', 'payment_frequency', 'maturity_date']
    loans_df = pipeline.clean_loans_data(loans_df)

    # Repayments data
    repayments_df = pd.read_csv(repayment_csv)
    repayments_df.columns = ["loan_id", "id", "date_paid", "amount_paid"]
    repayments_df = pipeline.clean_repayment_data(repayments_df)


    # Loan Schedules
    schedule_df = pd.read_csv(schedule_csv)
    schedule_df.columns = ["loan_id", "id", "expected_payment_date", "expected_payment_amount"]
    schedule_df = pipeline.clean_schedule_data(schedule_df)

    # Saving stage
    pipeline.insert_data(borrowers_df, "borrowers")
    pipeline.insert_data(loans_df, "loans")
    pipeline.insert_data(repayments_df, "loan_payment")
    pipeline.insert_data(schedule_df, "payment_schedule")


if __name__ == "__main__":
    db_connection_string = 'postgresql://app:password@localhost:5432/test_db?sslmode=disable'
    main(db_connection_string)
