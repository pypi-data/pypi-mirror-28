# Copyright (c) 2017 LINE Corporation
# These sources are released under the terms of the MIT license: see LICENSE

import logging
import textwrap

from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from promgen import tasks
from promgen.models import Project, Service
from promgen.shortcuts import resolve_domain

logger = logging.getLogger(__name__)


class FormSenderBase(forms.Form):
    value = forms.CharField(required=True)
    alias = forms.CharField(required=False)


class NotificationBase(object):
    '''
    Base Notification class
    '''
    MAPPING = [
        ('project', Project),
        ('service', Service),
    ]

    form = FormSenderBase

    @classmethod
    def help(cls):
        if cls.__doc__:
            return textwrap.dedent(cls.__doc__)

    @classmethod
    def process(cls, data):
        '''
        Process a notification

        By default, this will just queue an item in celery to be processed but in some cases
        a notifier may want to immediately process it or otherwise send a message, so we
        provide this entry hook
        '''
        params = {'args': (cls.__module__, data)}
        if hasattr(cls, 'queue'):
            params['queue'] = getattr(cls, 'queue')
        tasks.send_notification.apply_async(**params)

    def _send(self, target, alert):
        '''
        Sender specific implmentation

        This function will receive some kind of target value, such as an email
        address or post endpoint and an individual alert combined with some
        additional alert meta data
        '''
        raise NotImplementedError()

    def config(self, key):
        '''
        Plugin specific configuration

        This wraps our PROMGEN settings so that a plugin author does not need to
        be concerned with how the configuration files are handled but only about
        the specific key.
        '''
        try:
            return settings.PROMGEN[self.__module__][key]
        except KeyError:
            logger.error('Undefined setting. Please check for %s under %s in settings.yml', key, self.__module__)

    def expand(self, data):
        '''
        Look through our alert and expand any objects we find

        This is responsible for looking through our alerts and finding any
        supported labels (like Projects and Services) that we can expand into
        an annotation
        '''
        output = {}

        data.setdefault('commonLabels', {})
        data.setdefault('commonAnnotations', {})

        # Look through our labels and find the object from Promgen's DB
        # If we find an object in Promgen, add an annotation with a direct link
        for label, klass in self.MAPPING:
            if label not in data['commonLabels']:
                logger.debug('Missing label %s', label)
                continue

            # Should only find a single value, but I think filter is a little
            # bit more forgiving than get in terms of throwing errors
            for obj in klass.objects.filter(name=data['commonLabels'][label]):
                logger.debug('Found %s %s', label, obj)
                output[label] = obj
                data['commonAnnotations'][label] = resolve_domain(obj)
        return output

    def send(self, data):
        '''
        Send out an alert

        This handles looping through the alerts from Alert Manager and checks
        to see if there are any notification senders configured for the
        combination of project/service and sender type.

        See tests/examples/alertmanager.json for an example payload
        '''
        sent = 0
        output = self.expand(data)

        for label, obj in output.items():
            for sender in obj.notifiers.filter(sender=self.__module__):
                try:
                    self._send(sender.value, data)
                except:
                    logger.exception('Error sending notification')
                else:
                    sent += 1
        if sent == 0:
            logger.debug('No senders configured for project or service')
        return sent

    def test(self, target, data):
        '''
        Send out test notification

        Combine a simple test alert from our view, with the remaining required
        parameters for our sender child classes
        '''
        logger.debug('Sending test message to %s', target)
        self.expand(data)
        self._send(target, data)

    def render(self, template, context):
        s = render_to_string(template, context).strip()
        # Uncomment to re-generate test templates
        # with open(template.replace('sender', 'tests/notifications'), 'w+') as fp:
        #     fp.write(s)
        return s
