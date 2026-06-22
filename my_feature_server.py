from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Define your data models
class FeatureRequest(BaseModel):
    user_id: str
    feature_names: list[str]

app = FastAPI(title="My Feature Server")

# Mock database or client for your feature store (e.g., Redis, Feast)
mock_feature_store = {
    "user_123": {"age": 30, "last_login": "2026-06-22", "tier": "premium"}
}

@app.get("/health")
async def health_check():
    """Verify service status."""
    return {"status": "ok"}

@app.post("/get_features")
async def get_features(request: FeatureRequest):
    """Retrieve features for a specific user."""
    user_data = mock_feature_store.get(request.user_id)
    
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Filter only requested features
    response = {f: user_data.get(f) for f in request.feature_names}
    return {"user_id": request.user_id, "features": response}

if __name__ == "__main__":
    uvicorn.run("my_feature_server:app", host="0.0.0.0", port=8000, reload=True)
