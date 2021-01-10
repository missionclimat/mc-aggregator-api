from django.contrib import admin
from api.models import Workshop, Result

# Register your models here.


class WorkshopAdmin(admin.ModelAdmin):
    list_display = (
        "workshop_name",
        "id",
        "admin_code",
        "workshop_code",
        "time_created",
        "admin_name",
        "admin_email",
        "participants_nb",
        "email_access_sent_nb"
    )
    list_filter = ("workshop_name", "admin_name")
    search_fields = ["workshop_name"]


class ResultAdmin(admin.ModelAdmin):
    list_display = ("id", "workshop_code", "user_email", "group_name")
    list_filter = ("workshop_code__workshop_name", "group_name", "user_email", "workshop_code")
    search_fields = ["workshop_code__admin_name", "group_name"]


admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(Result, ResultAdmin)
