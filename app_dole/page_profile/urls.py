from django.urls import path,include
from .import views

from .views import (
    Profile_Page,
    Profile_Create,
    Profile_Create_AJAXView,
    Profile_Update,
    Profile_Update_AJAXView,
    Profile_Update_Save_AJAXView,
    Profile_Table_AJAXView,
    Profile_Details_Page,
    Profile_Programs_Details_Table_AJAXView
)

urlpatterns = [
    path('', Profile_Page.as_view(), name = 'profile'),
    path('create', Profile_Create.as_view(), name = 'profile_create'),
    path('api/create', Profile_Create_AJAXView.as_view(), name = 'profile_create_api'),
    path('update/<int:pk>', Profile_Update.as_view(), name = 'profile_update'),
    path('api/update', Profile_Update_AJAXView.as_view(), name = 'profile_update_api'),
    path('api/update/save/<int:pk>', Profile_Update_Save_AJAXView.as_view(), name = 'profile_update_save_api'),
    path('api/table', Profile_Table_AJAXView.as_view(), name = 'profile_table_api'),
    path('details/<int:pk>', Profile_Details_Page.as_view(), name = 'profile_details'),
    path('api/details/table/<int:pk>', Profile_Programs_Details_Table_AJAXView.as_view(), name = 'profile_programs_details_table_api'),


]
