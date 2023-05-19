from fastapi import FastAPI
import crud

app = FastAPI()
app.include_router(crud.router)