import io
import time
import json
import datetime
import numpy as np
import picamera
import picamera.array
from PIL import Image
from avenieca.utils.config import Config
from avenieca.utils.signal import Signal
from avenieca.producers.event import Event


def publish_to_monitor(client, img):
    img = np.asarray(img)
    img = img.tolist()
    img = json.dumps(img)
    client.send(img)


if __name__ == '__main__':
    stream = io.BytesIO()
    f = open("config.json")
    json_config = json.load(f)
    frame = None
    with picamera.PiCamera() as camera:
        resolution = json_config["picam"]["resolution"]
        resolution = (resolution[0], resolution[1])
        camera.resolution = resolution
        camera.framerate = json_config["picam"]["framerate"]
        Config["bootstrap_servers"] = json_config["kafka_url"]
        Config["topic"] = json_config["picam"]["topic"]
        event = Event(config=Config)
        Config["topic"] = "monitor"
        client = Event(config=Config)
        for f in camera.capture_continuous(stream, format='rgb', use_video_port=True):
            stream.truncate()
            stream.seek(0)
            time.sleep(json_config["picam"]["sync_rate"])
            img = Image.frombuffer('RGB', resolution, stream.getvalue())
            publish_to_monitor(client, img)
            img = np.asarray(img, dtype=np.float64)
            img = img.reshape(resolution[0] * resolution[1] * 3)
            Signal["valence"] = 1
            Signal["state"] = img
            event.publish(Signal)
            current_time = datetime.datetime.now()
            print("{}: signal sent".format(current_time))
