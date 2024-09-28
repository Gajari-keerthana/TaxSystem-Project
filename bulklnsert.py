from datetime import datetime
from models import db, Company, Tax

# Sample data
data = [
    {"company": "derm", "amount": 4100.00, "payment_date": "09/26/2023", "status": "paid", "due_date":"01/15/2024"},
    {"company": "derm", "amount": 4100.00, "payment_date": "10/12/2023", "status": "paid", "due_date":"01/15/2024"},
    {"company": "tek", "amount": 15200.00, "payment_date": "06/09/2023", "status": "paid", "due_date":"06/15/2023"},
    {"company": "tek", "amount": 15200.00, "payment_date": "07/12/2023", "status": "paid", "due_date":"09/15/2023"},
    {"company": "tek", "amount": 11400.00, "payment_date": "08/11/2023", "status": "paid", "due_date":"09/15/2023"},
    {"company": "tek", "amount": 14440.00, "payment_date": "09/26/2023", "status": "paid", "due_date":"01/15/2024"},
    {"company": "tek", "amount": 15200.00, "payment_date": "10/18/2023", "status": "paid", "due_date":"01/15/2024"},
    {"company": "tek", "amount": 23520.00, "status": "unpaid", "due_date":"01/15/2024"},
    {"company": "tek", "amount": 16800.00, "status": "unpaid", "due_date":"01/15/2024"},
    {"company": "tek", "amount": 16800.00, "status": "unpaid", "due_date":"01/15/2024"},
    {"company": "tek", "amount": 16800.00, "status": "unpaid", "due_date":"01/15/2024"},
]

# Bulk insert data into Company table
companies = set(item["company"] for item in data)
company_objects = {name: Company(name=name) for name in companies}
db.session.bulk_save_objects(company_objects.values())
db.session.commit()

# Retrieve inserted companies
company_lookup = {company.name: company.id for company in Company.query.all()}

# Bulk insert data into Tax table
tax_objects = []
for item in data:
    company_id = company_lookup[item["company"]]
    amount = item["amount"]
    payment_date = datetime.strptime(item["payment_date"], "%m/%d/%Y")
    status = item["status"]
    due_date = datetime.strptime(item["due_date"], "%m/%d/%Y") if "due_date" in item else None
    tax_objects.append(Tax(company_id=company_id, amount=amount, payment_date=payment_date, status=status, due_date=due_date))

db.session.bulk_save_objects(tax_objects)
db.session.commit()

print("Data inserted successfully.")