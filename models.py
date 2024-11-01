from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Tenant(Base):
    __tablename__ = 'Tenant'
    tenant_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15))
    email = Column(String(100))

class Owner(Base):
    __tablename__ = 'Owner'
    owner_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15))
    email = Column(String(100))

class Property(Base):
    __tablename__ = 'Property'
    property_id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(255), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    owner_id = Column(Integer, ForeignKey('Owner.owner_id'))
    owner = relationship("Owner")

class PropertyType(Base):
    __tablename__ = 'PropertyType'
    type_id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String(50), nullable=False)

class PropertyTypeList(Base):
    __tablename__ = 'PropertyTypeList'
    property_id = Column(Integer, ForeignKey('Property.property_id'), primary_key=True)
    type_id = Column(Integer, ForeignKey('PropertyType.type_id'), primary_key=True)

class LeaseContract(Base):
    __tablename__ = 'LeaseContract'
    contract_id = Column(Integer, primary_key=True, autoincrement=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    property_id = Column(Integer, ForeignKey('Property.property_id'))
    owner_id = Column(Integer, ForeignKey('Owner.owner_id'))
    tenant_id = Column(Integer, ForeignKey('Tenant.tenant_id'))

class Payments(Base):
    __tablename__ = 'Payments'
    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey('LeaseContract.contract_id'))
    date = Column(Date, nullable=False)
    is_paid = Column(Boolean)

class Reporting(Base):
    __tablename__ = 'Reporting'
    report_id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey('Property.property_id'))
    quarter = Column(String(10), nullable=False)
    contract_count = Column(Integer)
    total_income = Column(DECIMAL(10, 2))
    debt = Column(DECIMAL(10, 2))


engine = create_engine('mysql+pymysql://root:qwerty@localhost/SysTestREMS')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
