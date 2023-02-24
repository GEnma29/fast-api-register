from app.routes.user_routes import user_register_api_router
from fastapi import FastAPI


app = FastAPI()
# add routers to main
app.include_router(user_register_api_router)


@app.get("/")
async def root():
    return {"status": "welcome to first fast api login"}
