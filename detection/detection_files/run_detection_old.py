import pathlib
import threading
from datetime import timedelta
import cv2 as cv
import numpy as np
from .sort import Sort
from django.conf import settings
from detection.utils import get_location


class PotholeSave:
    def __init__(self, table, frame, count, save_img_count, time):
        self.frame = frame
        self.count = count
        self.time = time
        self.save_img_count = save_img_count
        self.table = table

    def run(self):

        save_path = str(self.table.date).replace('-', '').replace(':', '').replace(' ', '').split('+')[0]

        path = pathlib.Path(settings.MEDIA_ROOT, 'detect_objects', save_path)
        if not path.exists():
            pathlib.Path.mkdir(path)

        image = pathlib.Path(path, f'{self.save_img_count}.jpg')
        db_path = pathlib.Path('detect_objects', save_path, f'{self.save_img_count}.jpg')

        cv.imwrite(str(image), self.frame)
        location = get_location(self.time)

        self.table.pothols.create(
            url=str(db_path),
            latitude=location.latitude,
            longitude=location.longitude,
            count_img_pothole=self.count
        )


class PotholeDetection:
    def __init__(self, weights_path, cfg_path, obj_names, frame_size, data_table):
        self.tracker = None
        self.net = cv.dnn.readNetFromDarknet(cfg_path, weights_path)
        self.frameSize = frame_size
        self.data_table = data_table
        self.time_video = None
        self.save_img_count = 0
        self.object_detected = 0

        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

        with open(obj_names, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

        self.sort = Sort(max_age=30)
        self.trackerIds = np.zeros(0)
        self.is_unique = True
        self.save_img_count = 0
        self.object_detected = 0

        self.net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)

    def draw(self, frame):

        h, w = frame.shape[:2]
        blob = cv.dnn.blobFromImage(frame, 1 / 255.0, (self.frameSize, self.frameSize), swapRB=True, crop=False)

        self.net.setInput(blob)
        outputs = self.net.forward(self.output_layers)
        boxes = []
        confidences = []
        class_ids = []
        count_detection = 0

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.4:
                    box = detection[:4] * np.array([w, h, w, h])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    box = [x, y, int(width), int(height)]
                    boxes.append(box)
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indices = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        if len(indices) > 0:
            for i in range(len(indices)):
                count_detection += 1

        if count_detection > 0:
            detect = np.zeros((count_detection, 5))
            count = 0

            for i in range(len(indices)):
                b = boxes[i]

                x1 = int(b[0])
                y1 = int(b[1])
                x2 = int((b[0] + b[2]))
                y2 = int((b[1] + b[3]))

                bb = np.array([x1, y1, x2, y2, confidences[i]])
                detect[count, :] = bb[:]
                count += 1

            if len(detect) > 0:
                self.tracker = self.sort.update(detect)
                if len(self.tracker) > 0:
                    for d in self.tracker:
                        diff = np.in1d(self.trackerIds, self.tracker[:, 4])
                        self.is_unique = np.in1d(True, diff).all()
                        cv.rectangle(frame, (int(d[0]), int(d[1])), (int(d[2]), int(d[3])), (255, 0, 0), 1)

                if not self.is_unique:
                    if len(self.tracker) > 0:
                        self.trackerIds = np.append(self.trackerIds, self.tracker[:, 4])
                        self.save_img_count += 1
                        self.object_detected += len(self.tracker[:, 4])

                        save = PotholeSave(self.data_table, frame, len(self.tracker[:, 4]), self.save_img_count, self.time_video)
                        t = threading.Thread(target=save.run)
                        t.start()

    def get_time(self, milliseconds):
        seconds_t = milliseconds // 1000
        minutes_t = 0
        hours_t = 0

        if seconds_t >= 60:
            minutes_t = seconds_t // 60
            seconds_t = seconds_t % 60

        if minutes_t >= 60:
            hours_t = minutes_t // 60
            minutes_t = minutes_t % 60

        return hours_t, minutes_t, seconds_t

    def run(self):
        capture = cv.VideoCapture(self.data_table.video.path)
        count_frame = 0
        start_time = self.data_table.date - timedelta(hours=3)

        while True:
            res, frame = capture.read()

            if not res:
                break

            count_frame += 1
            if count_frame % 3 != 0:
                continue

            milliseconds = capture.get(cv.CAP_PROP_POS_MSEC)
            hours, minutes, seconds = self.get_time(milliseconds=milliseconds)
            self.time_video = start_time + timedelta(hours=hours, minutes=minutes, seconds=seconds)

            self.draw(frame)
            cv.imshow('frame', frame)

            if cv.waitKey(1) == ord('q'):
                break

        self.data_table.count_pothole = self.object_detected
        self.data_table.count_image = self.save_img_count
        self.data_table.save()

        capture.release()
        cv.destroyAllWindows()
