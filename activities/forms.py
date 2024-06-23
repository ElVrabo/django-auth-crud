from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    #Se crea un formulario en base al modelo Task
    class Meta:
        model = Task
        #Solo se crea con los campos title,description e important
        fields = ['title','description','important']
        #Esta propiedad sirve para agregar estilos al formulario que creamos
        #sin manipular el html
        widgets = {
            #El input title del formulario se le agrega una clase de bootstrap
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input mt-1'})
        }