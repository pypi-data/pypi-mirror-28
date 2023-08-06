# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import six
from django.contrib import messages
from django.urls import reverse
from django.db import models
from django.db.models.query import QuerySet
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class ErrorManager(models.Manager):
    def get_queryset(self):
        return QuerySet(self.model, using=self._db).defer('message', 'traceback')

    get_query_set = get_queryset


class Error(models.Model):
    class_name = models.CharField(_('type'), max_length=128)
    message = models.TextField()
    traceback = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    url = models.URLField(null=True, blank=True)
    server_name = models.CharField(max_length=128, db_index=True)
    username = models.CharField(max_length=100, db_index=True, null=True, blank=True)
    objects = ErrorManager()

    def __unicode__(self):
        return "{0.date_time}: {0.class_name}".format(self)

    def __repr__(self):
        try:
            u = six.text_type(self)
        except (UnicodeEncodeError, UnicodeDecodeError):
            u = '[Bad Unicode data]'
        return smart_str(u'<Error: %s>' % u)

    def get_change_url(self):
        return reverse('admin:crashlog_error_change', args=[self.pk])

    def message_user(self, request, message, level=messages.ERROR, extra_tags='', fail_silently=False,
                     detail_link=True):
        if detail_link:
            message = mark_safe("{} (<a href='{}'>details</a>)".format(message, self.get_change_url()))

        messages.add_message(request, level, message, extra_tags=extra_tags,
                             fail_silently=fail_silently)

    class Meta:
        app_label = 'crashlog'
