from rest_framework import serializers
from .models import Task, User, Family, Composite, QuickTask

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'

class CompositeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composite
        fields = '__all__'

class QuickTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickTask
        fields = "__all__"