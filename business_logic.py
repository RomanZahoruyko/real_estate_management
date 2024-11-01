from sqlalchemy.orm import sessionmaker
from models import LeaseContract, Payments, Reporting, engine, Property
from datetime import date
from dateutil.relativedelta import relativedelta


Session = sessionmaker(bind=engine)

from datetime import datetime


def is_valid_date_range(start_date, end_date):
    return start_date < end_date


def add_lease_contract(start_date, end_date, property_id, owner_id, tenant_id, paid_month=0):
    session = Session()

    while True:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            if not is_valid_date_range(start_date, end_date):
                raise ValueError("Дата початку повинна бути меншою за дату закінчення.")
            break

        except ValueError as e:
            print(f"Помилка: {e}. Спробуйте ще раз.")
            start_date = input("Введіть дату початку (YYYY-MM-DD): ")
            end_date = input("Введіть дату закінчення (YYYY-MM-DD): ")

    new_contract = LeaseContract(start_date=start_date, end_date=end_date,
                                 property_id=property_id, owner_id=owner_id, tenant_id=tenant_id)
    session.add(new_contract)
    session.commit()

    contract_id = new_contract.contract_id
    paid_month = int(paid_month)

    duration_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

    for month in range(duration_months + 1):
        payment_date = start_date + relativedelta(months=month)

        if paid_month > 0:
            new_payment = Payments(contract_id=contract_id, date=payment_date, is_paid=1)
            paid_month -= 1
        else:
            new_payment = Payments(contract_id=contract_id, date=payment_date, is_paid=0)

        session.add(new_payment)

    session.commit()
    session.close()


def update_lease_contract(contract_id, new_start_date=None, new_end_date=None):
    session = Session()
    contract = session.get(LeaseContract, contract_id)

    if contract:
        if new_start_date:
            while True:
                try:
                    new_start_date = date.fromisoformat(new_start_date)
                    end_date = date.fromisoformat(str(contract.end_date))
                    if not is_valid_date_range(new_start_date, end_date):
                        raise ValueError("Нова дата початку повинна бути меншою за дату закінчення.")
                except ValueError as e:
                    print(f"Помилка: {e}. Спробуйте ще раз.")
                    new_start_date = input("Введіть нову дату початку (YYYY-MM-DD): ")

            contract.start_date = new_start_date

            payments = session.query(Payments).filter(Payments.contract_id == contract_id).all()
            for payment in payments:
                if payment.date < new_start_date:
                    session.delete(payment)

            duration_months = (contract.end_date.year - new_start_date.year) * 12 + (
                    contract.end_date.month - new_start_date.month)
            for month in range(duration_months + 1):
                payment_date = new_start_date + relativedelta(months=month)
                if not any(payment.date == payment_date for payment in payments):
                    new_payment = Payments(contract_id=contract_id, date=payment_date, is_paid=False)
                    session.add(new_payment)

        if new_end_date:
            while True:
                try:
                    new_end_date = date.fromisoformat(new_end_date)
                    if not is_valid_date_range(contract.start_date, new_end_date):
                        raise ValueError("Нова дата закінчення повинна бути більшою за дату початку.")
                except ValueError as e:
                    print(f"Помилка: {e}. Спробуйте ще раз.")
                    new_end_date = input("Введіть нову дату закінчення (YYYY-MM-DD): ")

            contract.end_date = new_end_date

            payments = session.query(Payments).filter(Payments.contract_id == contract_id).all()
            for payment in payments:
                if payment.date > new_end_date:
                    session.delete(payment)

            duration_months = (new_end_date.year - contract.start_date.year) * 12 + (
                    new_end_date.month - contract.start_date.month)
            for month in range(duration_months + 1):
                payment_date = contract.start_date + relativedelta(months=month)
                if not any(payment.date == payment_date for payment in payments):
                    new_payment = Payments(contract_id=contract_id, date=payment_date, is_paid=False)
                    session.add(new_payment)

        session.commit()
    session.close()


def delete_lease_contract(contract_id):
    session = Session()

    payments = session.query(Payments).filter_by(contract_id=contract_id).all()
    for payment in payments:
        session.delete(payment)

    contract = session.get(LeaseContract, contract_id)
    if contract:
        session.delete(contract)
        session.commit()
        print(f"Орендний договір з ID {contract_id} було видалено.")
    else:
        print(f"Орендний договір з ID {contract_id} не знайдено.")

    session.close()


Session = sessionmaker(bind=engine)
session = Session()


def get_quarter(date):
    if date.month in [1, 2, 3]:
        return 'Q1'
    elif date.month in [4, 5, 6]:
        return 'Q2'
    elif date.month in [7, 8, 9]:
        return 'Q3'
    else:
        return 'Q4'

def update_reporting():
    contracts = session.query(LeaseContract).all()

    reports = {}

    for contract in contracts:
        property_id = contract.property_id

        property_price = session.query(Property.price).filter(Property.property_id == property_id).scalar()
        if property_price is None:
            print(f"Не знайдено ціни за цим айді: {property_id}")
            continue

        payments = session.query(Payments).filter(Payments.contract_id == contract.contract_id).all()

        for payment in payments:
            payment_quarter = get_quarter(payment.date)

            if payment_quarter not in reports:
                reports[payment_quarter] = {
                    'total_income': 0,
                    'debt': 0,
                    'contract_count': 0,
                    'property_id': property_id
                }

            if payment.is_paid:
                reports[payment_quarter]['total_income'] += property_price
            else:
                reports[payment_quarter]['debt'] += property_price

            if reports[payment_quarter]['contract_count'] == 0:
                reports[payment_quarter]['contract_count'] = session.query(LeaseContract).filter(
                    LeaseContract.property_id == property_id
                ).count()

    for payment_quarter, data in reports.items():
        existing_report = session.query(Reporting).filter(Reporting.property_id == data['property_id'], Reporting.quarter == payment_quarter).first()
        if existing_report:
            existing_report.total_income += data['total_income']
            existing_report.debt += data['debt']
            existing_report.contract_count = data['contract_count']
            print(f"Оновлено для нерухомості за Айді: {data['property_id']} за квартал {payment_quarter}")
        else:
            new_report = Reporting(
                property_id=data['property_id'],
                total_income=data['total_income'],
                debt=data['debt'],
                contract_count=data['contract_count'],
                quarter=payment_quarter
            )
            session.add(new_report)

    session.commit()