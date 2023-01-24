import io
import json
import numpy as np
import datetime
from PIL import Image
from picamera import PiCamera
from avenieca.producers import Event
from avenieca.utils.config import Config
from avenieca.utils.signal import Signal
from avenieca.producer import Producer


def publish_to_monitor(producer, image):
    image = np.array(image)
    image = image.tolist()
    image = json.dumps(image)
    data = {"img": image}
    producer.send(data)


if __name__ == '__main__':
    stream = io.BytesIO()
    f = open("config.json")
    json_config = json.load(f)
    Config["bootstrap_servers"] = json_config["bootstrap_servers"]
    Config["topic"] = json_config["picam"]["topic"]
    event = Event(Config)
    Config["topic"] = "monitor"
    client = Producer(Config)
    with picamera.PiCamera() as camera:
        resolution = json_config["picam"]["resolution"]
        camera.resolution = (resolution[0], resolution[1])
        camera.framerate = json_config["picam"]["framerate"]
        for frame in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
            img = Image.frombuffer('RGB', (resolution[0], resolution[1]), stream.getvalue())
            publish_to_monitor(client, img)
            img = np.array(img, dtype=np.float64)
            img = img.flatten()
            Signal["valence"] = 1
            Signal["state"] = img
            event.publish(Signal)
            current_time = datetime.datetime.now()
            print("{}: signal sent".format(current_time))
