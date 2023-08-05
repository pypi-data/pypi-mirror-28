# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
import json
from django.db.models.loading import get_model
from . import data


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

        requested_data_array = json.loads(request.GET.get("models", None))
        if not requested_data_array:
            error_messages.append("An array of models have to be provided")
        else:
            for requested_data in requested_data_array:
                try:
                    model = get_model(requested_data['model'])
                    model_data = {
                        "from": None,
                        "to": None,
                        "data": None
                    }

                    try:
                        date_from = requested_data['from']
                        date_to = requested_data['to']
                    except KeyError:
                        date_from = None
                        date_to = None

                    if date_from is None or date_to is None:
                        model_data['data'] = data.get(model)
                        response_json_object['models'].append(model_data)
                        response_json_object['models'][model.__name__] = model_data
                    elif data.is_date_valid(date_from) and data.is_date_valid(date_to):
                        model_data['from'] = data.get_date_from_string(date_from)
                        model_data['to'] = data.get_date_from_string(date_to)
                        model_data['data'] = data.get_from_to(model, data.get_date_from_string(date_from),
                                                              data.get_date_from_string(date_to))
                        response_json_object['models'][model.__name__] = model_data
                    else:
                        error_messages.append(
                            "dates for model " + requested_data['model'] + " are not valid, should be DD/MM/YYYY")
                except KeyError:
                    error_messages.append(requested_data['model'] + " does not exist")

        if len(error_messages) != 0:
            response_json_object['result'] = "error"
            response_json_object['message'] = error_messages

        return Response(response_json_object)
