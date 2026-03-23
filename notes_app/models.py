from django.db import models
from django.contrib.auth.models import User


class Unit(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Student(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reg_number = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def save(self, *args, **kwargs):
        self.reg_number = self.reg_number.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.reg_number})"

    class Meta:
        ordering = ['reg_number']


class Note(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='notes')
    topic = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.topic} — {self.unit.name}"

    class Meta:
        ordering = ['-created_at']


class Group(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(max_length=100, default='Study Group')
    members = models.ManyToManyField(Student, related_name='groups', blank=True)

    def __str__(self):
        return f"{self.name} ({self.unit.name})"


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Reminder(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='reminders')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.SET_NULL, null=True, blank=True)
    reminder_time = models.DateTimeField()
    message = models.TextField()
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"Reminder: {self.message[:40]} ({self.student})"

    class Meta:
        ordering = ['reminder_time']
