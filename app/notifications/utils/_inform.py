import os
import io
import pytz
import csv
import xlsxwriter
import string
from datetime import datetime, timedelta
import dateutil
from ..locales import en, jp

# IMG_PATH = ""
# header_en = list(en.HEADER.values())
# header_jp = list(jp.HEADER.values())
# header_key = list(string.ascii_uppercase)[:len(header_en)]
# col_en = dict(zip(header_en, header_key))
# col_jp = dict(zip(header_jp, header_key))


def to_csv(records, h, fout):
    # csv
    try:
        with open(fout, 'w') as f:
            write = csv.DictWriter(f, fieldnames=h)
            write.writeheader()
            for record in records:
                write.writerow(record)
        return True
    except Exception as e:
        return False

# return:
#   slot : slot name
#   site : site name
#   start time :2021-05-07T19:38:16
#   end time
#   parking period
#   photo


def _format(s, si, st, et, pp, p):
    res = {
        "slot": s,
        "site": si,
        "start time": st,
        "end time": et,
        "parking period": pp,
        "photo": p
    }
    return res


def _calculate(records):
    def g_slot(s): return [r for r in records if r["slot"] == s]
    def g_time(s): return dateutil.parser.parse(s)
    slots = list(set([r["slot"] for r in records]))
   # print("slots" ,slots)
    res = []
    for slot in slots:
        sl = []
        gl = g_slot(slot)

        #print("gl", gl)
        idx = 0
        ll = len(gl) - 1
        while idx < ll:
            if gl[idx]["event"] == "occupied":
                if gl[idx+1]["event"] == "vacancy":
                    si = gl[idx]["site"]
                    st = gl[idx]["time"]
                    et = gl[idx+1]["time"]
                    pp = str(g_time(gl[idx+1]["time"]) -
                             g_time(gl[idx]["time"]))
                    p = gl[idx]["path"]
                    res.append(_format(slot, si, st, et, pp, p))
            idx += 1
   # print(res)
    return res


def to_excel(records: list, header: list):

    records = _calculate(records)
    # print(records)
    # xlxs

    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # decor
    bold = workbook.add_format({'bold': True, 'color': 'blue'})
    text_format = workbook.add_format({'text_wrap': True})
    my_format = workbook.add_format()
    my_format.set_align('vcenter')
    worksheet.set_column('A:F', None, my_format)

    cell_width = 240
    cell_height = 240

    # worksheet.set_column('A:F', 20)
    # worksheet.set_column('G:G', cell_width)
    # worksheet.set_default_row(cell_height)
    # worksheet.set_row(0,5)

    #   A        B          C               D           E
    # Number |  Slot | Site | Start time | End time | Parking Period | Photo
    for i, h in enumerate(header):
        worksheet.write(1, i, h, bold)

    def _scale(img):
        im = Image.open(img)
        w, h = im.size
        x_scale = cell_width/w
        y_scale = cell_height/h
        fscale = {'x_scale': x_scale, 'y_scale': y_scale}
        return fscale

    nrow = 2
    for record in records:
        ncol = 0
        for k, v in record.items():
            worksheet.write(nrow, ncol, v, text_format)
            ncol += 1
        nrow += 1
    workbook.close()

    xlsx_data = output.getvalue()
    return xlsx_data
