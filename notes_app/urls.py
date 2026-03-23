from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('units/', views.units_view, name='units'),
    path('notes/', views.notes_view, name='notes'),
    path('notes/unit/<int:unit_id>/', views.notes_view, name='notes_by_unit'),
    path('notes/<int:note_id>/', views.note_detail_view, name='note_detail'),
    path('groups/', views.groups_view, name='groups'),
    path('groups/unit/<int:unit_id>/', views.groups_view, name='groups_by_unit'),
    path('students/', views.students_view, name='students'),
    path('announcements/', views.announcements_view, name='announcements'),
    path('reminders/', views.reminders_view, name='reminders'),
    path('reminders/<int:reminder_id>/done/', views.mark_reminder_done, name='mark_reminder_done'),
]
