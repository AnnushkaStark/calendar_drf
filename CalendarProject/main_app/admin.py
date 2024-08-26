from django.contrib import admin

from models import EventModel


@admin.register(EventModel)
class EventModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_time",
        "period",
    )
    ordering = ["start_time"]
    search_fields = ["name"]
    search_help_text = "Поиск по названию"
