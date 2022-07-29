import os, random, re
import threading
from datetime import datetime, timedelta, timezone
import time
import cv2 as cv
import numpy as np
from django.conf import settings
from .sort import Sort
from detect.utils import get_location
# from detect.thread import PotholeSave


class PotholeSave(threading.Thread):

    def __init__(self, frame, count, time_video, data_table, url, url_date, save_img_count):
        self.frame = frame
        self.count = count
        self.time_video = time_video
        self.url = url
        self.url_date = url_date
        self.save_img_count = save_img_count
        self.data_table = data_table
        threading.Thread.__init__(self)

    def run(self):

        img_name = f"{self.url}/{self.url_date}_{self.save_img_count}.jpg"
        file_name =  f"{self.url}/{self.url_date}_{self.save_img_count}.txt"
        db_img_name = f'{settings.OBJECT_DETECTED_PATH}/{self.url_date}/{self.url_date}_{self.save_img_count}.jpg'
        text_file_db = f'{settings.OBJECT_DETECTED_PATH}/{self.url_date}/{self.url_date}_{self.save_img_count}.txt'
      
        
        if not os.path.exists(self.url):
            os.mkdir(self.url)
       
        cv.imwrite(f"{img_name}", self.frame )
    
        with open(f"{file_name}",'w') as file:
            file.write('hi')
            file.close()

        location = get_location(self.time_video)
        self.data_table.pothols.create(url=db_img_name, url_txt_file=text_file_db,  latitude =location.latitude, longitude = location.longitude, count_img_pothole = self.count)
     

