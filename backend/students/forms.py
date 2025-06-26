from django import forms
from .models import Student
from django.utils import timezone

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['admission_number']
        widgets = {
            'date_of_birth':forms.DateInput(attrs={'type':'date'}),
        }
        fields = '__all__'  # Or list fields like ['first_name', 'class_ref', 'stream_ref', ...]
    def clean_admission_number(self):
            admission_number = self.cleaned_data['admission_number']
            # Example format: ADM-0001
            if not re.match(r'^ADM-\d{4}$', admission_number):
                raise forms.ValidationError("Admission number must be in the format ADM-0001.")
            return admission_number



class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'middle_name', 'last_name',
            'date_of_birth', 'gender', 'photo',
            'class_ref', 'stream', 'date_admitted',
            'guardian_name', 'guardian_contact',
            'guardian_email', 'address', 'emergency_contact',
            'admission_number'  # Optional: allow setting during import
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_admitted': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Admission number is optional if not importing
        self.fields['admission_number'].required = False

    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('date_of_birth')

        if dob and dob > timezone.now().date():
            self.add_error('date_of_birth', "Date of birth cannot be in the future.")

        return cleaned_data
