import json
import datetime
from avenieca.consumer import Consumer


def move(cmd):
    try:
        f = open("cmd.txt", "w")
        f.write(cmd)
        f.close()
        current_time = datetime.datetime.now()
        print("{}: signal recieved {}".format(current_time, cmd))
    except Exception as e:
        print("Error: {}".format(e))


if __name__ == '__main__':
    f = open("config.json")
    json_config = json.load(f)
    consumer_config = {
        "bootstrap_servers": json_config["kafka_url"],
        "topic": json_config["wheels"]["sub_topic"],
        "auto_offset_reset": "latest"
    }
    consumer = Consumer(consumer_config)
    consumer.consume(move)
