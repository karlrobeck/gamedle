import os
from fastapi import FastAPI
from pypox.compiler import Pypox
from fastapi.middleware.cors import CORSMiddleware

app: FastAPI = Pypox(os.path.dirname(__file__))()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
