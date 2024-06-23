from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#Se define una tabla en la base de datos nombrada Task y contiene los
#siguientes campos
class Task(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    created=models.DateTimeField(auto_now_add=True)
    datecompleted=models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    #ForeignKey crea una relacion de muchos a uno con el modelo User
    #es decir, que cada tarea estara asociada a un usuario
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        #Es para que aparezca solo el titulo de la tarea y no el object
            return self.title + ' - ' + self.user.username
     
