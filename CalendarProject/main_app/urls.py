from django.urls import path
from .views import (
    ReadEventsView,
    UpdateEventView,
    RemoveEventView,
    RemoveNextEventsView,
    CreateEventView,
    RemoveEventFullView,
)

urlpatterns = [
    path(
        "events/<int:year>/<int:month>/<int:day>/",
        ReadEventsView.as_view(),
        name="events_by_date",
    ),
    path(
        "update/<int:id>/<int:year>/<int:month>/<int:day>/",
        UpdateEventView.as_view(),
        name="update_event",
    ),
    path(
        "remove/<int:id>/<int:year>/<int:month>/<int:day>/",
        RemoveEventView.as_view(),
        name="remove_event",
    ),
    path(
        "remove-next/<int:id>/<int:year>/<int:month>/<int:day>/",
        RemoveNextEventsView.as_view(),
        name="remove_next_events",
    ),
    path("crate/", CreateEventView.as_view(), name="create_event"),
    path("remove_full/<int:id>/", RemoveEventFullView.as_view(), name="remove_full"),
]
