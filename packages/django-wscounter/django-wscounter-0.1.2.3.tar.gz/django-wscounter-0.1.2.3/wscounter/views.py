# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
import register

class WSCounterAPIView(APIView):
    authentication_classes = (authentication.CSRFCheck,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        summary = {}

        for model in register.models:
            summary[model.__name__] = "ss"

        return Response(summary)