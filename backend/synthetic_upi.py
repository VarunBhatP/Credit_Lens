from faker import Faker
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
def generate_upi_data(n=200):
    fake = Faker()
    data = []
    balance = 5000
    for _ in range(n):
        upi_id = fake.user_name() + '@' + random.choice(['okaxis', 'okhdfcbank', 'oksbi', 'okicici'])
        date = datetime.today() - timedelta(days=random.randint(0, 180))
        date = date.strftime('%Y-%m-%d')
        description = random.choice(['Grocery', 'Utilities', 'Entertainment', 'Dining', 'Travel', 'Health', 'Education','Swiggy credit', 'UPI transfer', 'Electricity bill',
                      'Mobile recharge', 'Rent payment', 'Grocery store',
                      'Zomato credit', 'ATM withdrawal'])
        amount = round(random.uniform(50, 5000), 2)
        credit_keywords = ['Swiggy credit', 'Zomato credit', 'UPI transfer']
        txn_type = 'Credit' if description in credit_keywords else 'Debit'   
        if txn_type == 'Debit' and balance - amount < 0:
            txn_type = 'Credit'
            balance += amount
        else:
            if txn_type == 'Credit':
                balance += amount
            else:
                balance -= amount
        data.append({'UPI ID': upi_id, 'Date': date, 'Description': description, 'Type': txn_type, 'Amount': amount, 'Balance': balance})

    return pd.DataFrame(data)
def generate_swiggy_partner(n=200):
    # High credit ratio, consistent small credits = good EXT_SOURCE
    return generate_upi_data(n)

def generate_low_income_user(n=200):
    # More debits, lower balance
    fake = Faker()
    data = []
    balance = 2000  # starts low
    for _ in range(n):
        upi_id = fake.user_name() + '@' + random.choice(['okaxis', 'oksbi'])
        date = datetime.today() - timedelta(days=random.randint(0, 180))
        date = date.strftime('%Y-%m-%d')
        description = random.choice(['Rent payment', 'ATM withdrawal', 'Grocery store', 'Mobile recharge'])
        amount = round(random.uniform(50, 1000), 2)
        txn_type = 'Debit'  # mostly debits
        if balance - amount < 0:
            txn_type = 'Credit'
            balance += amount
        else:
            balance -= amount
        data.append({'UPI ID': upi_id, 'Date': date, 'Description': description, 'Type': txn_type, 'Amount': amount, 'Balance': balance})
    return pd.DataFrame(data)

if __name__ == '__main__':
    # User B — Swiggy partner (good profile)
    df1 = generate_upi_data(200)
    df1.to_csv('upi_swiggy_partner.csv', index=False)
    print("Swiggy partner CSV generated")

    # User C — Low income (risky profile)
    df2 = generate_low_income_user(200)
    df2.to_csv('upi_low_income.csv', index=False)
    print("Low income CSV generated")

if __name__ == '__main__':
       df = generate_upi_data()
       df.to_csv('sample_upi.csv', index=False)
       print(df.head())