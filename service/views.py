from django.views.generic import ListView
from django.shortcuts import render
from .models import Service


class ServiceListView(ListView):
    model = Service
    template_name = './service/service_list.html'
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filters'] = ['Oil Change', 'Tire Rotation', 'Brake Inspection']   # Список фильтров
        context['show_filters'] = True   # Делаем видимым блок фильтров
        return context
