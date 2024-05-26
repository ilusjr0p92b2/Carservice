from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlencode
from django.utils.timezone import now
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, Car, Order, Category


class ServiceListView(ListView):
    model = Service
    template_name = './service/service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        queryset = super().get_queryset()
        selected_filters_ids = self.request.GET.getlist('selected_filters')
        if selected_filters_ids:
            queryset = queryset.filter(category_id__in=selected_filters_ids)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if user.is_authenticated:
            car = Car.objects.filter(owner=user).first()
            filter_list = Category.objects.all()
            selected_filters_ids = self.request.GET.getlist('selected_filters')

            current_datetime = now()
            current_date = current_datetime.date().strftime('%Y-%m-%d')
            current_time = current_datetime.time()

            context.update({
                'car': car,
                'filter_list': filter_list,
                'show_filters': True,
                'selected_filters': selected_filters_ids,
                'current_date': current_date,
                'current_time': current_time,
            })
        return context

    def post(self, request, **kwargs):
        selected_filters_ids = request.POST.getlist('selected_filters')
        url = reverse_lazy('service_list')
        query_string = urlencode({'selected_filters': selected_filters_ids}, doseq=True)
        return redirect(f'{url}?{query_string}')


@method_decorator(login_required, name='dispatch')
class ServiceBookingView(View):
    def post(self, request):
        selected_services_ids = request.POST.get('selected_services').split(',')
        user = request.user
        date = request.POST.get('date')
        car_brand = request.POST.get('brand')
        car_model = request.POST.get('model')
        car_vin = request.POST.get('vin')
        car_year = request.POST.get('year')

        car, created = Car.objects.get_or_create(
            model=car_model,
            brand=car_brand,
            year=int(car_year),
            owner=user
        )

        order = Order.objects.create(
            car=car,
            date=date.split('T')[0],
            time=date.split('T')[1],
            is_completed=False,
            user=user
        )

        try:
            services = Service.objects.filter(id__in=selected_services_ids)
            order.services.set(services)

            order.save()  # Сохраняем заказ перед установкой услуг
            message = f'Вы успешно записались на {date.split("T")[0]} в {date.split("T")[1]}.'
            messages.success(request, message)
            return redirect('service_list')
        except Exception as e:
            messages.error(request, f'Произошла ошибка: {str(e)}')
            return redirect('not_found')


@method_decorator(login_required, name='dispatch')
class CarServiceListView(View):
    template_name = 'service/car_services.html'

    def get(self, request, *args, **kwargs):
        # Получить все заказы с is_completed=False
        orders = Order.objects.filter(is_completed=False)
        print(orders)
        # Получить все связанные с ними услуги
        services = [order.services.all() for order in orders]
        print(services)
        # services теперь список списков услуг для каждого заказа
        return render(request, self.template_name, {'orders': orders, 'services': services})


class MarkAsDoneView(View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.is_completed = True
        order.save()
        return redirect('orders')


# class EditorderView(View):
#     template_name = 'authapp/edit_service.html'
#
#     def get(self, request, service_id):
#         service = get_object_or_404(Service, id=service_id, car__owner=request.user)
#         form = ServiceForm(instance=service)
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request, service_id):
#         service = get_object_or_404(Service, id=service_id, car__owner=request.user)
#         form = ServiceForm(request.POST, instance=service)
#         if form.is_valid():
#             form.save()
#             return redirect('car_services')
#         return render(request, self.template_name, {'form': form})
#
#
class DeleteOrderView(View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        return redirect('orders')
