from fastapi import HTTPException

async def get_query_token(token: str):
    if token != "something":
        raise HTTPException(status_code=400, details="no something token provided.")