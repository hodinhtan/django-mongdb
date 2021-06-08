from django.http import HttpResponse, Http404
from django.conf import settings
from django.shortcuts import render
from .models.report import Event
from .task import gen_csv, gen_xlsx, send_gmail
from mongoengine import Q
from datetime import datetime, timedelta
import pytz
# Create your views here.


def index(request):
    # sleepy()
    return HttpResponse(" Hello World!!")


def event(req):
    zone = pytz.timezone("Asia/Tokyo")
    n = datetime.now(zone)
    today = n - timedelta(0)
    yesterday = n - timedelta(10)
    start_date = yesterday.isoformat()
    end_date = today.isoformat()

    # pipe = (Q(event="occupied") | Q(event="vacancy")) & Q(slot__exists=True) & Q(time__gte=date_from) & Q(time__lte=date_to)
    # pipe_time = (Q(time__gte=date_from) & Q(time__lte=date_to))
    # events = Event.objects(pipe_time).order_by("time")
    print(start_date, end_date)
    raw_query = {
        "time": {"$gte": start_date, "$lt": end_date},
        "$or": [
             {"event": "occupied"},
             {"event": "vacancy"},
        ],
        "slot": {"$exists": True},
    }

    events = Event.objects(__raw__=raw_query).order_by("time")
    res = []
    for r in events:
        print(r)
        _project = r.project
        _device = r.device
        _site = r.site
        _camera = r.camera
        _event = r.event
        _time = r.time
        _slot = r.slot
        _path = r.path
        res.append(
            {
                "project": _project,
                "device": _device,
                "site": _site,
                "camera": _camera,
                "event": _event,
                "time": _time,
                "slot": _slot,
                "path": _path,
            }
        )

    # ans = gen_csv(res) # task
    header = ["slot", "site", "start time", "end time", "parking period", "photo"]
    xlsx_bin = gen_xlsx(res, header)

    response = HttpResponse(
        xlsx_bin,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = "attachment; filename=test.xlsx"

    E = {
        "subject": "device send report",
        "body": "From site device  with love",
        "sender": "parking@siliconcube.kr.co",
        "receiver": ["tan.ho@smartcube.vn"],
        "bcc": [],
        "reply_to": [],
        "file": xlsx_bin,
        "file_name": "report today",
        "type": "application/vnd.ms-excel",
        "headers": {"Message-ID": "foo"},
    }
    # print(E)
    # issend = send_gmail(E)
    # return HttpResponse(f"send_email: {issend}")
    return HttpResponse(res)
