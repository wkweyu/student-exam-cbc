from rest_framework import viewsets,filters,generics,status, permissions, parsers
from .models import Student, Class, Stream,StudentPromotionHistory
from .serializers import StudentSerializer, ClassSerializer, StreamSerializer,StudentRegistrationSerializer
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm,StudentForm
from rest_framework.parsers import MultiPartParser, FormParser
from django.views import View
from django.utils.crypto import get_random_string
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StudentSerializer
from django.http import JsonResponse,Http404
from students.models import GRADE_LEVELS
from django.views.decorators.http import require_http_methods




#1
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['first_name','last_name','admission_number','guardian_name']
    ordering_fields = ['admission_number','created_at']
#2
class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
#3
class StreamViewSet(viewsets.ModelViewSet):
    queryset = Stream.objects.all()  # <-- ADD this line
    serializer_class = StreamSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        class_id = self.request.query_params.get('class_id')
        if class_id:
            queryset = queryset.filter(class_ref__id=class_id)
        return queryset


#4
class StudentRegistrationView(APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student registered successfully", "student": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#5
class StudentDetailView(generics.RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    parser_classes = [MultiPartParser, FormParser]  # Accept multipart/form-data

@login_required
def student_register_page(request):
    classes = Class.objects.all()
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(
                request,
                f"Student '{student.full_name()}' registered successfully with admission number: {student.admission_number}"
            )
            return redirect('student-register-form')
    else:
        form = StudentForm()

    return render(request, 'students/register_student.html', {
        'form': form,
        'classes': classes
    })


def student_list(request):
    query = request.GET.get('q', '')
    students = Student.objects.all()
    if query:
        students = students.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(admission_number__icontains=query)
        )
    return render(request, 'students/student_list.html', {'students': students, 'query': query})


#6
class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 20  # Optional: paginate results

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = super().get_queryset().select_related('class_ref', 'stream')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(admission_number__icontains=query)
            )
        return queryset.order_by('last_name', 'first_name')

#7
class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    
    def get_success_url(self):
        return reverse_lazy('student_detail', kwargs={'pk': self.object.pk})


def promote_class_students(request, class_id):
    source_class = get_object_or_404(Class, id=class_id)
    next_year = source_class.year + 1

    # Try finding the next grade level
    current_index = [x[0] for x in GRADE_LEVELS].index(source_class.grade_level)
    try:
        next_grade = GRADE_LEVELS[current_index + 1][0]
    except IndexError:
        messages.error(request, "This is the highest grade level. Promotion not possible.")
        return redirect('class_list')

    # Create or get next class
    next_class, _ = Class.objects.get_or_create(grade_level=next_grade, year=next_year)

    # Migrate each student
    students = Student.objects.filter(class_ref=source_class)
    for student in students:
        from_stream = student.stream
        to_stream = Stream.objects.filter(class_ref=next_class, name=from_stream.name).first()

        # Promote
        history = StudentPromotionHistory.objects.create(
            student=student,
            from_class=student.class_ref,
            from_stream=student.stream,
            to_class=next_class,
            to_stream=to_stream,
            reason='Promotion'
        )
        student.class_ref = next_class
        student.stream = to_stream
        student.save()

    messages.success(request, f"Students from {source_class} promoted to {next_class}.")
    return redirect('student_list')

def transfer_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        new_class_id = request.POST.get('class_id')
        new_stream_id = request.POST.get('stream_id')
        reason = request.POST.get('reason', 'Transfer')

        to_class = get_object_or_404(Class, id=new_class_id)
        to_stream = get_object_or_404(Stream, id=new_stream_id)

        StudentPromotionHistory.objects.create(
            student=student,
            from_class=student.class_ref,
            from_stream=student.stream,
            to_class=to_class,
            to_stream=to_stream,
            reason=reason
        )

        student.class_ref = to_class
        student.stream = to_stream
        student.save()

        messages.success(request, "Student transferred successfully.")
        return redirect('student_detail', pk=student.pk)

    return render(request, 'students/transfer_student.html', {
        'student': student,
        'classes': Class.objects.all(),
        'streams': Stream.objects.all(),
    })

# students/views.py

