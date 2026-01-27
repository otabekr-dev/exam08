from django.urls import path

from .views import EventCreateView, EventRegisterView, EventRegistrationCancelView, EventStatsView

urlpatterns = [
    path('create/', EventCreateView.as_view(), name='create event'),
    path('register/', EventRegisterView.as_view(), name='register event'),
    path('register/cancel/<int:pk>', EventRegistrationCancelView.as_view(), name='cancel register event'),
    path('stats/', EventStatsView.as_view(), name='event statistics')
]
