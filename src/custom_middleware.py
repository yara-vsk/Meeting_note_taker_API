from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


async def unexpected_data_middleware(request: Request, call_next):
    content_type = request.headers.get("content-type", "")
    if request.method == 'PUT':
        if "multipart/form-data" in content_type:
            response = JSONResponse(content={"detail": "Unexpected 'multipart/form-data' body"}, status_code=400)
            return response
    response = await call_next(request)
    return response