from django.conf import settings
from django.db import models
from django.dispatch import receiver, Signal
from django.db.models.signals import post_save
from helpers.send_email import send_email
from config.keys import SENDER_EMAIL

pre_bulk_create = Signal(["objs", "batch_size"])
post_bulk_create = Signal(["objs", "batch_size"])

class ContactQuerySet(models.QuerySet):
    def bulk_create(self, objs, batch_size=None, ignore_conflicts=True):
            pre_bulk_create.send(sender=self.model, objs=objs, batch_size=batch_size)
            res = super(ContactQuerySet, self).bulk_create(objs, batch_size)
            post_bulk_create.send(sender=self.model, objs=objs, batch_size=batch_size)
            return res

# Create your models here.
class Contact(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    first_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    middle_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    phone_number = models.CharField(
        max_length=255,
        blank=False
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    date_added = models.DateTimeField(
        auto_now_add=True
    )

    objects= ContactQuerySet.as_manager()

@receiver(post_bulk_create, sender=Contact)
def bulk_create_handler(sender, **kwargs):
    objs = kwargs['objs']
    recipient_email = objs[0].user.email
    
    send_email(recipient_email, SENDER_EMAIL, "Upload successful", "Your CSV records has been successfully uploaded to the database")
    