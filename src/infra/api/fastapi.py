from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infra.api.routes.plans import router as plans_router
from src.infra.db import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize application
    create_db_and_tables()
    yield
    # Shutdown: Clean up resources if needed
    pass

app = FastAPI(title="Subscription Service API", lifespan=lifespan)

# Include routers
app.include_router(plans_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
