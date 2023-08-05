# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import FieldError
from django.db.models import Q
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

        try:
            requested_data_array = json.loads(request.GET.get("models", None))
        except ValueError:
            error_messages.append("Provided data is not valid")

        if not requested_data_array:
            error_messages.append("An array of models have to be provided")
        else:
            for requested_data in requested_data_array:
                try:
                    model = data_utils.get_model(requested_data['model'])
                    model_data = {}

                    queryset = model.objects.all()

                    try:
                        date_from = data_utils.get_date_from_string(requested_data['from'])
                        date_to = data_utils.get_date_from_string(requested_data['to'])

                        if data_utils.is_date_valid(date_from) and data_utils.is_date_valid(date_to):
                            try:
                                queryset = queryset.filter(created_at__range=[date_from, date_to])
                            except FieldError:
                                queryset = queryset.filter(created__range=[date_from, date_to])

                            model_data['from'] = date_from
                            model_data['to'] = date_to
                        else:
                            error_messages.append(
                                "dates for model " + requested_data['model'] + " are not valid, should be DD/MM/YYYY")

                    except KeyError:
                        pass

                    try:  # Check if custom Query
                        query = requested_data['query']

                        django_query = Q()
                        for x in query:
                            django_query.add(Q(**x), Q.AND)

                        queryset = queryset.filter(django_query)
                    except KeyError:
                        pass

                    model_data['data'] = queryset.count()
                    response_json_object['models'][model.__name__] = model_data

                except KeyError:
                    error_messages.append(requested_data['model'] + " does not exist")

        if len(error_messages) != 0:
            response_json_object['result'] = "error"
            response_json_object['message'] = error_messages

        return Response(response_json_object)
