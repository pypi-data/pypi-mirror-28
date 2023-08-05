from datetime import datetime, timedelta

from cerberus import Validator
from django.core.exceptions import FieldError

schema = {
    'model': {'type': 'string', 'required': True},
    'from': {'type': 'string', 'dependencies': ['to']},
    'to': {'type': 'string', 'dependencies': ['from']},
    'includeReport': {'type': 'boolean'},
    'nowMinus': {'type': 'integer'},
    'query': {'type': 'list'}
}

validator = Validator(schema)


def get_today(model):
    try:
        return model.objects.filter(created_at__gt=datetime.now().date()).count()
    except FieldError:
        return model.objects.filter(created__gt=datetime.now().date()).count()


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

    return report


def is_date_valid(date):
    try:
        datetime.strptime(date, "%d/%m/%Y").date()
        return True
    except ValueError:
        return False
