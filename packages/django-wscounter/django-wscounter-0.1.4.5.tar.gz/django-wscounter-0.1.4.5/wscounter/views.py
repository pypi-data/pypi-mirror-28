# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import FieldError
from django.db.models import Q
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
import json
from . import utils as data_utils


class WSCounterAPIView(APIView):
    authentication_classes = (authentication.CSRFCheck,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        """
        :param request:
        :param format:
                    models = [
                      {
                          "model": "ModelName",
                          "from": "date",
                          "to": "date"
                      },
                      .
                      .
                      .
                    ]
        :return:
                      ModelName: {
                          "from": "date",
                          "to": "date",
                          "data": "count"
                      },
                      .
                      .
                      .
        """
        response_json_object = {
            "result": "success",
            "models": {},
            "message": None
        }

        error_messages = []
        requested_data_array = None

        try:  # Validate JSON object
            requested_data_array = json.loads(request.GET.get("models", None))
            try:  # Check if at least one model name exists
                for requested_data in requested_data_array:
                    try:  # Check if model exists
                        model = data_utils.get_model(requested_data['model'])
                        model_data = {}

                        try:  # check if report mode
                            include_report = requested_data['includeReport']
                            if include_report:
                                now_minus_set = [1, 3, 7, 30]  # Days
                                for now_minus in now_minus_set:
                                    count = 0
                                    try:
                                        count = model.objects.filter(
                                            created_at__gte=datetime.now() - timedelta(days=now_minus)).count()
                                    except FieldError:
                                        count = model.objects.filter(
                                            created__gte=datetime.now() - timedelta(days=now_minus))

                                    model_data = {
                                        "report": {
                                            now_minus: {
                                                "from": None,
                                                "to": None,
                                                "count": None,
                                            },
                                        }
                                    }

                                    model_data['report'][now_minus]['from'] = datetime.now() - timedelta(days=now_minus)
                                    model_data['report'][now_minus]['to'] = datetime.now()
                                    model_data['report'][now_minus]['count'] = count
                            else:
                                raise KeyError  # flag is false, proceed to detailed mode
                        except KeyError:
                            pass

                        queryset = model.objects.all()
                        try:  # Check if date (from to) parameters were sent
                            try:  # Check if date is valid
                                date_from = datetime.strptime(requested_data['from'], "%d/%m/%Y")
                                date_to = datetime.strptime(requested_data['to'], "%d/%m/%Y")
                                try:
                                    queryset = queryset.filter(created_at__range=[date_from, date_to])
                                except FieldError:
                                    queryset = queryset.filter(created__range=[date_from, date_to])

                                model_data['from'] = date_from
                                model_data['to'] = date_to
                            except ValueError:
                                error_messages.append(
                                    "dates for model " + requested_data[
                                        'model'] + " are not valid, should be DD/MM/YYYY")
                        except KeyError:
                            try:  # Check if timedelta
                                now_minus = requested_data['nowMinus']
                                try:
                                    queryset = queryset.filter(
                                        created_at__gte=datetime.now() - timedelta(days=now_minus))
                                except FieldError:
                                    queryset = queryset.filter(
                                        created__gte=datetime.now() - timedelta(days=now_minus))

                                model_data['from'] = datetime.now() - timedelta(days=now_minus)
                                model_data['to'] = datetime.now()
                            except KeyError:
                                pass

                        try:  # Check if custom Query
                            query = requested_data['query']

                            django_query = Q()
                            for x in query:
                                django_query.add(Q(**x), Q.AND)

                            queryset = queryset.filter(django_query)
                        except KeyError:  # No custom query
                            pass
                        except FieldError as field_error:  # Custom query error
                            error_messages.append(str(field_error))

                        model_data['data'] = queryset.count()

                        response_json_object['models'][model.__name__] = model_data

                    except (KeyError, LookupError):
                        response_json_object['models'] = {}
                        error_messages.append(requested_data['model'] + " does not exist")
            except KeyError:
                error_messages.append("At least one model name has to be provided")
        except ValueError:
            error_messages.append("Provided data is not valid")

        if len(error_messages) != 0:
            response_json_object['result'] = "error"
            response_json_object['message'] = error_messages

        return Response(response_json_object)
