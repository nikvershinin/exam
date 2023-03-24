from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin

from .models import *
from .filters import *
from .forms import *

class PostList(ListView):
    model = Post
    template_name = 'post/post_all.html'
    context_object_name = 'post_all'
    ordering = ['-dateCreation']
    paginate_by = 10

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "filter": self.get_filter(),
        }

class PostDetail(DetailView):
    model = Post
    template_name = 'post/post_id.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

class AddPostView(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    permission_required = ('post.post_create',)
    raise_exception = True
    template_name = "post/post_create.html"
    form_class = PostForm

    def form_valid(self, form):
        user = get_object_or_404(User, username=self.request.user)
        if not Author.objects.filter(authorUser__username=user).exists():#проверка, есть ли связь юзер-автор
            author = Author(authorUser=user)
            author.save()
        form.instance.author = self.request.user.author
        return super().form_valid(form)

class DeletePostView(DetailView, PermissionRequiredMixin):
    permission_required = ('post.post_delete',)
    template_name = 'post/post_delete.html'
    queryset = Post.objects.all()
    success_url = ''

class UpdatePostView(UpdateView, PermissionRequiredMixin):
    permission_required = ('post.post_update',)
    template_name = 'post/post_update.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)