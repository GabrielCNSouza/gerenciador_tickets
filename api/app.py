from fastapi import FastAPI

from api.routes.tickets_routes import router as tickets_router

app = FastAPI()

app.include_router(tickets_router)

@app.get("/health")
def health_check() -> dict:
    return {
        "status": "ok"
    }

