from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.api import employees, tasks

app = FastAPI()

app.include_router(employees.router, prefix="/employees", tags=["employees"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})
