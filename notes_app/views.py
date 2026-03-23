from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from .models import Unit, Student, Note, Group, Announcement, Reminder
from .forms import RegisterForm, ReminderForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'notes_app/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to IN16 Study Manager, {user.first_name}!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'notes_app/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    announcements = Announcement.objects.all()[:5]
    units = Unit.objects.all()
    notes_count = Note.objects.count()
    students_count = Student.objects.count()
    upcoming_reminders = []
    try:
        student = request.user.student
        upcoming_reminders = Reminder.objects.filter(
            student=student,
            reminder_time__gte=timezone.now(),
            is_done=False
        )[:3]
    except Student.DoesNotExist:
        pass
    context = {
        'announcements': announcements,
        'units': units,
        'notes_count': notes_count,
        'students_count': students_count,
        'upcoming_reminders': upcoming_reminders,
    }
    return render(request, 'notes_app/home.html', context)


@login_required
def units_view(request):
    units = Unit.objects.prefetch_related('notes', 'groups').all()
    return render(request, 'notes_app/units.html', {'units': units})


@login_required
def notes_view(request, unit_id=None):
    units = Unit.objects.all()
    selected_unit = None
    notes = Note.objects.select_related('unit').all()
    if unit_id:
        selected_unit = get_object_or_404(Unit, id=unit_id)
        notes = notes.filter(unit=selected_unit)
    return render(request, 'notes_app/notes.html', {
        'units': units,
        'notes': notes,
        'selected_unit': selected_unit,
    })


@login_required
def note_detail_view(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, 'notes_app/note_detail.html', {'note': note})


@login_required
def groups_view(request, unit_id=None):
    units = Unit.objects.all()
    selected_unit = None
    groups = Group.objects.prefetch_related('members__user').select_related('unit').all()
    if unit_id:
        selected_unit = get_object_or_404(Unit, id=unit_id)
        groups = groups.filter(unit=selected_unit)
    return render(request, 'notes_app/groups.html', {
        'units': units,
        'groups': groups,
        'selected_unit': selected_unit,
    })


@login_required
def students_view(request):
    query = request.GET.get('q', '')
    gender = request.GET.get('gender', '')
    students = Student.objects.select_related('user').all()
    if query:
        students = students.filter(
            reg_number__icontains=query
        ) | students.filter(
            user__first_name__icontains=query
        ) | students.filter(
            user__last_name__icontains=query
        )
    if gender:
        students = students.filter(gender=gender)
    return render(request, 'notes_app/students.html', {
        'students': students,
        'query': query,
        'gender': gender,
        'total': Student.objects.count(),
    })


@login_required
def announcements_view(request):
    announcements = Announcement.objects.all()
    return render(request, 'notes_app/announcements.html', {'announcements': announcements})


@login_required
def reminders_view(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        messages.warning(request, 'No student profile found for your account.')
        return redirect('home')

    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.student = student
            reminder.save()
            messages.success(request, 'Reminder set successfully!')
            return redirect('reminders')
    else:
        form = ReminderForm()

    reminders = Reminder.objects.filter(student=student).select_related('unit', 'note')
    upcoming = reminders.filter(reminder_time__gte=timezone.now(), is_done=False)
    past = reminders.filter(reminder_time__lt=timezone.now()) | reminders.filter(is_done=True)

    return render(request, 'notes_app/reminders.html', {
        'form': form,
        'upcoming': upcoming,
        'past': past.order_by('-reminder_time')[:10],
    })


@login_required
def mark_reminder_done(request, reminder_id):
    try:
        student = request.user.student
        reminder = get_object_or_404(Reminder, id=reminder_id, student=student)
        reminder.is_done = True
        reminder.save()
        messages.success(request, 'Reminder marked as done.')
    except Student.DoesNotExist:
        pass
    return redirect('reminders')