class Detection:
    def __init__(self, weightsPath, cfgPath, objNames, frameSize, data_table, date):

        self.net = cv.dnn.readNetFromDarknet(cfgPath,weightsPath)
        self.net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)

        # self.net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        # self.net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)

        self.frameSize = frameSize
        self.data_table = data_table
        self.date = date
        self.time_video = None
        self.save_img_count = 0
        self.object_detected = 0
        self.bl = True

        self.sort = Sort(max_age=30)
        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

        self.trackerIds = np.zeros((0))
    
        with open(objNames, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        
        self.color_list = []
        for j in range(1000):
            self.color_list.append(((int)(random.randrange(255)),(int)(random.randrange(255)),(int)(random.randrange(255))))

        
        self.url_date = self.date.replace('-','_').replace(':', '_')
        self.url = os.path.join(settings.OBJECT_DETECTED_IMG, self.url_date)

        self.pothole_db = []
        self.date_table = []
        self.file_out = os.path.join(settings.DETECTED_VIDEO_PATH, f'{self.url_date}.mp4')
        self.file_out_db = f'{settings.DETECTED_VIDEO_PATH_NAME}/{self.url_date}.mp4'

    def draw(self, frame):
        h, w = frame.shape[:2]
        blob = cv.dnn.blobFromImage(frame, 1/255.0, (self.frameSize, self.frameSize), swapRB=True, crop=False)

        self.net.setInput(blob)
        outputs = self.net.forward(self.output_layers)
        boxes = []
        confidences = []
        classIDs = []
        count_detection = 0

        tracker = []

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                if confidence > 0.5:
                    box = detection[:4] * np.array([w, h, w, h])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    box = [x, y, int(width), int(height)]
                    boxes.append(box)
                    confidences.append(float(confidence))
                    classIDs.append(classID)
        
        
        indices = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        if len(indices) > 0:
            for i in range(len(indices)):
                count_detection +=1 


        if count_detection > 0:
            detect = np.zeros((count_detection,5))
            count = 0

            for i in range(len(indices)):
                b = boxes[i]

                x1 = int(b[0])
                y1 = int(b[1])
                x2 = int((b[0] + b[2]))
                y2 = int((b[1] + b[3]))

                bb = np.array([x1,y1,x2,y2,confidences[i]])
                detect[count,:] = bb[:]
                count+=1

            if len(detect) != 0:
                tracker = self.sort.update(detect)  
                if(len(tracker)>0):
                    for d in tracker:
                        diff = np.in1d(self.trackerIds, tracker[:, 4])
                        self.bl = np.in1d(True, diff).all()
                        cv.rectangle(frame, ((int)(d[0]), (int)(d[1])), ((int)(d[2]), (int)(d[3])), (255,0,0), 1)
                       
                    
                if self.bl == False:
                    if len(tracker) > 0:
                        self.trackerIds = np.append(self.trackerIds, tracker[:, 4])
                    
                        self.save_img_count+=1
                        self.object_detected +=len(tracker[:, 4])
                        # self.img_save(frame, len(tracker))
                        PotholeSave(frame, len(tracker), self.time_video, self.data_table, self.url, self.url_date, self.save_img_count).start()
                
    
    def img_save(self, frame, count):
        
        img_name = f"{self.url}/{self.url_date}_{self.save_img_count}.jpg"
        file_name =  f"{self.url}/{self.url_date}_{self.save_img_count}.txt"
        # db_img_name = os.path.join(settings.MEDIA_ROOT, img_name).replace('\\', '/')
        db_img_name = f'{settings.OBJECT_DETECTED_PATH}/{self.url_date}/{self.url_date}_{self.save_img_count}.jpg'
        text_file_db = f'{settings.OBJECT_DETECTED_PATH}/{self.url_date}/{self.url_date}_{self.save_img_count}.txt'
        # db_img_name = f"{settings.OBJECT_DETECTED_PATH}/{self.url_date}/{self.url_date}_{self.save_img_count}.jpg"
        

        if not os.path.exists(self.url):
            os.mkdir(self.url)
       
        cv.imwrite(f"{img_name}", frame )
    
        with open(f"{file_name}",'w') as file:
            file.write('hi')
            file.close()

        location = get_location(self.time_video)
        time.sleep(2)
        self.data_table.pothols.create(url=db_img_name, url_txt_file=text_file_db,  latitude =location.latitude, longitude = location.longitude, count_img_pothole = count)

      

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


    def slugify(self, text):
        pattern = r'[^\w+]'
        return re.sub(pattern, '_', str(text))


    def run(self, file):
        
        # try:
        capture = cv.VideoCapture(file)
        count_frame = 0
    
        start_time = self.date.replace('-','').replace(':','').replace('T','')
        start_time = datetime.strptime(start_time, '%Y%m%d%H%M%S').replace(tzinfo=timezone.utc)
        start_time = start_time - timedelta(hours=3)
        

        frame_width = int(capture.get(3))
        frame_height = int(capture.get(4))
        
        size = (frame_width, frame_height)

        fourcc = cv.VideoWriter_fourcc(*'H264')

        outputStream = cv.VideoWriter(self.file_out, fourcc, 30.0, size)
        
        while capture.isOpened():
            res, frame = capture.read()

            if not res:
                break
        
            count_frame+=1
            if count_frame % 3 !=0:
                continue
            
        
            milliseconds = capture.get(cv.CAP_PROP_POS_MSEC)
            hours, minutes, seconds = self.get_time(milliseconds=milliseconds)
            self.time_video = start_time + timedelta(hours=hours, minutes=minutes, seconds=seconds)
            self.draw(frame)
        
            cv.imshow('frame', frame)

            outputStream.write(frame)
            

            if cv.waitKey(1) == ord('q'):
                break
        
        
        capture.release()
        outputStream.release()
        cv.destroyAllWindows()
    
        self.data_table.count_pothole = self.object_detected
        self.data_table.count_image = self.save_img_count
        self.data_table.url = self.url
        self.data_table.send_detect = False
        self.data_table.slug = self.slugify(self.data_table.date)
        self.data_table.save()
    
        # for i in range(len(self.pothole_db)):
        #     self.data_table.pothols.create(url=self.pothole_db[i][0], url_txt_file=self.pothole_db[i][1],  latitude = self.pothole_db[i][2], 
        #                                         longitude = self.pothole_db[i][3], count_img_pothole = self.pothole_db[i][4])
        
        self.data_table.detectedfile.create(title=f"Контрольный выезд на {self.data_table.date}", file_path = self.file_out_db)

        
        
        
        # except:
        #     data_table.url = self.url
        #     data_table.send_detect = False
        #     data_table.error_processing = True
        #     data_table.save()
            
        #     for i in range(len(self.pothole_db)):   
        #         data_table.pothols.create(url=self.pothole_db[i][0], url_txt_file=self.pothole_db[i][1],  latitude = self.pothole_db[i][2], 
        #                                             longitude = self.pothole_db[i][3], count_img_pothole = self.pothole_db[i][4])

        #     data_table.detectedfile.create(title=f"Контрольный выезд на {data_table.date}", file_path = self.file_out)