from sqlalchemy import DECIMAL
from sqlalchemy.orm import sessionmaker
from models import engine

Session = sessionmaker(bind=engine)
session = Session()

def create_record(model, **kwargs):
    new_record = model(**kwargs)
    session.add(new_record)
    session.commit()
    print(f"Successfully created {model.__name__} with ID {new_record.id}.")

def print_records(model):
    columns = model.__table__.columns
    results = session.query(*columns).all()

    formatted_results = []
    for row in results:
        formatted_row = ', '.join(
            f"{column.name}: {value:.2f}" if isinstance(value, DECIMAL) else f"{column.name}: {value}"
            for column, value in zip(columns, row)
        )
        formatted_results.append(formatted_row)

    for report in formatted_results:
        print(report)

def update_record(model, record_id, id_field, **kwargs):
    record = session.query(model).filter(getattr(model, id_field) == record_id).first()
    if record:
        for key, value in kwargs.items():
            if hasattr(record, key):
                setattr(record, key, value)
        session.commit()
        print(f"Successfully updated {model.__name__} with ID {record_id}.")
    else:
        print(f"{model.__name__} with ID {record_id} not found.")

def delete_record(model, record_id, primary_key='id', additional_deletes=None):
    record = session.query(model).filter(getattr(model, primary_key) == record_id).first()

    if record:
        if additional_deletes:
            for delete_model, filter_condition in additional_deletes:
                session.query(delete_model).filter(filter_condition).delete()

        session.delete(record)
        session.commit()
        print(f"Record with ID {record_id} deleted successfully.")
    else:
        print(f"No record found for {model.__name__} with ID: {record_id}")

def get_filtered_records(model, filter_conditions=None):
    query = session.query(model)

    if filter_conditions:
        for column_name, value in filter_conditions.items():
            column = getattr(model, column_name)
            if value is None:
                query = query.filter(column.is_(None))  # Якщо value None, фільтруємо за NULL
            else:
                query = query.filter(column == value)

    return query.all()

session.close()
