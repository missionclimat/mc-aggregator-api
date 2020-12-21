from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

import os

from api.serializers import WorkshopSerializer, ResultSerializer
from api.models import Workshop, Result
from django_filters.rest_framework import DjangoFilterBackend

# For the documentation
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from drf_yasg import openapi

# This param is added in the schema through the decorator (using drf_yasg)
admin_code_param = openapi.Parameter(
    'admin_code', openapi.IN_QUERY, description="The admin_code (found in the workshop object) is required to delete results or workshops", type=openapi.TYPE_STRING)


class WorkshopViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Workshop to be viewed or edited.
    """

    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['workshop_name', 'admin_email', 'admin_name']
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Upon workshop creation, send an email to the workshop's admin with confirmation and access detail
        """
        serializer.save()
        context = {"workshop_name": serializer.data["workshop_name"], "visualize_result_url": "https://lysed.mission.climat.io/{}".format(
            serializer.data["id"]), "workshop_code": serializer.data["workshop_code"], "admin_code": serializer.data["admin_code"]}
        html_message = render_to_string('workshop_confirm_email.html', context)
        plain_message = strip_tags(html_message)

        send_mail(
            'Votre atelier {} a bien été créé'.format(
                serializer.data["workshop_name"]),
            plain_message,
            os.environ.get("EMAIL_HOST_USER", 'mission-climat'),
            [serializer.data["admin_email"]],
            fail_silently=True,
        )

    # Add the admin_code param to the schema
    @swagger_auto_schema(manual_parameters=[admin_code_param])
    def destroy(self, request, pk=None):
        """
        Destroy the object only if the admin_code is found in the request
        """

        instance = self.get_object()

        if request.query_params.get('admin_code') == str(instance.admin_code):
            self.perform_destroy(instance)
            return Response(data={"detail": "Result deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response(data={"detail": "the admin_code is missing or wrong"}, status=status.HTTP_401_UNAUTHORIZED)


class ResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Results to be viewed or edited.
    """

    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["workshop_code"]

    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Upon result creation, an email is send to the user posting the results (optional)
        """

        serializer.save()
        if serializer.data["user_email"] != None:
            workshop = Workshop.objects.get(workshop_code=serializer.data["workshop_code"])
            print(workshop)
            context = {"workshop_name": workshop.workshop_name}
            html_message = render_to_string(
                'result_confirm_email.html', context)
            plain_message = strip_tags(html_message)
            send_mail(
                'Confirmation des Résultats',
                plain_message,
                os.environ.get("EMAIL_HOST_USER", 'mission-climat'),
                [serializer.data["user_email"]],
                fail_silently=True,
            )

    # Add the admin_code param to the schema
    @swagger_auto_schema(manual_parameters=[admin_code_param])
    def destroy(self, request, pk=None):
        """
        Destroy the object only if the admin_code is found in the request        
        """

        instance = self.get_object()

        if request.query_params.get('admin_code') == str(instance.workshop.admin_code):
            self.perform_destroy(instance)
            return Response(data={"detail": "Result deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response(data={"detail": "the admin_code is missing or wrong"}, status=status.HTTP_401_UNAUTHORIZED)
