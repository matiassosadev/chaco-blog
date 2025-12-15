from django.shortcuts import redirect, render
from .models import Post, Comentario, Categoria 
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ComentarioForm, CrearPostForm, NuevaCategoriaForm
from django.urls import reverse_lazy, reverse
from django.contrib import messages

# Vista para el index
def index(request):
    posts = Post.objects.all().order_by('-fecha')[:3] 
    return render(request, 'index.html', {'posts': posts})

class PostListView(ListView):
    model = Post
    template_name = "posts/posts.html"
    context_object_name = "posts"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        orden = self.request.GET.get('orden')
        if orden == 'reciente':
            queryset = queryset.order_by('-fecha')
        elif orden == 'antiguo':
            queryset = queryset.order_by('fecha')
        elif orden == 'alfabetico':
            queryset = queryset.order_by('titulo')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orden'] = self.request.GET.get('orden', 'reciente')
        # ✅ Corrección para enviar la lista de categorías
        context['categorias'] = Categoria.objects.all() 
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_individual.html"
    context_object_name = "posts"
    pk_url_kwarg = "id"
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComentarioForm()
        context['comentarios'] = Comentario.objects.filter(posts_id=self.kwargs['id']).order_by('-fecha')
        return context

    def post(self, request, *args, **kwargs): 
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.posts_id = self.kwargs['id']
            comentario.save()
            return redirect('apps.posts:post_individual', id=self.kwargs['id'])
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
        
class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentario/agregarComentario.html'
    success_url = 'comentario/comentarios/'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.posts_id = self.kwargs['posts_id']
        return super().form_valid(form)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CrearPostForm
    template_name = 'posts/crear_post.html'
    success_url = reverse_lazy('apps.posts:posts')
    
    def form_valid(self, form):
        form.instance.autor = self.request.user  # Asignar el usuario como autor
        messages.success(self.request, '¡Post creado exitosamente!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear el post. Revisa los campos.')
        return super().form_invalid(form)

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = NuevaCategoriaForm
    template_name = 'posts/crear_categoria.html'
    
    def form_valid(self, form):
        messages.success(self.request, f'Categoría "{form.instance.nombre}" creada exitosamente!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear la categoría.')
        return super().form_invalid(form)
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('apps.posts:crear_post')
        
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'posts/categoria_list.html'
    context_object_name = 'categorias'

class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'posts/categoria_confirm_delete.html'
    success_url = reverse_lazy('apps.posts:categoria_list')

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = CrearPostForm
    template_name = 'posts/modificar_post.html'
    success_url = reverse_lazy('apps.posts:posts')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/eliminar_post.html'
    success_url = reverse_lazy('apps.posts:posts')

class ComentarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentario/comentario_form.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('apps.posts:post_individual', args=[self.object.posts.id])
        
class ComentarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Comentario
    template_name = 'comentario/comentario_confirm_delete.html'

    def get_success_url(self):
        return reverse('apps.posts:post_individual', args=[self.object.posts.id])
    
class PostsPorCategoriaView(ListView):
    model = Post
    template_name = 'posts/posts_por_categoria.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(categoria_id=self.kwargs['pk'])