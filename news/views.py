from django.views.generic import (View, ListView, DetailView, CreateView, UpdateView, DeleteView)
from .filters import PostFilter
from .models import Post, Subscription, PostCategory, Category
from django.urls import reverse_lazy
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Exists, OuterRef
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import  get_object_or_404
from django.views.decorators.cache import cache_page
from django.core.cache import cache


class PostList(LoginRequiredMixin, ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostsSearch(LoginRequiredMixin, ListView):
    model = Post
    ordering = 'title'
    template_name = 'news_search.html'
    context_object_name = 'posts'
    paginate_by = 5
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()
    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)

class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_article',)
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'
    def form_valid(self, form):
        article = form.save(commit=False)
        article.categoryType = 'AR'
        return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_article',)
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_article',)
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = PostCategory.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

class CategoryListView(ListView):
    model = Post
    template_name = 'posts/category_list.html'
    context_object_name = 'category_posts_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super.get_context_date(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subsribers.all()
        context['category'] = self.postCategory
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subsribers.add(user)
    message = 'Подписка на рассылку новостей категории'
    return render(request, 'posts/subscribe.html', {'category': category, 'message': message})

def get(self, request, notify_about_new_post=None):
    notify_about_new_post.delay()
    return redirect("/")

@cache_page(60 * 15)
def my_view(request):
    ...

