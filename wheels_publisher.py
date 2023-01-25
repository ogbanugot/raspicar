import json
import mover
import datetime
from avenieca.utils.config import Config
from avenieca.producers.stream import Stream
from avenieca.utils.signal import Signal

CMD_STATE = {
    "w": [10, 20, 30, 40],
    "s": [50, 60, 70, 80],
    "a": [90, 100, 110, 120],
    "d": [130, 140, 150, 160],
    "b": [180, 190, 200, 210]
}

STATE_CMD = {
    "[10, 20, 30, 40]": "w",
    "[50, 60, 70, 80]": "s",
    "[90, 100, 110, 120]": "a",
    "[130, 140, 150, 160]": "d",
    "[180, 190, 200, 210]": "b"
}


def move():
    try:
        f = open("cmd.txt", "r")
        cmd = f.read().replace("\n", "")
        f.close()
        sleep_time = 0.0060
        mover.key_input(STATE_CMD[cmd], sleep_time)
        Signal["valence"] = 1
        Signal["state"] = cmd
        current_time = datetime.datetime.now()
        print("{}: signal sent {}".format(current_time, Signal))
        return Signal
    except Exception as e:
        print("Error: {}".format(e))


if __name__ == '__main__':
    f = open("config.json")
    json_config = json.load(f)
    mover.init()
    Config["bootstrap_servers"] = json_config["kafka_url"]
    Config["topic"] = json_config["wheels"]["pub_topic"]
    stream = Stream(config=Config, sync_rate=json_config["wheels"]["sync_rate"])
    stream.publish(move)

