from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, send_mass_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

import os

from api.serializers import WorkshopSerializer, ResultSerializer, WorkshopsAndResultsSerializer
from api.models import Workshop, Result
from django_filters.rest_framework import DjangoFilterBackend

# For the documentation
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, get_serializer_ref_name
from drf_yasg.inspectors import JSONFieldInspector
from drf_yasg import openapi

# This param is added in the schema through the decorator (using drf_yasg)
# TODO required
admin_code_param = openapi.Parameter(
    'admin_code', openapi.IN_QUERY, description="The admin_code (found in the workshop object) is required to delete results or workshops", type=openapi.TYPE_STRING, required=True)


class WorkshopViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Workshop to be viewed or edited.
    """

    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['workshop_name',
                        'admin_email', 'admin_name', 'workshop_code']
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Upon workshop creation, send an email to the workshop's admin with confirmation and access detail
        """
        serializer.save()
        context = {"workshop_name": serializer.data["workshop_name"], "visualize_result_id": serializer.data["id"],
                   "workshop_code": serializer.data["workshop_code"], "admin_code": serializer.data["admin_code"]}
        html_message = render_to_string('workshop_confirm_email.html', context)
        plain_message = strip_tags(html_message)

        send_mail(
            'Votre atelier {} a bien été créé'.format(
                serializer.data["workshop_name"]),
            plain_message,
            os.environ.get("EMAIL_HOST_USER", 'mission-climat'),
            [serializer.data["admin_email"]],
            fail_silently=True,
            html_message=html_message
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

            workshop = Workshop.objects.get(
                workshop_code=serializer.data["workshop_code"])

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


class WorkshopAndResult(APIView):

    http_method_names = ["get"]

    @swagger_auto_schema(responses={200: openapi.Response('OK', WorkshopsAndResultsSerializer), })
    def get(self, request):
        """
        Return all workshops and results
        """

        response = {
            "results": list(Result.objects.all().values()),
            "workshops": list(Workshop.objects.all().values()),
        }

        return(JsonResponse(response))


class SendResultAccessEmail(APIView):

    http_method_names = ["post"]

    @swagger_auto_schema(responses={200: openapi.Response(r'Object with success message ex:  {"message" : "4 email(s) sent"} ')}, manual_parameters=[admin_code_param])
    def post(self, request):
        """
        Send result access email to all the users that have submitted their emails
        """

        # retrieve the workshop associated with the admin_code in the query
        workshop = Workshop.objects.get(
            admin_code=request.query_params.get('admin_code'))

        if workshop.email_access_sent_nb >= int(os.environ.get("EMAIL_ACCESS_LIMIT_NB", 2)):
            return(JsonResponse({"message": "exeeded the {} email number limit".format(os.environ.get("EMAIL_ACCESS_LIMIT", 2))}))

        # Retrieve all the result of the workshop
        results = Result.objects.filter(workshop_code=workshop.workshop_code)

        recipient_list = []

        # For each result get user email (if not already in recipient_list)
        for result in results:
            if result.user_email and result.user_email not in recipient_list:
                recipient_list.append(result.user_email)

        if len(recipient_list) > 0:

            context = {
                "visualize_result_id": workshop.id}

            html_message = render_to_string(
                'result_access_email.html', context)
            plain_message = strip_tags(html_message)

            email = EmailMessage('Accès aux résultats',
                                 plain_message,
                                 os.environ.get(
                                     "EMAIL_HOST_USER", 'mission-climat'),
                                 [],
                                 recipient_list)

            email.send()
            workshop.email_access_sent_nb += 1
            workshop.save()

        return(JsonResponse({"message": "{} email(s) sent".format(len(recipient_list))}))
