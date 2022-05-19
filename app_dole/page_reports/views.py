from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import (
    View,
    TemplateView,
    ListView,
    DetailView,
)
from django.conf.urls.static import static

#functions
from django.db.models.functions import Coalesce,Concat
from django.db.models import Q,F,Sum,Count
from django.db.models import Value
from django.urls import reverse
#datetime
from datetime import datetime
from django.utils import timezone
#JSON AJAX
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

from app_dole.render import Render

class Reports(LoginRequiredMixin,TemplateView):
    template_name = 'admin_page/pages/reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']        = "Reports"
        context['barangay']     = Barangay.objects.all()
        return context


class Report_Generate_List_Print(LoginRequiredMixin,View):
    def get(self, request):
        try:
            datepicker1     = self.request.GET.get('datepicker1')
            datepicker2     = self.request.GET.get('datepicker2')
            category        = self.request.GET.get('category')
            barangay_id     = self.request.GET.get('barangay')
        except KeyError:
            datepicker1     = None
            datepicker2     = None
            category        = None
            barangay_id     = None
        now = timezone.now()
        record_array = []
        print(category)
        if category or barangay_id or datepicker1 or datepicker2:
            if category == "0":
                if barangay_id == "0":
                    record = Programs_Detail.objects.filter(programs__date_from__range=(datepicker1, datepicker2)).order_by('profile__surname','profile__firstname','profile__middlename').all()
                    profile = Profile.objects.filter(id__in = record.values('profile_id')).all()
                    for p in profile:
                        profile = {
                        'profile' : Profile.objects.get(id=p.id),
                        'program_detail' : Programs_Detail.objects.filter(profile_id = p.id,programs__date_from__range=(datepicker1, datepicker2)),
                        }
                        record_array.append(profile)
                else:
                    record = Programs_Detail.objects.filter(profile__barangay_id = barangay_id,programs__date_from__range=(datepicker1, datepicker2)).order_by('profile__surname','profile__firstname','profile__middlename').all()
                    profile = Profile.objects.filter(id__in = record.values('profile_id')).all()
                    for p in profile:
                        profile = {
                        'profile' : Profile.objects.get(id=p.id),
                        'program_detail' : Programs_Detail.objects.filter(profile_id = p.id,programs__date_from__range=(datepicker1, datepicker2)),
                        }
                        record_array.append(profile)
            else:
                if barangay_id == "0":
                    print('all')
                    record = Programs_Detail.objects.filter(programs__category=category,programs__date_from__range=(datepicker1, datepicker2)).order_by('profile__surname','profile__firstname','profile__middlename').all()
                    profile = Profile.objects.filter(id__in = record.values('profile_id')).all()
                    for p in profile:
                        profile = {
                        'profile' : Profile.objects.get(id=p.id),
                        'program_detail' : Programs_Detail.objects.filter(profile_id = p.id,programs__category=category,programs__date_from__range=(datepicker1, datepicker2)),
                        }
                        record_array.append(profile)
                else:
                    print('selected')
                    record = Programs_Detail.objects.filter(programs__category=category,profile__barangay_id = barangay_id,programs__date_from__range=(datepicker1, datepicker2)).order_by('profile__surname','profile__firstname','profile__middlename').all()
                    profile = Profile.objects.filter(id__in = record.values('profile_id')).all()
                    for p in profile:
                        profile = {
                        'profile' : Profile.objects.get(id=p.id),
                        'program_detail' : Programs_Detail.objects.filter(profile_id = p.id,programs__category=category,programs__date_from__range=(datepicker1, datepicker2)),
                        }
                        record_array.append(profile)
        params = {
            'now': now,
            'profile': record_array,
            'date_from': datepicker1,
            'date_to': datepicker2,
        }
        pdf = Render.render('reports/report_generate_list.html', params)
        return pdf
