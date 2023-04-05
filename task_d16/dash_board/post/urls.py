from django.urls import path
from .views import *



urlpatterns = [
    path('', PostList.as_view(), name='post_all'),
    path('post/<int:pk>', PostDetail.as_view(), name='post_id'),
    path('create/', AddPostView.as_view(), name='post_create'),
    path('delete/<int:pk>', DeletePostView.as_view(), name='post_delete'),
    path('<int:pk>/update/', UpdatePostView.as_view(), name='post_update'),
    path('my_post/', MyPostView.as_view, name='my_post'),
    path('comment/<int:pk>', CommentDetail.as_view(), name='comment_id'),
    path('comment/<int:pk>/delete', CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/<int:pk>/approve', comment_approve, name='comment_approve'),
    path('category/<int:pk>', CatListView.as_view(), name='category_list'),
    path('category/<int:pk>/subscribe', subscribe, name='subscribe'),
]
