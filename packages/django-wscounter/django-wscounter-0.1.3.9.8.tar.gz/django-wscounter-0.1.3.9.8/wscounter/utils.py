from datetime import datetime


def get_model(model_name):
    try:
        from django.apps import apps
        return apps.get_model(model_name)
    except ImportError:
        from django.db.models.loading import get_model
        return get_model(model_name)


def is_date_valid(date_text):
    try:
        datetime.strptime(date_text, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def get_date_from_string(date_text):
    return datetime.strptime(date_text, "%d/%m/%Y")
