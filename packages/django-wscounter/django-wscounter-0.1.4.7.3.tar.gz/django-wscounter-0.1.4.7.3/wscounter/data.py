from datetime import datetime, timedelta

from django.core.exceptions import FieldError


def get_today(model):
    yesterday = datetime.today() - timedelta(days=1)
    try:
        return model.objects.filter(created_at__gt=yesterday)
    except FieldError:
        return model.objects.filter(created__gt=yesterday)


def get_report(model):
    report = {}
    now_minus_set = [1, 3, 7, 30]  # Days
    for now_minus in now_minus_set:
        count = 0
        try:
            count = model.objects.filter(
                created_at__range=[datetime.now().date() - timedelta(days=now_minus),
                                   datetime.now().date()]).count()
        except FieldError:
            count = model.objects.filter(
                created__range=[datetime.now().date() - timedelta(days=now_minus),
                                datetime.now().date()]).count()

        report[now_minus] = {
            "from": datetime.now().date() - timedelta(days=now_minus),
            "to": datetime.now().date(),
            "count": count,
        }