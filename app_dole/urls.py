from django.urls import path,include
from .import views

from .views import (
    Home,
    Security_Page,
    Security_AJAXView,
)

urlpatterns = [
    path('', Home.as_view(), name = 'dashboard'),
    path('profile/', include('app_dole.page_profile.urls')),
    path('programs/', include('app_dole.page_programs.urls')),
    path('reports/', include('app_dole.page_reports.urls')),
    path('auth/', include('app_dole.page_auth.urls')),
    path('sms/', include('app_dole.page_sms_config.urls')),
    path('security', Security_Page.as_view(), name = 'security'),
    path('api/security', Security_AJAXView.as_view(), name = 'api_security'),
]
