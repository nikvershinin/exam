from django.views.generic import ListView, CreateView, DetailView
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

class AddPost(SuccessMessageMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = "post/add_post.html"
    success_message = "Added Succesfully"

    def get_success_url(self):
        return reverse('')