from database_handler import DBConnector
from database_handler import DatabaseHandler
import pika
import json

credentials = pika.PlainCredentials("user", "password")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)
)
channel = connection.channel()
channel.queue_declare(queue="pendientes")


connector = DBConnector()
db_handler = DatabaseHandler(connector)
projects = db_handler.get_updated_projects()
for project in projects:
    project_json = json.dumps(project, default=str)
    channel.basic_publish(exchange="", routing_key="pendientes", body=project_json)
    print(
        f'Project {project["owner"]}/{project["project"]} {project["last_extraction"]} published'
    )
