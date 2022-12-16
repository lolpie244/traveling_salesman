from django.contrib import admin
from django.conf import settings
from balancer.models import WorkersSettings


Workers = settings.REDIS_CLIENT


@admin.register(WorkersSettings)
class SettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


    list_display = ["clients_count", "min_servers_count", "max_servers_count", "prefered_load", "worker_timeout"]

