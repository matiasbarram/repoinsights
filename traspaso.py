from services.traspaso_service.queue_client import QueueClient
from services.traspaso_service.db_connector.connector import DBConnector
from services.traspaso_service.db_connector.database_handler import DatabaseHandler


def main():
    queue_client = QueueClient()
    project = queue_client.get_from_queue_curado(debug=True)
    print(project)

    db = DBConnector()
    db_handler = DatabaseHandler(db)


if __name__ == "__main__":
    main()
