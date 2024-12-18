from django.shortcuts import render
from .models import Task, User, Family, QuickTask
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

def index(request):
    return render()

class QuickTaskListView(ListView):
    model = QuickTask
    ordering = ['id']

class QuickTaskDetailView(DetailView):
    model = QuickTask

class QuickTaskCreateView(CreateView):
    model = QuickTask
    fields = ['title', 'type']

# Views for Tasks -------------------------------------------------------------------------------------

class TaskListView(ListView):
    model = Task
    ordering = ['id']

class TaskDetailView(DetailView):
    model = Task

class TaskCreateView(CreateView):
    model = Task
    fields = ['title', 'description', 'fecha', 'hora', 'puntosDeExperiencia', 'acompanantes', 'status']

# Views for Users ---------------------------------------------------------------------------------------

class UserListView(ListView):
    model = User
    ordering = ['id']

class UserDetailView(DetailView):
    model = User

class UserCreateView(CreateView):
    model = User
    fields = ['username', 'email', 'password']

# Views for Families ---------------------------------------------------------------------------------------

class FamilyListView(ListView):
    model = Family
    ordering = ['id']

class FamilyDetailView(DetailView):
    model = Family

class FamilyCreateView(CreateView):
    model = Family
    fields = ['tasks', 'creador', 'parent', 'color', 'title', 'description']

