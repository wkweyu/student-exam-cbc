from django.contrib import admin
from django import forms
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.html import format_html
from django.http import HttpResponse
from django.utils import timezone
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from import_export.widgets import ForeignKeyWidget, DateWidget
from import_export.formats import base_formats
from .models import Student, Class, Stream, StudentPromotionHistory


@admin.register(Class)
class ClassAdmin(ImportExportModelAdmin):  # Changed from admin.ModelAdmin
    list_display = ('grade_level', 'year', 'student_count')
    list_filter = ('grade_level', 'year')
    search_fields = ('grade_level',)  # Added search
    list_per_page = 50  # Added pagination

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'Students'

@admin.register(Stream)
class StreamAdmin(ImportExportModelAdmin):  # Changed from admin.ModelAdmin
    list_display = ('name', 'class_ref', 'year', 'capacity', 'student_count')
    list_filter = ('class_ref', 'year')
    search_fields = ('name', 'class_ref__grade_level')  # Added search
    list_per_page = 50  # Added pagination

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'Students'

class StudentAdminForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_admitted': forms.DateInput(attrs={'type': 'date'})
        }


class StudentResource(resources.ModelResource):
    class_ref = fields.Field(
        column_name='class_ref',
        attribute='class_ref',
        widget=ForeignKeyWidget(Class, 'grade_level'))
    stream = fields.Field(
        column_name='stream',
        attribute='stream',
        widget=ForeignKeyWidget(Stream, 'name'))
    date_of_birth = fields.Field(
        column_name='date_of_birth',
        attribute='date_of_birth',
        widget=DateWidget('%d/%m/%Y'))
    date_admitted = fields.Field(
        column_name='date_admitted',
        attribute='date_admitted',
        widget=DateWidget('%d/%m/%Y'))

    class Meta:
        model = Student
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('admission_number',)
        fields = (
            'admission_number', 'legacy_admission_number', 'first_name', 'middle_name', 'last_name',
            'date_of_birth', 'gender', 'photo', 'class_ref', 'stream',
            'date_admitted', 'is_active', 'guardian_name', 'guardian_contact',
            'guardian_email', 'address', 'emergency_contact'
        )
        export_order = fields

    def before_import_row(self, row, **kwargs):
        """Handle admission numbers during import"""
        # Preserve legacy number if provided
        if 'legacy_admission_number' in row and row['legacy_admission_number']:
            # Keep the legacy number as is
            pass
        
        # Generate new admission number if not provided
        if 'admission_number' not in row or not row['admission_number']:
            current_year = timezone.now().year
            last_admission = (
                Student.objects
                .filter(admission_number__startswith=str(current_year))
                .order_by('-admission_number')
                .first()
            )
            
            if last_admission:
                try:
                    last_seq = int(last_admission.admission_number.split('-')[1])
                except (IndexError, ValueError):
                    last_seq = 0
            else:
                last_seq = 0
            
            row['admission_number'] = f"{current_year}-{last_seq + 1:04d}"

