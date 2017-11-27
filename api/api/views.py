from __future__ import unicode_literals

from collections import OrderedDict

from django.shortcuts import render
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


class APIRootView(APIView):
    _ignore_model_permissions = True
    exclude_from_schema = True

    def get_view_name(self):
        return "API Root"

    def get(self, request, format=None):

        return Response(OrderedDict((
            ('firewalls', reverse('firewall-api:api-root', request=request, format=format)),
        )))
