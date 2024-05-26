from django.contrib import admin
from .models import Article, Category, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'image')
    list_filter = ('author', 'created_at', 'updated_at', 'categories')
    search_fields = ('title', 'content')
    filter_horizontal = ('categories',)
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author', 'categories', 'image')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content',)
    raw_id_fields = ('author', 'article')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
