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
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth.mixins import LoginRequiredMixin
from app_dole.models import (
    Sms_Config,
)

from .forms import (
    Sms_ConfigForm,
)

success = 'success'
info = 'info'
error = 'error'
warning = 'warning'
question = 'question'


class Sms_Config_Page(LoginRequiredMixin,TemplateView):
    LOGIN_URL = 'login'
    template_name = 'admin_page/pages/sms_config.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "SMS Configuration"
        return context

class Sms_Config_AJAXView(LoginRequiredMixin,View):
    def get(self, request):
        data = dict()
        sms_config = Sms_Config.objects.first()
        if sms_config:
            form = Sms_ConfigForm(instance=sms_config)
        else:
            form = Sms_ConfigForm()
        # print(form)
        context = {
            'form' : form,
            'btn_name': "primary",
            'btn_title': "Changed",
        }
        data['html_form'] = render_to_string('admin_page/forms/sms_config_forms.html',context)
        return JsonResponse(data)

    def post(self, request):
        data =  dict()
        if request.method == 'POST':
            sms_config = Sms_Config.objects.first()
            if sms_config:
                form = Sms_ConfigForm(request.POST,request.FILES,instance=sms_config)
            else:
                form = Sms_ConfigForm(request.POST,request.FILES)
            if form.is_valid():
                user = form.save()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully changed.'
        return JsonResponse(data)