def student_transfer_search(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        results = []

        if query:
            students = Student.objects.filter(
                Q(first_name__icontains=query) |
                Q(middle_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(admission_number__endswith=query)
            )
            for s in students:
                results.append({
                    "id": s.id,
                    "label": f"{s.full_name()} - {s.admission_number}",
                    "value": f"{s.full_name()} - {s.admission_number}"
                })
        return JsonResponse(results, safe=False)

    return render(request, 'students/transfer_search.html')



def get_streams_by_class(request):
    class_id = request.GET.get('class_id')
    streams = Stream.objects.filter(class_ref__id=class_id).values('id', 'name')
    return JsonResponse(list(streams), safe=False)


def student_transfer_or_promote(request):
    students = Student.objects.select_related('class_ref', 'stream').all()
    classes = Class.objects.all()
    streams = Stream.objects.all()

    if request.method == 'POST':
        if request.POST.get('promote') == 'true':
            # PROMOTION LOGIC
            promoted_students = []
            for student in students:
                stream_key = f'stream_{student.id}'
                new_stream_id = request.POST.get(stream_key)

                if not new_stream_id:
                    continue  # Skip if no stream selected for this student

                # Get next class
                current_class = student.class_ref
                try:
                    current_index = [x[0] for x in GRADE_LEVELS].index(current_class.grade_level)
                    next_grade = GRADE_LEVELS[current_index + 1][0]
                except (ValueError, IndexError):
                    continue  # Cannot promote beyond last grade

                next_year = current_class.year + 1
                next_class, _ = Class.objects.get_or_create(grade_level=next_grade, year=next_year)
                new_stream = Stream.objects.get(id=new_stream_id)

                # Log promotion
                StudentPromotionHistory.objects.create(
                    student=student,
                    from_class=student.class_ref,
                    from_stream=student.stream,
                    to_class=next_class,
                    to_stream=new_stream,
                    reason="Promotion"
                )

                # Update student
                student.class_ref = next_class
                student.stream = new_stream
                student.save()
                promoted_students.append(student)

            messages.success(request, f"{len(promoted_students)} students promoted successfully.")
            return redirect('student_transfer_or_promote')

        # TRANSFER LOGIC
        student_id = request.POST.get('student_id')
        new_class_id = request.POST.get('new_class_id')
        new_stream_id = request.POST.get('new_stream_id')
        reason = request.POST.get('reason', 'Transfer')

        if student_id and new_class_id and new_stream_id:
            student = get_object_or_404(Student, pk=student_id)
            new_class = get_object_or_404(Class, pk=new_class_id)
            new_stream = get_object_or_404(Stream, pk=new_stream_id)

            StudentPromotionHistory.objects.create(
                student=student,
                from_class=student.class_ref,
                from_stream=student.stream,
                to_class=new_class,
                to_stream=new_stream,
                reason=reason
            )

            student.class_ref = new_class
            student.stream = new_stream
            student.save()

            messages.success(request, f"{student.full_name()} transferred successfully.")
            return redirect('student_transfer_or_promote')

    # GET rendering
    next_streams = Stream.objects.all()
    return render(request, 'students/promote_transfer.html', {
        'students': students,
        'classes': classes,
        'streams': streams,
        'next_streams': next_streams,
    })
#Promote students batch
@login_required
@require_http_methods(["GET", "POST"])
def promote_students_batch(request):
    classes = Class.objects.order_by("grade_level", "year")
    streams = Stream.objects.all()
    students = []

    from_class_id = request.GET.get("from_class")
    from_stream_id = request.GET.get("from_stream")

    if request.method == "GET" and from_class_id:
        students = Student.objects.filter(class_ref_id=from_class_id)
        if from_stream_id:
            students = students.filter(stream_id=from_stream_id)
        students = students.select_related("class_ref", "stream")

    elif request.method == "POST":
        student_ids = request.POST.getlist("student_ids")
        to_class_id = request.POST.get("to_class")
        to_stream_id = request.POST.get("to_stream")

        to_class = get_object_or_404(Class, pk=to_class_id)
        to_stream = get_object_or_404(Stream, pk=to_stream_id)

        for sid in student_ids:
            student = Student.objects.get(pk=sid)

            StudentPromotionHistory.objects.create(
                student=student,
                from_class=student.class_ref,
                from_stream=student.stream,
                to_class=to_class,
                to_stream=to_stream,
                reason="Promotion"
            )
            student.class_ref = to_class
            student.stream = to_stream
            student.save()

        messages.success(request, f"{len(student_ids)} students promoted to {to_class} - {to_stream}.")
        return redirect("promote_students_batch")

    return render(request, "students/promote_students_batch.html", {
        "classes": classes,
        "streams": streams,
        "students": students,
        "from_class": request.GET.get("from_class", ""),   # pass selected class for template use
        "from_stream": request.GET.get("from_stream", ""),  # pass selected stream for template use
    })


def get_student_details(request, student_id):
    try:
        student = Student.objects.select_related('class_ref', 'stream').get(id=student_id)
        data = {
            'class': str(student.class_ref) if student.class_ref else None,
            'stream': str(student.stream) if student.stream else None,
            'class_id': student.class_ref.id if student.class_ref else None,
            'stream_id': student.stream.id if student.stream else None,
        }
        return JsonResponse(data)
    except Student.DoesNotExist:
        raise Http404("Student not found")


def test_base(request):
    return render(request, "students/test_base.html")
