from django.urls import path,include
from .import views

from .views import (
    Reports,
)

urlpatterns = [
    path('', Reports.as_view(), name = 'reports'),
]
