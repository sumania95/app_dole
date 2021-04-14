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
    Barangay,
    Profile,
    Programs,
    Programs_Detail,
    Sms_Bluster,
    Sms_Config,
)
from .forms import (
    ProgramsForm,
    Sms_BlusterForm
)
from django.utils import timezone
from app_dole.render import (
    Render
)

import huaweisms.api.user
import huaweisms.api.sms

success = 'success'
info = 'info'
error = 'error'
warning = 'warning'
question = 'question'

class Programs_Page(LoginRequiredMixin,TemplateView):
    template_name = 'admin_page/pages/programs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Programs"
        return context

class Programs_Create(LoginRequiredMixin,TemplateView):
    template_name = 'admin_page/components/programs_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Programs"
        return context

class Programs_Create_AJAXView(LoginRequiredMixin,View):
    template_name = 'admin_page/forms/programs_forms.html'
    def get(self, request):
        data = dict()
        form = ProgramsForm()
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
            form = ProgramsForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                data['message_type'] = success
                data['message_title'] = 'Successfully saved.'
        return JsonResponse(data)

class Programs_Update(LoginRequiredMixin,TemplateView):
    template_name = 'admin_page/components/programs_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            id = self.kwargs['pk']
            context['programs'] = Programs.objects.get(id = id)
        except Exception as e:
            pass
        context['title'] = "Update Programs"
        return context

class Programs_Update_AJAXView(LoginRequiredMixin,View):
    template_name = 'admin_page/forms/programs_forms.html'
    def get(self, request):
        data = dict()
        try:
            id = self.request.GET.get('id')
        except KeyError:
            id = None
        programs = Programs.objects.get(pk=id)
        form = ProgramsForm(instance=programs)
        context = {
            'form': form,
            'programs':programs,
            'is_Create': False,
            'btn_name': "warning",
            'btn_title': "Update",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Programs_Update_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data = dict()
        programs = Programs.objects.get(pk=pk)
        if request.method == 'POST':
            form = ProgramsForm(request.POST,request.FILES,instance=programs)
            if form.is_valid():
                form.save()
                data['message_type'] = success
                data['message_title'] = 'Successfully updated.'
        return JsonResponse(data)

class Programs_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Programs.objects.all()
    template_name = 'admin_page/tables/programs_table.html'
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
            data['counter'] = self.queryset.filter(Q(description__icontains = search)).count()
            programs = self.queryset.filter(Q(description__icontains = search)).order_by('date_created')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'programs':programs,'start':start})
        return JsonResponse(data)

class Programs_Details_Page(DetailView):
    model = Programs
    template_name = 'admin_page/pages/programs_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['barangay'] = Barangay.objects.all()
        context['title'] = "Details Overview"
        return context

class Programs_Details_Form_AJAXView(LoginRequiredMixin,View):
    template_name = 'admin_page/forms/programs_details_forms.html'
    def get(self, request):
        data = dict()
        try:
            program_id = self.request.GET.get('program_id')
        except Exception as e:
            program_id = None
        context = {
            'program_id': program_id,
            'is_Create': True,
            'btn_name': "primary",
            'btn_title': "Submit",
            'title': "ADD TO LIST",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Programs_Details_Profile_Create_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data = dict()
        id = self.request.POST.get('program_id')
        profile = Profile.objects.get(pk=pk)
        programs = Programs.objects.get(pk=id)
        if request.method == 'POST':
            Programs_Detail.objects.create(profile=profile,programs=programs)
            data['message_type'] = success
            data['message_title'] = 'Successfully added.'
        else:
            data['message_type'] = error
            data['message_title'] = 'ERROR Connection Lost.'
        return JsonResponse(data)

class Programs_Details_Profile_Remove_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data = dict()
        if request.method == 'POST':
            Programs_Detail.objects.get(id=pk).delete()
            data['message_type'] = success
            data['message_title'] = 'Successfully removed.'
        else:
            data['message_type'] = error
            data['message_title'] = 'ERROR Connection Lost.'
        return JsonResponse(data)

class Programs_Details_Profile_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Profile.objects.all()
    template_name = 'admin_page/tables/programs_details_profile_table.html'
    def get(self, request):
        data = dict()
        try:
            search = self.request.GET.get('search')
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
            program_id = self.request.GET.get('program_id')
        except KeyError:
            search = None
            start = None
            end = None
            program_id = None
        if search or start or end:
            data['form_is_valid'] = True
            data['counter'] = self.queryset.exclude(id__in = Programs_Detail.objects.values('profile_id').filter(programs_id = program_id)).filter(Q(surname__icontains = search)|Q(firstname__icontains = search)).count()
            profile = self.queryset.exclude(id__in = Programs_Detail.objects.values('profile_id').filter(programs_id = program_id)).filter(Q(surname__icontains = search)|Q(firstname__icontains = search)).order_by('surname','firstname','middlename')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'profile':profile,'start':start,'program_id':program_id})
        return JsonResponse(data)

