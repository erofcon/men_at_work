import math
from .models import TrackerData


def get_location(date_time):
    gt_event = TrackerData.objects.filter(navigationtime__gte=date_time).order_by('navigationtime').first()
    lt_event = TrackerData.objects.filter(navigationtime__lte=date_time).order_by('-navigationtime').first()
    gt_diff = (gt_event.navigationtime - date_time).total_seconds() if gt_event else math.inf
    lt_diff = (date_time - lt_event.navigationtime).total_seconds() if lt_event else math.inf

    return gt_event if gt_diff <= lt_diff else lt_event