@admin.register(Student)
class StudentAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = StudentResource
    form = StudentAdminForm
    
    # Display configuration
    list_display = ('admin_photo', 'full_name', 'admission_number', 'legacy_admission_number', 
                   'class_stream', 'is_active', 'current_age')
    list_display_links = ('admin_photo', 'full_name')
    list_filter = (
        ('class_ref', admin.RelatedOnlyFieldListFilter),
        ('stream', admin.RelatedOnlyFieldListFilter),
        ('date_admitted', admin.DateFieldListFilter),
        'is_active',
        'gender',
    )
    search_fields = ('first_name', 'last_name', 'middle_name', 
                    'admission_number', 'legacy_admission_number', 
                    'guardian_name', 'guardian_contact')
    readonly_fields = ('created_at', 'updated_at', 'current_age')
    list_per_page = 50
    save_on_top = True
    list_select_related = ('class_ref', 'stream')
    
    # Fieldsets organization
    fieldsets = (
        ('Personal Information', {
            'fields': ('photo', 'first_name', 'middle_name', 'last_name', 
                      'date_of_birth', 'gender')
        }),
        ('Academic Information', {
            'fields': ('class_ref', 'stream', 'date_admitted', 'is_active')
        }),
        ('Guardian Information', {
            'fields': ('guardian_name', 'guardian_contact', 
                      'guardian_email', 'emergency_contact', 'address')
        }),
        ('System Information', {
            'fields': ('admission_number', 'legacy_admission_number', 
                      'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    # Custom actions
    actions = [
        'activate_students',
        'deactivate_students',
        'promote_students',
        'export_selected_students',
        'generate_admission_numbers',
        'migrate_legacy_numbers'
    ]

    # Custom methods
    def admin_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" />', obj.photo.url)
        return "-"
    admin_photo.short_description = 'Photo'

    def class_stream(self, obj):
        if obj.class_ref and obj.stream:
            return f"{obj.class_ref} - {obj.stream}"
        return "-"
    class_stream.short_description = 'Class/Stream'

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'

    def current_age(self, obj):
        from datetime import date
        today = date.today()
        return today.year - obj.date_of_birth.year - (
            (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
    current_age.short_description = 'Age'

    # Custom URLs
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('register/',
                self.admin_site.admin_view(self.registration_view),
                name='student_registration'),
            path('promote/',
                self.admin_site.admin_view(self.promotion_view),
                name='student_promotion'),
            path('get-streams/',
                self.admin_site.admin_view(self.get_streams),
                name='get_streams'),
        ]
        return custom_urls + urls

    def registration_view(self, request):
        if request.method == 'POST':
            form = self.form(request.POST, request.FILES)
            if form.is_valid():
                student = form.save()
                messages.success(request, f'Student {student.full_name()} registered successfully')
                return redirect('admin:students_student_changelist')
        
        form = self.form()
        context = self.admin_site.each_context(request)
        context.update({
            'opts': self.model._meta,
            'form': form,
            'title': 'Student Registration'
        })
        return render(request, 'admin/students/registration_form.html', context)

    def promotion_view(self, request):
        if request.method == 'POST':
            # Implement promotion logic here
            pass
        
        classes = Class.objects.all()
        context = self.admin_site.each_context(request)
        context.update({
            'classes': classes,
            'title': 'Student Promotion'
        })
        return render(request, 'admin/students/promotion_form.html', context)

    def get_streams(self, request):
        class_id = request.GET.get('class_id')
        streams = Stream.objects.filter(class_ref_id=class_id)
        options = '<option value="">---------</option>'
        for stream in streams:
            options += f'<option value="{stream.id}">{stream.name}</option>'
        return HttpResponse(options)

    # Custom actions implementation
    def activate_students(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} students activated successfully.")
    activate_students.short_description = "Activate selected students"

    def deactivate_students(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} students deactivated successfully.")
    deactivate_students.short_description = "Deactivate selected students"

    def generate_admission_numbers(self, request, queryset):
        """Action to generate admission numbers for students without them"""
        count = 0
        for student in queryset:
            if not student.admission_number:
                student.save()  # This triggers the admission number generation
                count += 1
        self.message_user(request, f"Admission numbers generated for {count} students.")
    generate_admission_numbers.short_description = "Generate admission numbers"

    def migrate_legacy_numbers(self, request, queryset):
        """Action to copy legacy numbers to admission numbers"""
        count = 0
        for student in queryset:
            if student.legacy_admission_number and not student.admission_number:
                student.admission_number = student.legacy_admission_number
                student.save()
                count += 1
        self.message_user(request, f"Migrated legacy numbers for {count} students.")

    migrate_legacy_numbers.short_description = "Migrate legacy to admission numbers"

    def promote_students(self, request, queryset):
        """Action to promote students to next class"""
        if 'apply' in request.POST:
            target_class_id = request.POST.get('target_class')
            target_stream_id = request.POST.get('target_stream')
            
            if not target_class_id:
                self.message_user(request, "Please select a target class", level='error')
                return
            
            target_class = Class.objects.get(id=target_class_id)
            target_stream = Stream.objects.get(id=target_stream_id) if target_stream_id else None
            
            promoted = 0
            for student in queryset:
                StudentPromotionHistory.objects.create(
                    student=student,
                    from_class=student.class_ref,
                    from_stream=student.stream,
                    to_class=target_class,
                    to_stream=target_stream,
                    reason='Bulk Promotion'
                )
                student.class_ref = target_class
                student.stream = target_stream
                student.save()
                promoted += 1
            
            self.message_user(request, f"{promoted} students promoted successfully.")
            return
        
        # Show intermediate form
        classes = Class.objects.all()
        streams = Stream.objects.none()
        if classes:
            streams = Stream.objects.filter(class_ref=classes[0])
        
        return render(request, 'admin/students/promote_intermediate.html', {
            'students': queryset,
            'classes': classes,
            'streams': streams,
            'title': 'Promote Students'
        })
    promote_students.short_description = "Promote selected students"

    def export_selected_students(self, request, queryset):
        """Custom export action for selected students"""
        dataset = self.resource_class().export(queryset)
        format = base_formats.XLSX()
        export_data = format.export_data(dataset)
        content_type = format.get_content_type()
        response = HttpResponse(export_data, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename=students_export_{timezone.now().date()}.xlsx'
        return response
    export_selected_students.short_description = "Export selected students"
    
@admin.register(StudentPromotionHistory)
class PromotionHistoryAdmin(admin.ModelAdmin):
    list_display = ("student", "from_class", "to_class", "from_stream", "to_stream", "reason", "timestamp")
    list_filter = ("from_class", "to_class", "timestamp")