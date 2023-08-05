from datetime import datetime

from django.core.exceptions import FieldError
from django.db.models import Q


def get_from_to(model, date_from, date_to):
    try:
        return model.objects.filter(created_at__range=[date_from, date_to]).count()
    except FieldError:
        return model.objects.filter(created__range=[date_from, date_to]).count()


def get(model):
    return model.objects.all().count()


def get_query(model, query):
    django_query = Q()
    for x in query:
        django_query.add(Q(**x), Q.AND)

    return model.objects.filter(django_query).count()


def is_date_valid(date_text):
    try:
        datetime.strptime(date_text, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def get_date_from_string(date_text):
    return datetime.strptime(date_text, "%d/%m/%Y")
