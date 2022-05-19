from django.urls import path,include
from .import views

from .views import (
    Reports,
    Report_Generate_List_Print,
)

urlpatterns = [
    path('', Reports.as_view(), name = 'reports'),
    path('generate-list', Report_Generate_List_Print.as_view(), name = 'report_generate_list'),
]
