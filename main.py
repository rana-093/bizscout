from fastapi import FastAPI
from routers import usage_router
app = FastAPI(title="BizScout")


app.include_router(usage_router, prefix="/api/v1", tags=["users"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
