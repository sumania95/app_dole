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
from .forms import ProfileForm
from app_dole.models import Profile
from app_dole.decorators import (
    Settings_Decorators,
)
success = 'success'
info = 'info'
error = 'error'
warning = 'warning'
question = 'question'


class Profile_Page(LoginRequiredMixin,Settings_Decorators,TemplateView):
    template_name = 'admin_page/pages/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Profile"
        return context

class Profile_Create(LoginRequiredMixin,TemplateView):
    template_name = 'admin_page/components/profile_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Profile"
        return context

class Profile_Create_AJAXView(LoginRequiredMixin,View):
    template_name = 'admin_page/forms/profile_forms.html'
    def get(self, request):
        data = dict()
        form = ProfileForm()
        context = {
            'form': form,
            'is_Create': True,
            'btn_name': "primary",
            'btn_title': "Submit",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)
    def post(self, request):
        data =  dict()
        if request.method == 'POST':
            form = ProfileForm(request.POST,request.FILES)
            if form.is_valid():
                user_exist = Profile.objects.filter(firstname__iexact = form.instance.firstname.lower(),surname__iexact = form.instance.surname.lower(),ext_name__iexact = form.instance.ext_name.lower()).exists()
                if user_exist:
                    data['valid'] = False
                    data['message_type'] = error
                    data['message_title'] = 'Duplicated Account.'
                else:
                    form.save()
                    data['valid'] = True
                    data['message_type'] = success
                    data['message_title'] = 'Successfully saved.'
        return JsonResponse(data)

class Profile_Update(LoginRequiredMixin,TemplateView):
    template_name = 'admin_page/components/profile_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            id = self.kwargs['pk']
            context['profile'] = Profile.objects.get(id = id)
        except Exception as e:
            pass
        context['title'] = "Update Profile"
        return context

class Profile_Update_AJAXView(LoginRequiredMixin,View):
    template_name = 'admin_page/forms/profile_forms.html'
    def get(self, request):
        data = dict()
        try:
            id = self.request.GET.get('id')
        except KeyError:
            id = None
        profile = Profile.objects.get(pk=id)
        form = ProfileForm(instance=profile)
        context = {
            'form': form,
            'profile':profile,
            'is_Create': False,
            'btn_name': "warning",
            'btn_title': "Update",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Profile_Update_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data = dict()
        profile = Profile.objects.get(pk=pk)
        if request.method == 'POST':
            form = ProfileForm(request.POST,request.FILES,instance=profile)
            if form.is_valid():
                form.save()
                data['message_type'] = success
                data['message_title'] = 'Successfully updated.'
        return JsonResponse(data)

class Profile_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Profile.objects.all()
    template_name = 'admin_page/tables/profile_table.html'
    def get(self, request):
        data = dict()
        try:
            search = self.request.GET.get('search')
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
        except KeyError:
            search = None
            start = None
            end = None
        if search or start or end:
            data['form_is_valid'] = True
            data['counter'] = self.queryset.filter(Q(firstname__icontains = search)|Q(surname__icontains = search)).count()
            profile = self.queryset.filter(Q(firstname__icontains = search)|Q(surname__icontains = search)).order_by('surname','firstname')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'profile':profile,'start':start})
        return JsonResponse(data)
