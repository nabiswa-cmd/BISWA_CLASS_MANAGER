from django.contrib import admin
from .models import Unit, Student, Note, Group, Announcement, Reminder


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['reg_number', 'get_full_name', 'gender']
    search_fields = ['reg_number', 'user__first_name', 'user__last_name', 'user__username']
    list_filter = ['gender']

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Name'


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['topic', 'unit', 'created_at']
    list_filter = ['unit']
    search_fields = ['topic', 'content']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'member_count']
    list_filter = ['unit']
    filter_horizontal = ['members']

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title', 'content']


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['student', 'unit', 'reminder_time', 'is_done']
    list_filter = ['is_done', 'unit']
    search_fields = ['message', 'student__reg_number']
