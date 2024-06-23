"""
URL configuration for tasks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from activities import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('logout/', views.signout, name='logout'),
    path('login/', views.signin, name='login'),
    path('create_task/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.task_details, name='task_details'),
    path('tasks/<int:task_id>/completed', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/eliminated', views.task_eliminated, name='task_eliminated'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),

]