class Programs_Detials_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Programs_Detail.objects.all()
    template_name = 'admin_page/tables/programs_details_table.html'
    def get(self, request,pk):
        data = dict()
        try:
            search = self.request.GET.get('search')
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
            barangay = self.request.GET.get('barangay')

        except KeyError:
            search = None
            start = None
            end = None
            barangay = None
        if search or start or end or barangay:
            if int(barangay) > 0:
                data['form_is_valid'] = True
                data['counter'] = self.queryset.filter(Q(profile__surname__icontains = search)|Q(profile__firstname__icontains = search),programs_id=pk,profile__barangay_id = barangay).count()
                programs_details = self.queryset.filter(Q(profile__surname__icontains = search)|Q(profile__firstname__icontains = search),programs_id=pk,profile__barangay_id = barangay).order_by('profile__surname','profile__firstname')[int(start):int(end)]
                data['data'] = render_to_string(self.template_name,{'programs_details':programs_details,'start':start})
            else:
                data['form_is_valid'] = True
                data['counter'] = self.queryset.filter(Q(profile__surname__icontains = search)|Q(profile__firstname__icontains = search),programs_id=pk).count()
                programs_details = self.queryset.filter(Q(profile__surname__icontains = search)|Q(profile__firstname__icontains = search),programs_id=pk).order_by('profile__surname','profile__firstname')[int(start):int(end)]
                data['data'] = render_to_string(self.template_name,{'programs_details':programs_details,'start':start})
        return JsonResponse(data)

class Programs_Details_Print(LoginRequiredMixin,View):
    queryset = Programs_Detail.objects.all()
    def get(self, request,pk):
        try:
            search = self.request.GET.get('search')
            barangay = self.request.GET.get('barangay')
        except KeyError:
            search = None
            start = None
            end = None
            barangay = None
        now = timezone.now()
        programs = Programs.objects.get(id=pk)
        if search or barangay:
            if int(barangay) > 0:
                profile = self.queryset.filter(Q(profile__surname__icontains = search)|Q(profile__firstname__icontains = search),programs_id=pk,profile__barangay_id = barangay).order_by('profile__surname','profile__firstname')
            else:
                profile = self.queryset.filter(Q(profile__surname__icontains = search)|Q(profile__firstname__icontains = search),programs_id=pk).order_by('profile__surname','profile__firstname')
        params = {
            'now': now,
            'programs': programs,
            'profile': profile,
        }
        pdf = Render.render('reports/programs_print.html', params)
        return pdf

# SMS BLUSTER

class Programs_Details_SMS_Bluster_AJAXView(LoginRequiredMixin,View):
    template_name = 'admin_page/forms/programs_details_sms_bluster_form.html'
    def get(self, request):
        data = dict()
        try:
            program_id = self.request.GET.get('program_id')
        except Exception as e:
            program_id = None
        forms = Sms_BlusterForm()
        context = {
            'program_id': program_id,
            'forms': forms,
            'is_Create': True,
            'btn_name': "success",
            'btn_title': "SEND MESSAGE",
            'title': "CREATE MESSAGE",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Programs_Details_SMS_Bluster_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data = dict()
        program = Programs_Detail.objects.filter(programs_id=pk).count()
        program_list = Programs_Detail.objects.filter(programs_id=pk).all()
        # Sms_Config
        sms_config = Sms_Config.objects.first()
        try:
            ctx = huaweisms.api.user.quick_login(sms_config.username, sms_config.password, modem_host=sms_config.ip_address)
            print(ctx)
            if request.method == 'POST':
                form = Sms_BlusterForm(request.POST,request.FILES)
                mobile_no = []
                message = ""
                if form.is_valid():
                    for p in program_list:
                        mobile_no.append(p.profile.contact_no)
                        form.instance.profile = p.profile
                        form.instance.user = self.request.user
                        message = form.instance.message
                        form.save()
                huaweisms.api.sms.send_sms(
                    ctx,
                    mobile_no,
                    message
                )
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully send.'
        except Exception as e:
            data['valid'] = False
            data['message_type'] = error
            data['message_title'] = 'Message Not Sent!'
        return JsonResponse(data)
import csv
from django.http import HttpResponse
class Programs_Details_Export_Excel_AJAXView(LoginRequiredMixin,View):
    def get(self, request,pk):
        programs = Programs.objects.get(id=pk)
        profile = Programs_Detail.objects.filter(programs_id = programs.id).values_list('profile__firstname', 'profile__middlename', 'profile__surname','profile__ext_name','profile__date_of_birth', 'profile__gender' , 'profile__civil_status' ,'profile__purok_street','profile__barangay__name','profile__contact_no').order_by('profile__surname','profile__firstname')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="programs.csv"'
        writer = csv.writer(response)
        writer.writerow(['Firstname', 'Middlename', 'Surname','Ext Name' ,'Birthdate','Gender', 'Status','Purok Street','Barangay' ,'Mobile'])
        for user in profile:
            writer.writerow(user)
        return response
