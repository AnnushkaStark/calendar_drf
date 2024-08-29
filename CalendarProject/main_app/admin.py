from django.contrib import admin

from main_app.models import EventModel


@admin.register(EventModel)
class EventModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_time",
        "period",
    )
    search_fields = ["name"]
    search_help_text = "Поиск по названию"
