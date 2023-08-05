"""Send events to SQS for processing by notification-centre.
"""
import logging

import six

from boto3 import exceptions as b3e

from django.conf import settings

from rest_framework import serializers

from .exceptions import NotificationClientException
from .serializers import EventSerializer, UserSerializer


logger = logging.getLogger(__name__)  # pylint: disable=C0103


def _get_user(request, user_incoming, email_incoming):
    """Pull out and return the user's ID and email from a given request,
    or (None, '') if the request is None.
    """
    if request:
        user_id = user_incoming if user_incoming else request.user.id
        user_email = email_incoming if email_incoming else request.user.email
    else:
        user_id = user_incoming
        user_email = email_incoming

    return user_id, user_email


def _send_event(event_name, organisation_id, request=None, user_incoming=None,
                email_incoming='', user_outgoing=None, email_outgoing='',
                route_params=None, extra=None, related_obj=None):
    """Send an event to the notifications-centre server.

    @param event_name: the type of event
    @param organisation_id: the active organisation's ID
    @param request: the request that triggered this event (the user's details
        are retrieved from this - may be left unspecified for 'all user'
        notifications)
    @param user_outgoing: the user to deliver the notification to (same as
        the triggering user if unspecified)
    @param email_outgoing: the email address of the user to whom the
        notification will be delivered (same as that of the triggering user if
        unspecified)
    @param route_params: parameters used by the client router to construct the
        final URL
    @param extra: additional event information
    @param related_obj: an object ID used to identify this event in the future
    """

    user_id, user_email = _get_user(request, user_incoming, email_incoming)

    data = {
        'event_name': event_name,
        'user_incoming': user_id,
        'email_incoming': user_email,
        'user_outgoing': user_outgoing,
        'email_outgoing': email_outgoing,
        'organisation': organisation_id,
        'route_params': route_params,
        'related_obj': related_obj,
        'extra': extra if extra is not None else {},
    }

    serialized = EventSerializer(data=data)

    try:
        serialized.is_valid(raise_exception=True)
    except serializers.ValidationError:
        raise NotificationClientException(serialized.errors)

    serialized.save()


def send_event(*args, **kwargs):
    """A wrapper for _send_event() so that the user may elect to ignore
    exceptions.
    """
    if getattr(settings, 'NOTIFICATION_CLIENT_IGNORE_EXCEPTIONS', False):
        exceptions_to_ignore = (b3e.Boto3Error, b3e.RetriesExceededError)
    else:
        exceptions_to_ignore = ()

    try:
        _send_event(*args, **kwargs)
    except exceptions_to_ignore as e:
        logger.exception('Ignored exception: %s', six.text_type(e))


def send_users(user_list):
    """Send users to the notification-centre server.

    @param user_list: the set of user models to serialize and send
    """

    serializer = UserSerializer(user_list, many=True)
    serializer.save()
