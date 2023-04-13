import os
from dotenv import load_dotenv
from db_connector.orm_main import DBConnector

env = "prd"

if env == "local":
    load_dotenv(".env.local")
elif env == "prd":
    load_dotenv(".env.prd")

consolidada_user = os.getenv("CONSOLIDADA_USER")
consolidada_password = os.getenv("CONSOLIDADA_PASSWORD")
consolidada_database = os.getenv("CONSOLIDADA_DB")
consolidada_ip = os.getenv("CONSOLIDADA_IP")
consolidada_port = os.getenv("CONSOLIDADA_PORT")

temp_user = os.getenv("TEMP_USER")
temp_password = os.getenv("TEMP_PASSWORD")
temp_database = os.getenv("TEMP_DB")
temp_ip = os.getenv("TEMP_IP")
temp_port = os.getenv("TEMP_PORT")


db_consolidada = DBConnector(
    consolidada_user,
    consolidada_ip,
    consolidada_password,
    consolidada_port,
    consolidada_database,
)

db_temp = DBConnector(
    temp_user,
    temp_ip,
    temp_password,
    temp_port,
    temp_database,
)
