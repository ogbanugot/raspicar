import json
import datetime
from avenieca.utils.config import Config
from avenieca.consumer import Consumer


def signal(cmd):
    try:
        f = open("cmd.txt", "w")
        f.write(cmd)
        f.close()
        current_time = datetime.datetime.now()
        print("{}: signal received".format(current_time))
    except Exception as e:
        print("Error: {}".format(e))


if __name__ == '__main__':
    f = open("config.json")
    json_config = json.load(f)
    Config["bootstrap_servers"] = json_config["bootstrap_servers"]
    Config["topic"] = json_config["wheels"]["sub_topic"]
    consumer = Consumer(Config)
    consumer.consume(signal)
