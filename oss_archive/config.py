from dotenv import dotenv_values
from typing import TypedDict


__env = dotenv_values(".env")

ENV = __env.get("ENV") or "dev"

ARCHIVE_BASE_PATH = __env.get("ARCHIVE_BASE_PATH")

JSON_META_LISTS_PATH = __env.get("JSON_META_LISTS_PATH")
JSON_LICENSES_PATH = __env.get("JSON_LICENSES_PATH")

class DatabaseConfigType(TypedDict):
    user: str
    password: str
    host: str
    port: int
    name: str
    url: str
    conn_str: str

db_port = __env.get("DB_PORT")

DB = DatabaseConfigType(
    user= __env.get("DB_USER") or "postgres",
    password= __env.get("DB_PASSWORD") or "postgres",
    host= __env.get("DB_HOST") or "localhost",
    port= int(db_port) if db_port is not None else 5432,
    name= __env.get("DB_NAME") or "oss_archive",
    url= F"postgresql://{__env.get("DB_USER")}:{__env.get("DB_PASSWORD")}@{__env.get("DB_HOST")}:{__env.get("DB_PORT")}/{__env.get("DB_NAME")}",
    conn_str=  F"host={__env.get("DB_HOST")} port={__env.get("DB_PORT")} user={__env.get("DB_USER")} dbname={__env.get("DB_NAME")} password={__env.get("DB_PASSWORD")} sslmode=disable"        
    )