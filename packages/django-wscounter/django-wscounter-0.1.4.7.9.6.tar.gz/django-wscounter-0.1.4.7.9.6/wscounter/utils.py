def get_model(model_name):
    try:
        try:
            from django.apps import apps
            return apps.get_model(model_name)
        except ImportError:
            from django.db.models.loading import get_model
            return get_model(model_name)
    except LookupError:
        return None
