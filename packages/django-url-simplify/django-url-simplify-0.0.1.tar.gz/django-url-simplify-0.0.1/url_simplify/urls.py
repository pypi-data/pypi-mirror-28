from django.urls import path
from django.conf import settings
from . import views

app_name = 'url_simplify'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:url_id>/delete/', views.delete_url, name='delete_url'),
    path('urls/', views.UrlsView.as_view(), name='urls'),
    path('shortify/', views.add_url, name='add_url'),
    path(settings.SHORT_PREFIX + '<str:short_id>/',
         views.short_redirect, name='short_redirect')
]
