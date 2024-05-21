from django.contrib import admin
from django.urls import path, include

from service.views import ServiceListView

urlpatterns = [
    path('', ServiceListView.as_view(), name='service_list'),
    # path('/<int:id>', name='service_about'),

]
