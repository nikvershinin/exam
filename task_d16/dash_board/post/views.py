from .models import *
from .filters import *
from django.views.generic import ListView


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
