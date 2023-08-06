# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from admin_extra_urls.mixins import _confirm_action
from django.contrib import admin

from admin_extra_urls.extras import ExtraUrlMixin, link
from django.db import connection

from crashlog.models import Error


class ErrorAdmin(ExtraUrlMixin, admin.ModelAdmin):
    change_form_template = "admin/crashlog/error_form.html"
    date_hierarchy = 'date_time'
    list_display = ('class_name', 'message', 'date_time', 'url', 'username')
    list_filter = ('class_name', 'date_time', 'server_name')
    search_fields = ('username', 'class_name', 'message', 'url')
    ordering = ('-date_time',)

    @link(label='Empty Log', css_class="btn btn-danger", icon="icon-trash icon-white")
    def empty_log(self, request):
        def _action(request):
            cursor = connection.cursor()
            cursor.execute('TRUNCATE TABLE "{0}"'.format(Error._meta.db_table))

        return _confirm_action(self, request, _action,
                               "Confirm deletion whole error log",
                               "Successfully executed")

    def has_add_permission(self, request):
        return False


admin.site.register(Error, ErrorAdmin)
