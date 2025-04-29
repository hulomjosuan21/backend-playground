import os
from sqlalchemy import create_engine, text, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URI")
Base = declarative_base()

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)

Base.metadata.create_all(engine)

customers = session.query(Customer).all()

print(*customers)

# Read only one
# customer = session.query(Customer).filter(Customer.id == 2).first()
# if customer:
#     print(f"Customer ID: {customer.id}, Name: {customer.name}")
# else:
#     print("Customer not found.")

# Add
# new_customer = Customer(name="John Doe")
# session.add(new_customer)
# session.commit()

# Update
# customer_to_update = session.query(Customer).filter(Customer.id == 1).first()
# if customer_to_update:
#     customer_to_update.name = "Jane Doe"
    
#     session.commit()
#     print("Customer updated successfully!")
# else:
#     print("Customer not found.")

# customer_to_delete = session.query(Customer).filter(Customer.id == 1).first()
# if customer_to_delete:
#     session.delete(customer_to_delete)
    
#     session.commit()
    
#     print("Customer deleted successfully!")
# else:
#     print("Customer not found.")


# Raw SQL Query
# result = session.execute(text("SELECT * FROM customers"))

# for row in result.fetchall():
#     print(row)

session.close()