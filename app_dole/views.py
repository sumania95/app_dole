from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import (
    View,
    TemplateView,
    ListView,
    DetailView,
)

#functions
from django.db.models.functions import Coalesce,Concat
from django.db.models import Q,F,Sum,Count
from django.db.models import Value
from django.urls import reverse
#datetime
from datetime import datetime
#JSON AJAX
#JSON AJAX
from django.core import serializers
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.template import RequestContext

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (
    Profile,
    Barangay,
    Programs,
)
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth import logout
import json
success = 'success'
info = 'info'
error = 'error'
warning = 'warning'
question = 'question'

class Home(LoginRequiredMixin,TemplateView):
    LOGIN_URL = 'login'
    template_name = 'admin_page/pages/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_total'] = Profile.objects.all().count()
        context['barangay_total'] = Barangay.objects.all().count()
        context['program_total'] = Programs.objects.all().count()
        context['user_total'] = User.objects.all().count()
        return context

class Security_Page(LoginRequiredMixin,TemplateView):
    LOGIN_URL = 'login'
    template_name = 'admin_page/pages/security.html'

class Security_AJAXView(LoginRequiredMixin,View):
    def get(self, request):
        data = dict()
        user = User.objects.get(id=self.request.user.id)
        form = SetPasswordForm(user=user)
        context = {
            'form': form,
            'user': user,
            'btn_name': "primary",
            'btn_title': "Submit",
        }
        data['html_form'] = render_to_string('admin_page/forms/security_forms.html',context)
        return JsonResponse(data)

    def post(self, request):
        data =  dict()
        if request.method == 'POST':
            form = SetPasswordForm(user=self.request.user,data=request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully updated.'
                data['url'] = reverse('dashboard')
                logout(request)
            else:
                error_message = form.errors.as_json()
                y = json.loads(error_message)
                data['valid'] = False
                data['message_type'] = error
                new_password2 = y['new_password2']
                for p in new_password2:
                    data['message_title'] = p['message']
        return JsonResponse(data)
