from datetime import datetime


def get_from_to(model, date_from, date_to):
    return model.objects.filter(created_at__range=[date_from, date_to]).count()


def get(model):
    return model.objects.all().count()


def is_date_valid(date_text):
    try:
        datetime.strptime(date_text, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def get_date_from_string(date_text):
    return datetime.strptime(date_text, "%d/%m/%Y")
