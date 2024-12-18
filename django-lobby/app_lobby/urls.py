from django.urls import path
from django.contrib import admin
from django.urls import path, include
from .api import FamilyTasksViewSet, TaskViewSet, FamilyViewSet, QuickTaskViewSet

urlpatterns = [
    path('tasks/', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-list'),
    path('tasks/<int:pk>/', TaskViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='task-detail'),

    path('quickTasks/', QuickTaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='QuickTask-list'),
    path('quickTasks/<int:pk>/', QuickTaskViewSet.as_view({'delete': 'destroy'}), name='QuickTask-detail'),
    
    path('family/', FamilyViewSet.as_view({'get': 'list', 'post': 'create'}), name='family-list'),
    path('family/<int:pk>/', FamilyViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='family-detail'),
    # Otras rutas...
]  