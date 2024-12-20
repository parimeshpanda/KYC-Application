import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse  
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError 

from loguru import logger
import redis  
from src.config.db import get_db
from src.routers.chat_router import chatrouter
from src.routers.user_router import user_router
from src.routers.record_router import record_router
from src.routers.user_explaination_router import explaination_router
# from src.workflows.workflow import run_workflow


@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_db()
    yield



app = FastAPI(
    title="LLM-IT",
    version="1.0",
    description="API for building projects" 
)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Set to allow any origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
@app.get("/", summary="Check server status", tags=["Default"])
def index():
    return PlainTextResponse("Server is up and running!")

@app.exception_handler(HTTPException)
async def http_exception_handler(
                            req: Request, exc: HTTPException):
    response = {
        "status": exc.status_code,
        "message": exc.detail,
        "data": None
    }
    return JSONResponse(response, status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
                            req: Request, exc: RequestValidationError):
    response = {
        "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "message": str(exc),
        "data": [{"field": error["loc"][1], "message": error["msg"]} for error in exc.errors()]
    }
    return JSONResponse(response, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

@app.exception_handler(Exception)
async def generic_exception_handler(
                            req: Request, exc: Exception):
    response = {
        "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "message": str(exc),
        "data": None
    }
    return JSONResponse(response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):  
    # Log error, rollback transaction, or take other appropriate action  
    return JSONResponse(  
        status_code=500,  
        content={"message": "Database error"},  
    )  

@app.exception_handler(redis.RedisError)  
async def redis_error_exception_handler(request, exc):  
    logger.error(f"Redis error: {exc}")  
    return JSONResponse(  
        status_code=500,  
        content={"message": "Internal Server Error. Redis error."},  
    )  
app.include_router(chatrouter) 
app.include_router(user_router)
app.include_router(record_router)
app.include_router(explaination_router)

app.add_exception_handler(Exception, generic_exception_handler)  
app.add_exception_handler(HTTPException, http_exception_handler)  
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler) 

if __name__ == "__main__":  
   
    uvicorn.run(app, host="0.0.0.0", port=8000)  



