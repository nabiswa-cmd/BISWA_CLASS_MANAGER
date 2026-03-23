"""
Run this after migrations to seed sample data:
  python seed_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IN16_Study_Manager.settings')
django.setup()

from django.contrib.auth.models import User
from notes_app.models import Unit, Student, Note, Group, Announcement

print("Seeding data...")

# Units
units_data = [
    "Operating Systems (COMP113)",
    "Computer Architecture (COMP100)",
    "System Analysis and Design (SOEN112)",
    "Structure Programming in C (SOEN102)",
    "Calculus 1 (MATH111)",
    "Introductory Electronics (PHY213)",
]
units = []
for u in units_data:
    unit, _ = Unit.objects.get_or_create(name=u)
    units.append(unit)
print(f"  ✓ {len(units)} units")

# Superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@in16.ac.ke', 'admin123')
    print("  ✓ Superuser: admin / admin123")

# Sample students
students_data = [
    ('IN16/00034/25', 'Kevin', 'Kiptoo', 'M'),
    ('IN16/00031/25', 'Lynette', 'Chepkemoi', 'F'),
    
]
student_objects = []
for reg, first, last, gender in students_data:
    username = first.lower() + last.lower()
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username, f'{first.lower()}@in16.ac.ke', 'pass1234', first_name=first, last_name=last)
        student = Student.objects.create(user=user, reg_number=reg, gender=gender)
        student_objects.append(student)
    else:
        student_objects.append(Student.objects.get(reg_number=reg))
print(f"  ✓ {len(student_objects)} students (password: pass1234)")

# Notes
notes_data = [
    (units[0], "Introduction to Python", "Python is a high-level, interpreted language known for its readability and simplicity.\n\nKey topics:\n- Variables and data types\n- Control flow (if/else, loops)\n- Functions and modules\n- Object-Oriented Programming basics\n\nPython uses indentation to define code blocks instead of curly braces."),
    (units[0], "Control Flow Statements", "Control flow determines the order in which statements are executed.\n\nif/elif/else:\n  Used for conditional execution.\n\nfor loops:\n  Iterate over sequences.\n\nwhile loops:\n  Execute while a condition is true.\n\nbreak, continue, pass:\n  Used to control loop execution."),
    (units[1], "Arrays and Linked Lists", "Arrays store elements in contiguous memory locations.\n- Access: O(1)\n- Insertion/Deletion: O(n)\n\nLinked Lists store elements in nodes with pointers.\n- Access: O(n)\n- Insertion/Deletion: O(1) if at head\n\nChoose based on your use case!"),
    (units[2], "SQL Basics", "SQL (Structured Query Language) is used to communicate with databases.\n\nCore commands:\n- SELECT: retrieve data\n- INSERT: add new records\n- UPDATE: modify existing records\n- DELETE: remove records\n- CREATE TABLE: define new tables\n\nExample:\nSELECT * FROM students WHERE gender = 'F';"),
    (units[3], "OSI Model", "The OSI model has 7 layers:\n1. Physical\n2. Data Link\n3. Network\n4. Transport\n5. Session\n6. Presentation\n7. Application\n\nMnemonic: Please Do Not Throw Sausage Pizza Away"),
    (units[4], "SDLC Phases", "Software Development Life Cycle phases:\n1. Requirements gathering\n2. System design\n3. Implementation (coding)\n4. Testing\n5. Deployment\n6. Maintenance\n\nModels: Waterfall, Agile, Spiral, V-Model"),
]
for unit, topic, content in notes_data:
    Note.objects.get_or_create(unit=unit, topic=topic, defaults={'content': content})
print(f"  ✓ {len(notes_data)} notes")

# Groups
if student_objects:
    g1, _ = Group.objects.get_or_create(name="Group 3 SOEN112", unit=units[0])
    g1.members.set(student_objects[:4])
    g2, _ = Group.objects.get_or_create(name="Group 1 COMP113", unit=units[0])
    g2.members.set(student_objects[4:])
    g3, _ = Group.objects.get_or_create(name="GROUP 3 MATH113", unit=units[1])
    g3.members.set(student_objects[::2])
    print("  ✓ 3 groups")

# Announcements
ann_data = [
    ("Welcome to IN16 Study Manager", "Welcome to the official IN16 class study management platform. Use this system to access notes, connect with your group, and stay updated with class announcements. Best of luck this semester!"),
    ("CAT 1 Schedule Released", "The Continuous Assessment Test 1 schedule has been released. Please check your unit timetables and prepare accordingly. CATs will begin in Week 6."),
    ("Group Assignments Posted", "Study group assignments for all units have been posted. Please check the Groups section to see your assigned group members."),
]
for title, content in ann_data:
    Announcement.objects.get_or_create(title=title, defaults={'content': content})
print(f"  ✓ {len(ann_data)} announcements")

print("   Admin panel: http://127.0.0.1:8000/admin/ (admin / admin123)")
print("   Student login: NABISWAJAMES / pass1234")
