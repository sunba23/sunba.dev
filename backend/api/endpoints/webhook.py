from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import verify_github_signature
from core.jenkins import trigger_jenkins

router = APIRouter()

@router.post("/github-webhook/")
async def github_webhook(verified=Depends(verify_github_signature)):
    if trigger_jenkins():
        return {"message": "Webhook received and Jenkins triggered successfully."}
    raise HTTPException(status_code=500, detail="Failed to trigger Jenkins job")
