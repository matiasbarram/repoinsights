from github_service.config import GHGetToken
import pika
import sys
import os
from main import extract_all_info


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    extract_all_info(body.decode("utf-8"))


def main():
    credentials = pika.PlainCredentials("user", "password")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", credentials=credentials)
    )
    channel = connection.channel()
    queue_name = "projects_test"
    channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
