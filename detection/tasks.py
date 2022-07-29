from men_at_work.celery import app
from detection.detection_files.run_detection import PotholeDetection
from .models import DetectionTable


@app.task(bind=True)
def run_detection(self, ident):
    table = DetectionTable.objects.filter(id=ident).first()
    d = PotholeDetection(
        'detection/model/yolov4-pothole.weights',
        'detection/model/yolov4-pothole.cfg',
        'detection/model/obj.names',
        416,
        table,
    )

    try:
        d.run()
    except:
        table.return_error = True
