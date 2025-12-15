from django import forms
from .models import Post, Comentario, Categoria

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-chaco-green',
                'rows': 4,
                'placeholder': 'Escribe tu comentario...'
            })
        }

class CrearPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'subtitulo', 'categoria', 'texto', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-chaco-green',
                'placeholder': 'Título del post'
            }),
            'subtitulo': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-chaco-green',
                'placeholder': 'Subtítulo (opcional)'
            }),
            'categoria': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-chaco-green'
            }),
            'texto': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-chaco-green',
                'rows': 12,
                'placeholder': 'Contenido del post'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'hidden',
                'id': 'file-upload'
            })
        }

class NuevaCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-chaco-green',
                'placeholder': 'Ej: Naturaleza, Cultura, etc.'
            })
        }