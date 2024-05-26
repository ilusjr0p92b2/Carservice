from django.contrib import admin
from .models import Car, Service, Order, Category


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'year', 'owner']
    list_filter = ['year']
    search_fields = ['brand', 'model', 'owner__username']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['car', 'date', 'time', 'is_completed']
    list_filter = ['date', 'time', 'is_completed']
    search_fields = ['car__brand', 'car__model']

    filter_horizontal = ['services']  # Добавляет удобный интерфейс для выбора множества услуг

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Предзагрузить связанные модели для улучшения производительности
        return queryset.select_related('car')
