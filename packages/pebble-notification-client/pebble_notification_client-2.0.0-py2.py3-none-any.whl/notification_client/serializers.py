"""Serialize the Events into data objects to send to JSON.
"""
from abc import abstractmethod
import logging
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils import timezone

from rest_framework import serializers

from queue_fetcher.utils import sqs

logger = logging.getLogger(__name__)  # pylint: disable=C0103


class SQSMessageMixin(object):
    """Send serialized data to SQS when the serializer is saved.
    """

    def save(self):
        """Push the serialized information out to the server.
        """

        validated_data = self.validate(self.data)
        queue_name = getattr(settings, 'AWS_EVENT_QUEUE', False)
        # Default setting from boto3
        region_name = getattr(settings, 'DEFAULT_SQS_REGION', False)

        if not queue_name:
            raise ImproperlyConfigured(
                'AWS_EVENT_QUEUE has not been configured. Make sure that '
                'it\'s configured in your settings file.')

        if region_name:
            queue = sqs.get_queue(queue_name, region_name=region_name)
        else:
            queue = sqs.get_queue(queue_name)

        sqs.send_message(queue, validated_data)
        self.save_success_message()

    @abstractmethod
    def save_success_message(self):
        """Make a log when the message is successfully sent to SQS.
        """
        return


class _ModelOrIntegerField(serializers.IntegerField):
    """Specialized handler for integer or Model fields.
    """

    def to_internal_value(self, data):
        """Convert a Django Model into a field.
        """
        if isinstance(data, models.Model):
            return data.pk
        return data


class EventSerializer(SQSMessageMixin, serializers.Serializer):
    """Serialize an event from data and context.

    Take the output of .data and pass it straight into the send_message.
    """

    event_name = serializers.CharField()
    organisation = _ModelOrIntegerField()

    user_incoming = serializers.IntegerField(allow_null=True)
    email_incoming = serializers.EmailField(allow_blank=True)

    user_outgoing = serializers.IntegerField(allow_null=True)
    email_outgoing = serializers.EmailField(allow_blank=True)

    route_params = serializers.JSONField(allow_null=True)

    related_obj = serializers.IntegerField(allow_null=True)

    extra = serializers.JSONField()

    def validate(self, validated_data):
        """Add the extra UUID and datetime fields.

        We will also add the user_outgoing and email_outgoing fields here.
        """
        validated_data['uuid'] = str(uuid4())
        validated_data['datetime'] = str(timezone.now())
        validated_data['message_type'] = 'event'

        if validated_data['user_outgoing'] is None:
            validated_data['user_outgoing'] = validated_data['user_incoming']
        if validated_data['email_outgoing'] is None:
            validated_data['email_outgoing'] = validated_data['email_incoming']

        return validated_data

    def save_success_message(self):
        """Make a log when the event is successfully sent to SQS.
        """
        logger.info('Sent event %s to SQS', self.validated_data['uuid'])


class OrganisationSerializer(serializers.Serializer):
    """Serialize an organisation.
    """

    external_id = serializers.IntegerField(source='id')
    name = serializers.CharField()


class UserListSerializer(SQSMessageMixin, serializers.ListSerializer):
    """Serialize multiple users for SQS.
    """

    def validate(self, data):
        """Add the SQS message type before saving.
        """
        return {
            'message_type': 'manual_add_user',
            'user_list': data
        }

    def save_success_message(self):
        """Make a log when the user is successfully sent to SQS.
        """
        logger.info('Sent %d users to SQS', len(self.data))


class UserSerializer(serializers.Serializer):
    """Serialize a user.
    """

    email = serializers.EmailField()
    first_name = serializers.CharField(
        max_length=100, allow_blank=True, allow_null=True)
    last_name = serializers.CharField(
        max_length=100, allow_blank=True, allow_null=True)

    is_active = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()

    organisations = OrganisationSerializer(many=True)

    class Meta:
        list_serializer_class = UserListSerializer
