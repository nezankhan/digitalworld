from django.urls import path
from . import views
from . views import (
    PostDeleteView,
    PostListView, 
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)


#to use class based view instead of function based view, we import our view
#PLease note that PostListView will look for template with the following path.name
# app/model_viewtype.html in our case it would be blog/post_list.html
# we can change our template name or we can specify which template to use

urlpatterns = [
    path('', PostListView.as_view(),name='blog-home'),
    path('user/str:<username>', UserPostListView.as_view(),name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(),name='post-detail'),
    path('post/new/', PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(),name='post-delete'),
    path('about/', views.about,name='blog-about'),
]

