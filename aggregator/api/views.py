from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail

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
admin_code_param = openapi.Parameter('admin_code', openapi.IN_QUERY, description="The admin_code (found in the workshop object) is required to delete results or workshops", type=openapi.TYPE_STRING)

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
        print(serializer)
        print(serializer.data)
        send_mail(
            'Confirmation de création d\'atelier',
            'Pour rejoindre votre atelier',
            os.environ.get("EMAIL_HOST_USER", 'mission-climat'),
            [serializer.data["admin_email"]],
            fail_silently=False,
        )

    # Add the admin_code param to the schema
    @swagger_auto_schema(manual_parameters=[admin_code_param])
    def destroy(self, request, pk=None):
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


    # Add the admin_code param to the schema
    @swagger_auto_schema(manual_parameters=[admin_code_param])
    def destroy(self, request, pk=None):

        instance = self.get_object()

        if request.query_params.get('admin_code') == str(instance.workshop.admin_code):
            self.perform_destroy(instance)
            return Response(data={"detail": "Result deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response(data={"detail": "the admin_code is missing or wrong"}, status=status.HTTP_401_UNAUTHORIZED)