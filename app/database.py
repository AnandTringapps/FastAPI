# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "mongodb://localhost:27017/fastapi"
# try:
#   engine = create_engine(DATABASE_URL)
#   print("Database connected successfull")
# except Exception as e:
#   print("Error connecting to database:", e)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
