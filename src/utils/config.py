from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from mashumaro import DataClassDictMixin
from mashumaro.mixins.yaml import DataClassYAMLMixin


class Config:
    _instance = None

    @classmethod
    def get(cls) -> GlobalConfig:
        if cls._instance == None:
            with open("./config.yaml", "r") as stream:
                buffer = stream.read()
                cls._instance = GlobalConfig.from_yaml(buffer)

        return cls._instance


@dataclass
class GlobalConfig(DataClassYAMLMixin):
    logging: LoggingConfig
    uvicorn: UvicornConfig
    cors_middleware: CORSMiddlewareConfig
    langchain: LangchainConfig
    chromadb: ChromaConfig


@dataclass
class LoggingConfig(DataClassDictMixin):
    level: str
    path: Optional[str]
    enqueue: bool
    backtrace: bool
    diagnose: bool


@dataclass
class UvicornConfig(DataClassDictMixin):
    host: str
    port: int


@dataclass
class CORSMiddlewareConfig(DataClassDictMixin):
    allow_origins: list[str]
    allow_credentials: bool
    allow_methods: list[str]
    allow_headers: list[str]


@dataclass
class LangchainConfig(DataClassDictMixin):
    model: str


@dataclass
class ChromaConfig(DataClassDictMixin):
    host: str
    port: int
