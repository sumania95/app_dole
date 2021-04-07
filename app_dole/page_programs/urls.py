from django.urls import path,include
from .import views

from .views import (
    Programs_Page,
    Programs_Create,
    Programs_Create_AJAXView,
    Programs_Update,
    Programs_Update_AJAXView,
    Programs_Update_Save_AJAXView,
    Programs_Table_AJAXView,
    Programs_Details_Page,
    Programs_Details_Form_AJAXView,
    Programs_Details_Profile_Create_AJAXView,
    Programs_Details_Profile_Remove_AJAXView,
    Programs_Details_Profile_Table_AJAXView,
    Programs_Detials_Table_AJAXView,
    Programs_Details_Print,
)

urlpatterns = [
    path('', Programs_Page.as_view(), name = 'programs'),
    path('create', Programs_Create.as_view(), name = 'programs_create'),
    path('api/create', Programs_Create_AJAXView.as_view(), name = 'programs_create_api'),
    path('update/<int:pk>', Programs_Update.as_view(), name = 'programs_update'),
    path('api/update', Programs_Update_AJAXView.as_view(), name = 'programs_update_api'),
    path('api/update/save/<int:pk>', Programs_Update_Save_AJAXView.as_view(), name = 'programs_update_save_api'),
    path('api/table', Programs_Table_AJAXView.as_view(), name = 'programs_table_api'),
    path('api/profile/table', Programs_Details_Profile_Table_AJAXView.as_view(), name = 'programs_details_profile_table_api'),
    path('details/<int:pk>', Programs_Details_Page.as_view(), name = 'programs_details'),
    path('api/details/table/<int:pk>', Programs_Detials_Table_AJAXView.as_view(), name = 'programs_details_table_api'),
    path('api/details/form', Programs_Details_Form_AJAXView.as_view(), name = 'programs_details_form_api'),
    path('api/details/profile/added/<int:pk>', Programs_Details_Profile_Create_AJAXView.as_view(), name = 'programs_details_profile_create_api'),
    path('api/details/profile/removed/<int:pk>', Programs_Details_Profile_Remove_AJAXView.as_view(), name = 'programs_details_profile_removed_api'),
    path('print/<int:pk>', Programs_Details_Print.as_view(), name = 'programs_details_print'),
]
