from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)

# Create your views here.
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request,'blog/home.html',context)


#Class based view

class PostListView(ListView):
    #we need to reference our model that will be used to create the view in this case it will be post
    model = Post
    # app/model_viewtype.html in our case it would be blog/post_list.html
    template_name = 'blog/home.html'
    #we also need to name our variable that our html will loop through
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    
class UserPostListView(ListView):
    #we need to reference our model that will be used to create the view in this case it will be post
    model = Post
    # app/model_viewtype.html in our case it would be blog/post_list.html
    template_name = 'blog/user_posts.html'
    #we also need to name our variable that our html will loop through
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_query_set(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
    
    
    
class PostDetailView(DetailView):
    #we need to reference our model that will be used to create the view in this case it will be post
    model = Post


class PostCreateView(LoginRequiredMixin,CreateView):
    #we need to reference our model that will be used to create the view in this case it will be post
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    #we need to reference our model that will be used to create the view in this case it will be post
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    #Test condition
    
    def test_func(self):
        post = self.get_object() #this will get the post we are trying to update
        #This checks if user updatding is author of the post
        if self.request.user == post.author: 
            return True
        
        return False
            
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    #we need to reference our model that will be used to create the view in this case it will be post
    model = Post
    success_url = '/feedback/'
    def test_func(self):
        post = self.get_object() #this will get the post we are trying to update
        #This checks if user updatding is author of the post
        if self.request.user == post.author: 
            return True
        
        return False

    



def about(request):
    return render(request,'blog/about.html',{'title':'title'})


