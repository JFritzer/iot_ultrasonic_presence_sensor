from django.urls import path
from . import views

urlpatterns = [
    path('displaymqtt/', views.displaymqtt, name='displaymqtt'),
]

