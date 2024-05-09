from fastapi import FastAPI
import models.books
from routes.books import router
from database import engine

models.books.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router, prefix="/book", tags=["book"])