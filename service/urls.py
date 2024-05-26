from django.urls import path
from service.views import ServiceListView, ServiceBookingView, CarServiceListView, MarkAsDoneView, DeleteOrderView

urlpatterns = [
    path('', ServiceListView.as_view(), name='service_list'),
    path('order/', ServiceBookingView.as_view(), name='order_service'),
    path('order/success/', ServiceListView.as_view(), name='order_success'),
    path('order_list/', CarServiceListView.as_view(), name='orders'),
    path('order_marks_done/<int:order_id>/', MarkAsDoneView.as_view(), name='mark_as_done'),
    path('delete/<int:order_id>/', DeleteOrderView.as_view(), name='delete_order'),
    path('edit/<int:order_id>/', MarkAsDoneView.as_view(), name='edit_order')
]
