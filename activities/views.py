from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
#funcionalidad de formularios de registro y login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#Se importa el modelo de usuarios
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
#El login_required funciona para proteger cada ruta, es decir, solo los usuarios
#autenticados pueden ingresar a ell
from django.contrib.auth.decorators import login_required



def signup(request):
    #Si el cliente entra a la vista se renderiza el formulario
    if request.method == 'GET':
          #El metodo render recibe 3 parametros, la request, el html a renderizar
    #y se le pueda pasar una data para que el html la consuma
         return render(request,'signup.html',{
        'form': UserCreationForm
    })
    if request.method == 'POST':
        if request.POST['username'] and request.POST['password1'] and request.POST['password2']:

         if request.POST['password1'] == request.POST['password2']:
           
           try:
               #Para registrar al usuario, el metodo create_user necesita 2 argumentos
               #el nombre de usuario y la contraseña
               user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
               #Se guarda el objeto del usuario en la base de datos
               user.save()
               #Una vez creado el usuario, se va a establecer una cookie
               #con la informacion del mismo
               login(request, user)
               #Redirige al usuario a la vista tasks
               return redirect('tasks')
           except IntegrityError :
                return render(request,'signup.html',{
                'form': UserCreationForm,
                'error':'El usuario ya existe'

            })
               
         else:
            return render(request,'signup.html',{
                'form': UserCreationForm,
                'error':'Las contraseñas no coinciden'

            })
        else:
            return render(request,'signup.html',{
                'form': UserCreationForm,
                'error':"Debes rellenar todos los campos"
            })
        
@login_required
def signout(request):
    #El metodo logout recibe la peticion del cliente
    logout(request)
    return redirect('signup')

def signin(request):
    if request.method == 'GET':
        return render(request,'login.html',{
        'form': AuthenticationForm
        })
    
    if request.method == 'POST':
         if request.POST['username'] and request.POST['password']:
            #El metodo authenticate verifica si el usuario y contraseña son validas,
            #recibe 2 parametros, la request, y el username y password
           user = authenticate(
             request, username=request.POST['username'], 
             password = request.POST['password'])
         
         #El if se ejecuta si no existe el usuario
           if user is None:
             return render (request,'login.html',{
                 'form': AuthenticationForm,
                 'error':'Las credenciales no son validas'
             })
           else:
             login(request,user)
             #si existe se redirige a la ruta tasks
             return redirect('tasks')
         else:
             return render(request,'login.html',{
                 'form':AuthenticationForm,
                 'error':'Debes de rellenar todos los campos'
             })

@login_required
def create_task(request):
    if request.method == 'GET':
         return render(request,'create_task.html',{
             'form':TaskForm
         })
    else:

        if request.POST['title'] and request.POST['description']:
           try:
        #Se crea un formulario TaskForm con los datos que vienen desde el cliente
               form = TaskForm(request.POST)
         #El commit en false es para la crecion de la instancia Task
         #pero sin que se guarde en la base de datos aun
               new_task = form.save(commit=False)
         #Se obtiene al usuario que hizo la peticion de crear tarea y se modifica
         #la instancia
               new_task.user = request.user
        #Se crea una nueva tarea con los datos del formulario
               new_task.save()
               return redirect('tasks')
           except:
            return render(request,'create_task.html',{
                'form':TaskForm,
                'error':'Por favor ingresa datos validos'
            })
        else:
            return render(request,'create_task.html',{
                'form':TaskForm,
                'error':"Debes de rellenar todos los campos"
            })
               


@login_required
def tasks(request):
     #Se obtienen las tareas del usuario que hace la peticion y las que aun
     #no estan completadas
     tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True).order_by('-important')
     for task in tasks:
         print(task.title)
         print(task.user)
     return render(request,'tasks.html',{
            'tasks':tasks,
            'user': request.user
        })


@login_required
#task_id es el valor de la variable que recibe la ulr que renderiza task_details
def task_details(request, task_id):
        if request.method == 'GET':
          #este metodo busca en el modelo Task una tarea que en su propiedad primarykey
          #sea igual al valor de task_id que viene de la url y y que sea del usuario que 
          #esta autenticado, si no la encuentra, regresa un 404
          task = get_object_or_404(Task,pk=task_id, user=request.user)
          #El formulario de task se visualiza con los valores que guardo la variable task,
          #que es la que obtiene una tarea por su pk
          form = TaskForm(instance=task)
          return render(request,'task_detail.html',{
            'task': task,
            'form':form
           })
        else:
            try:
               #Se busca esa tarea para poder actualizarla
                task = get_object_or_404(Task,pk=task_id)
               #Con los valores del request.POST,se actualiza la tarea que se a encontrado en task
                form = TaskForm(request.POST,instance=task)
               #Se guarda esa actualizacion
                form.save()
                return redirect('tasks')
            except ValueError:
                return render(request,'task_detail.html',{
               'task': task,
               'form':form,
               'error':'Ocurrio un error al actualizar la tarea'
           })

@login_required
def complete_task(request,task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task,pk=task_id, user=request.user)
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def task_eliminated(request,task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task,pk=task_id, user=request.user)
        task.delete()
        return redirect('tasks')

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'tasks_completed.html',{
        'tasks':tasks
    })


   
  
       
   


    
   
