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
        requested_data_array = None

        try:  # Validate JSON object
            requested_data_array = json.loads(request.GET.get("models", None))
            if requested_data_array and len(requested_data_array) > 0:
                for requested_data in requested_data_array:
                    # Validate requested data
                    if 'model' in requested_data and data_utils.get_model(
                            requested_data['model']):  # Check if model exists
                        model = data_utils.get_model(requested_data['model'])
                        model_data = {}
                        queryset = model.objects.all()

                        # Report
                        if 'includeReport' in requested_data:
                            if requested_data['includeReport']:
                                model_data = {
                                    "report": data.get_report(model)
                                }

                        # From/To Dates
                        if 'from' in requested_data and 'to' in requested_data:  # Check if date (from to) parameters were both revceived and valid
                            if data.is_date_valid(requested_data['from']) and data.is_date_valid(
                                    requested_data['to']):  # Check if date is valid
                                date_from = datetime.strptime(requested_data['from'], "%d/%m/%Y").date()
                                date_to = datetime.strptime(requested_data['to'], "%d/%m/%Y").date()
                                try:
                                    queryset = queryset.filter(created_at__range=[date_from, date_to])
                                except FieldError:
                                    queryset = queryset.filter(created__range=[date_from, date_to])

                                model_data['from'] = date_from
                                model_data['to'] = date_to
                            else:
                                error_messages.append(
                                    "dates for model " + requested_data[
                                        'model'] + " are not valid, should be DD/MM/YYYY")

                        # T- Days
                        if 'nowMinus' in requested_data:  # Check if timedelta
                            now_minus = requested_data['nowMinus']
                            try:
                                queryset = queryset.filter(
                                    created_at__gte=datetime.now().date() - timedelta(days=now_minus))
                            except FieldError:
                                queryset = queryset.filter(
                                    created__gte=datetime.now().date() - timedelta(days=now_minus))

                            model_data['from'] = datetime.now().date() - timedelta(days=now_minus)
                            model_data['to'] = datetime.now().date()

                        # Custom Query
                        if 'query' in requested_data:
                            query = requested_data['query']
                            django_query = Q()

                            try:
                                for x in query:
                                    django_query.add(Q(**x), Q.AND)

                                queryset = queryset.filter(django_query)
                            except FieldError as field_error:  # Custom query error
                                error_messages.append(str(field_error))

                        model_data['data'] = queryset.count()

                        if 'today' in requested_data:
                            model_data['today'] = data.get_today(model)

                        response_json_object['models'][model.__name__] = model_data
                    else:
                        response_json_object['models'] = {}
                        error_messages.append(requested_data['model'] + " does not exist")

            else:
                error_messages.append("At least one model name has to be provided")
        except ValueError:
            error_messages.append("Provided data is not valid")

        if len(error_messages) != 0:
            response_json_object['result'] = "error"
            response_json_object['message'] = error_messages

        return Response(response_json_object)
