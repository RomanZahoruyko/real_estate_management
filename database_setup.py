from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base,engine

DATABASE_URL = "mysql+pymysql://root:qwerty@localhost/SysTestREMS"

def setup_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
