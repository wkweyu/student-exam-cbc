from django.contrib import admin
from .models import Class, Stream

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('grade_level', 'year')
    list_filter = ('grade_level', 'year')

@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_ref')
    list_filter = ('class_ref',)
