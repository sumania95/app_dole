from django.views.generic import (
    View,
    TemplateView,
    ListView,
    DetailView,
)

from .models import (
    Barangay
)
from django.contrib.auth.models import User


class Settings_Decorators(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_setting'] = User.objects.get(id=self.request.user.id)
        return context
