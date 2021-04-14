from django.urls import path,include
from .import views

from .views import (
    Sms_Config_Page,
    Sms_Config_AJAXView,
)

urlpatterns = [
    path('', Sms_Config_Page.as_view(), name = 'sms_config_page'),
    path('api', Sms_Config_AJAXView.as_view(), name = 'sms_config_page_api'),
]
