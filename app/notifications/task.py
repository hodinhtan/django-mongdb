from celery import shared_task
from time import sleep
from .utils import _inform
from django.core.mail import EmailMessage
from .models.report import Event
from mongoengine import *


@shared_task
def check():
    print("I am checking your stuff")


@shared_task
def gen_csv(arr):
    _ = _inform.to_csv(arr, list(arr[0].keys()), "test.csv")
    return _


@shared_task
def gen_xlsx(arr, header):
    _ = _inform.to_excel(arr, header)
    return _


@shared_task
def send_gmail(E):
    # try sending email
    try:
        email = EmailMessage(
            E["subject"],
            E["body"],
            E["sender"],
            E["receiver"],
            E["bcc"],
            reply_to=E["reply_to"],
            headers=E["headers"],
        )
        email.attach(E["file_name"], E["file"], E["type"])
        email.send(fail_silently=False)
        print(f'Email send to {len(E["receiver"])} users')
        return True
    except Exception as e:
        print(e)
        return False


@shared_task
def test():
    print("here we go again!")
    return "test"


@shared_task
def send_daily_report():
    pipe = (Q(event="occupied") | Q(event="vacancy")) & Q(slot__exists=True)
    events = Event.objects(pipe).order_by("time")

    res = []
    for r in events:
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

    try:
        email = EmailMessage(
            E["subject"],
            E["body"],
            E["sender"],
            E["receiver"],
            E["bcc"],
            reply_to=E["reply_to"],
            headers=E["headers"],
        )
        email.attach(E["file_name"], E["file"], E["type"])
        email.send(fail_silently=False)
        print(f'Email send to {len(E["receiver"])} users')
    except Exception as e:
        print(e)
