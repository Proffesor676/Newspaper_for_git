from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
   path('', cache_page(60)(PostList.as_view()), name='post_list'),
   path('<int:pk>',cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
   path('news/search/', PostsSearch.as_view(), name='news_search'),
   path('news/create/', PostCreate.as_view(), name='post_create'),
   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe')
]