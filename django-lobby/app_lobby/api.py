from djoser.views import TokenCreateView
from djoser.conf import settings
from rest_framework import mixins, viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Task, Family, Composite, QuickTask
from .serializers import CompositeSerializer, TaskSerializer, FamilySerializer, QuickTaskSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


class MyTokenCreateView(TokenCreateView):
    def _action(self, serializer):
        response = super()._action(serializer)
        tokenString = response.data['auth_token']
        tokenObject = settings.TOKEN_MODEL.objects.get(key=tokenString)
        response.data['user_id'] = tokenObject.user_id
        return response

class FamilyViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    serializer_class = FamilySerializer
    def get_queryset(self):
        return Family.objects.filter(creador=self.request.user)
    
    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        family = serializer.save(creador=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        family = get_object_or_404(self.get_queryset(), pk=pk)
        if family.creador != request.user:
            raise ValidationError("You can't delete this family")
        family.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, pk=None):
        family = get_object_or_404(self.get_queryset(), pk=pk)
        if family.creador != request.user:
            raise ValidationError("You can't update this family")
        serializer = self.serializer_class(family, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    
#PROBLEMAS CON CREAR LA TAREAS
class FamilyTasksViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        # Return tasks in the task list of pk family, the endpoint is /family/<int:pk>/tasks/
        family = get_object_or_404(Family, pk=self.kwargs['pk'])
        return family.get_all_tasks()
    
    def list(self, request, pk=None):
        #listar las tareas de la familia con id=pk
        task_serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(task_serializer.data)

    def create(self, request, pk=None):
        #crear una tarea en la familia con id=pk
        family = get_object_or_404(Family, pk=self.kwargs['pk'])
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(creador=request.user)
        family.add_task(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    
class TaskViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(creador=self.request.user)

    def list(self, request):
        """ queryset = self.queryset.filter(creador=request.user) """
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(creador=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        task = get_object_or_404(self.get_queryset(), pk=pk)
        if task.creador != request.user:
            raise ValidationError("You can't delete this task")
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, pk=None):
        task = get_object_or_404(self.get_queryset(), pk=pk)
        if task.creador != request.user:
            raise ValidationError("You can't update this task")
        serializer = self.serializer_class(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class QuickTaskViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = QuickTaskSerializer

    def get_queryset(self):
        return QuickTask.objects.filter(creator=self.request.user)

    def list(self, request):
        """ queryset = self.queryset.filter(creador=request.user) """
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        quickTask = serializer.save(creator=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        QuickTask = get_object_or_404(self.get_queryset(), pk=pk)
        if QuickTask.creator != request.user:
            raise ValidationError("You can't delete this task")
        QuickTask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
