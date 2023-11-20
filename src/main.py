import aioredis
import uvicorn
from fastapi import FastAPI
from src.api.routers import all_routers
from src.custom_middleware import unexpected_data_middleware

app = FastAPI()

app.middleware("http")(unexpected_data_middleware)

for router in all_routers:
    app.include_router(router)


@app.on_event("startup")
async def startup():
    pass


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)