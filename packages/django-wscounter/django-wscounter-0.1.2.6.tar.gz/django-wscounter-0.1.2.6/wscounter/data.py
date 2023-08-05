from datetime import datetime


def get_from_to(model, date_from, date_to):
    return model.objects.filter(created__range=[date_from, date_to]).count()


def get(model):
    return model.objects.all().count()


def is_date_valid(date_text):
    try:
        datetime.strptime(date_text, "%Y/%m/%d")
    except ValueError:
        raise ValueError("Incorrect data format, should be DD/MM/YYYY")


def get_date_from_string(date_text):
    return datetime.strptime(date_text, "%Y/%m/%d")
