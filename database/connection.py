from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:spatni@localhost:3306/hbnb_db",
    echo=False
)
