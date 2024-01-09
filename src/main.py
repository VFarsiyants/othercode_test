import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import v1

app = FastAPI(
    title='otherblog',
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1.router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
