from django.db import models

# Create your models here.
class Usuario():
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    fecha_registro = models.DateField(auto_now_add=True)
    usuario = models.CharField(max_length=50)
    def __str__(self):
        return self.usuario

class Ocasion():
    id_ocasion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class Grupo():
    id_grupo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre

class Filtros():
    id_filtro = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
    
class Receta():
    id_receta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    grupo = models.ForeignKey(Grupo,on_delete=models.CASCADE)
    comensales = models.CharField(max_length=50)
    duracion = models.CharField(max_length=50)
    ocasion = models.ForeignKey(Ocasion,on_delete=models.CASCADE)
    dificultad = models.CharField(max_length=50)
    ingredientes = models.TextField()
    preparacion = models.TextField()
    imagen = models.ImageField()
    filtros = models.ManyToManyField(Filtros,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre
    
