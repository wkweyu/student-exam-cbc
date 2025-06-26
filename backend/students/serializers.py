from rest_framework import serializers
from .models import Student, Class, Stream
from rest_framework import serializers
import re
from datetime import datetime


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class StreamSerializer(serializers.ModelSerializer):
    class_ref = ClassSerializer(read_only=True)
    class_ref_id = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all(), write_only=True, source='class_ref')

    class Meta:
        model = Stream
        fields = ['id', 'name', 'class_ref', 'class_ref_id']



class StudentSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['admission_number']

    def validate_guardian_contact(self, value):
        if not re.match(r'^(\+254|254|0)?(7\d{8}|1\d{8})$', value):
            raise serializers.ValidationError("Enter a valid Kenyan mobile number (e.g., 07XXXXXXXX or 01XXXXXXXX).")
        return value

    def create(self, validated_data):
        # Auto-generate admission number if not provided
        if not validated_data.get('admission_number'):
            year = datetime.now().year
            last_student = Student.objects.filter(admission_number__startswith=str(year)).order_by('-id').first()
            next_id = 1 if not last_student else int(last_student.admission_number[-4:]) + 1
            validated_data['admission_number'] = f"{year}{next_id:04d}"
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Optional: prevent admission number updates
        validated_data.pop('admission_number', None)
        return super().update(instance, validated_data)

        
class StudentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name',
            'date_of_birth', 'class_ref', 'stream',
            'guardian_name', 'guardian_contact', 'address'
        ]
        extra_kwargs = {
            'admission_number': {'required': False}
        }
    def validate(self, data):
        class_ref = data.get('class_ref')
        stream_ref = data.get('stream_ref')

        if stream_ref and class_ref:
            if stream_ref.class_ref != class_ref:
                raise serializers.ValidationError({
                    'stream_ref': "Selected stream does not belong to the selected class."
                })

        return data
