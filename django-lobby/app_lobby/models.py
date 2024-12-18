from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from polymorphic.models import PolymorphicModel

class User(AbstractUser):
    
    TotalTareasPendientes = models.IntegerField(default=0)
    TotalTareasEnProceso = models.IntegerField(default=0)
    TotalTareasCompletadas = models.IntegerField(default=0)

    TareasPendientes = models.ManyToManyField('Task', related_name='TareasPendientes')
    TareasEnProceso = models.ManyToManyField('Task', related_name='TareasEnProceso')
    TareasCompletadas = models.ManyToManyField('Task', related_name='TareasCompletadas')

    puntos = models.IntegerField(default=0)

    nivel = models.IntegerField(default=1)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this player."""
        return reverse('user-detail', args=[str(self.id)])
    
    def finish_Task(self, task):
        self.TotalTareasCompletadas += 1
        self.TotalTareasEnProceso -= 1
        self.TareasEnProceso.remove(task)
        self.TareasCompletadas.add(task)
        self.puntos += task.puntosDeExperiencia
        self.save()
    
    def añadir_puntos(self, puntos):
        self.puntos += puntos
        #definir los diferentes niveles
        if self.puntos >= 100:
            self.nivel = 2
        if self.puntos >= 500:
            self.nivel = 3
        if self.puntos >= 1000:
            self.nivel = 4
        if self.puntos >= 2000:
            self.nivel = 5
        if self.puntos >= 5000:
            self.nivel = 6
        self.save()

    def __str__(self):
        return f"{self.username}-{self.nivel}"
    
class QuickTask(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False, default="Quick Task")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_creator")
    
    class Type(models.TextChoices):
        MONTH = 'MONTH'
        DAY = 'DAY'
        NONE = 'NONE'
    
    type = models.CharField(max_length=6, choices=Type.choices, default=Type.NONE)

    def __str__(self):
        return f"{self.title}"
    
    def get_absolute_url(self):
        return reverse('QuickTask-detail', args=[str(self.id)])


# Modelo abstracto que define la estructura básica del Composite
class Composite(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False, default="No title")
    description = models.TextField(max_length=500, blank=False, null=False, default="No description")

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

# Modelo para Tareas individuales
class Task(Composite):
    fecha = models.DateField(blank=False, null=True)
    hora = models.TimeField(blank=False, null=True)
    puntosDeExperiencia = models.IntegerField(default=0)
    location = models.CharField(max_length=100, blank=True, null=True)
    acompanantes = models.ManyToManyField(User, blank=True, related_name='acompañantes')
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_task', default=1)
    family = models.ForeignKey('Family', on_delete=models.CASCADE, null=True, blank=True)

    class Status(models.TextChoices):
        TODO = 'TODO'
        DOING = 'DOING'
        DONE = 'DONE'
        PAUSED = 'PAUSED'
    
    status = models.CharField(max_length=6, choices=Status.choices, default=Status.TODO)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('task-detail', args=[str(self.id)])

# Modelo para Familias de tareas
class Family(Composite):
    # Relación ManyToMany con tareas (Task)
    tasks = models.ManyToManyField(Task, blank=True, related_name='tasks')
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_family', default=1)
        # Relación recursiva donde una familia (Family) puede tener un padre que también es Family.
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    color = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('family-detail', args=[str(self.id)])

    # Método para agregar una tarea o subfamilia a esta familia
    def add_child(self, child: Composite):
        if isinstance(child, Task):
            self.tasks.add(child)
        elif isinstance(child, Family):
            child.parent = self
            child.save()

    # Método para listar todas las tareas y subfamilias de forma recursiva
    def get_all_tasks(self):
        tasks = list(self.tasks.all())
        for child_family in self.children.all():  # Recursión para obtener tareas de subfamilias
            tasks.extend(child_family.get_all_tasks())
        return tasks
    
    # metodo para añadir una tarea a la familia
    def add_task(self, task):
        self.tasks.add(task)
        self.save()