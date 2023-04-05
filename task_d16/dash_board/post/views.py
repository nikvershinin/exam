from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
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

    success_url = ''

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

class MyPostView(ListView):
    model = Post
    template_name = 'post/my_post.html'
    context_object_name = 'my_post'
    ordering = ['-dateCreation']
    paginate_by = 10

    def get_queryset(self):
        author = Author.objects.get(name=self.request.user)
        queryset = Post.objects.filter(post__author=author)
        return queryset

class CommentDetail(DetailView):
    model = Comment
    template_name = 'post/comment_id.html'
    context_object_name = 'comment_id'
    queryset = Comment.objects.all()

class CommentDeleteView(DetailView, LoginRequiredMixin):
    model = Comment
    template_name = 'post/comment_delete.html'
    queryset = Comment.objects.all()
    success_url = ''

def comment_approve(request, pk):
    obj = Comment.objects.get(id=pk)
    obj.status = True
    obj.save()
    return redirect('/my_comments')

class CatListView(ListView):
    model = Post
    template_name = 'post/category_list.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.category).order_by('-dateCreation')
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'post/subscribe.html', {'category': category, 'message': message})