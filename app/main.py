from fastapi import FastAPI
from app.api.routers import router as organization_router

app = FastAPI()
app.include_router(organization_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
