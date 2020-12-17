from django.db import models
import uuid
from random import randint

# DRF
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


def random_string():
    """
    Create a random string of 6 digit 
    """
    return str(randint(100000, 999999))

# Create your models here.
class Workshop(models.Model):
    """
    Model of the workshop.
    Workshop describe a group of Result, alongside with other access identification numbers
    """

    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        help_text="Use to display the page of the workshop with all the data about the results and praticipants",
    )

    workshop_code = models.CharField(
        max_length=10,
        default=random_string,
        editable=False,
        help_text="A 6 digit unique code, use to refer the workshop when sending the results",
        unique=True,
        blank=False,
    )

    admin_code = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Code used to delete workshop/results",
        blank=False,
    )
    time_created = models.DateTimeField(
        auto_now_add=True, blank=True, help_text="timestamp of the creation"
    )
    workshop_name = models.CharField(max_length=100, help_text="Name of the workshop")
    admin_name = models.CharField(max_length=100, help_text="Name of the admin")
    participants_nb = models.IntegerField(
        blank=False, help_text="Number of the participants (only visual help)"
    )
    admin_email = models.EmailField(
        help_text="Email of the admin used to send him an email with all the informations"
    )

    def __str__(self):
        return str(self.workshop_code)


class Result(models.Model):
    """
    Model of the Result.
    Result describe the data sent by a user from Mission Climat website
    """

    user_email = models.EmailField(
        help_text="Email of the user submitting the result (use to send him a confirmation and keep him up to date with the workshop results later)",
        blank=True,
    )
    data = models.JSONField(blank=False, help_text="The actual result data in json format")
    group_name = models.CharField(max_length=100)
    workshop_code = models.ForeignKey(
        Workshop,
        related_name="results",
        on_delete=models.CASCADE,
        to_field="workshop_code",
        help_text="The workshop_code value, use to refer the result to the workshop",
    )

    def __str__(self):
        return str(self.id)


# Catch post_save signal to create token for any new user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)