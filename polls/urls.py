from django import views
from django.urls import include, path
from django.urls.conf import re_path
from . import views

app_name ='polls'
urlpatterns = [
    # ex: /polls/
    path('', views.IndexView.as_view(), name="index"),
    # ex: polls/5/
    path('post/<int:pk>/', views.getPostPage, name="post"),
    #path('<int:post_id>/searchComments/', views.searchComments, name="searchComments"),
    path('updateComment/<int:post_id>/', views.updateNuoviCommenti, name="updateNuoviCommenti"),
    path('insertInProfile/<str:profile>/', views.insertInProfile, name="insertInProfile"),
    path('updateNewPost/<str:profile>/', views.updateNewPost, name="updateNewPost"),
    path('<int:pk>/', views.getProfile, name="profile"),
    path('insert/', views.insert, name="insert"),
    path('<int:profile_id>/delete/', views.delete, name="delete")
    #re_path(r'^ajax/validate_username/$', views.get_similar_username_profile, name="similar_profile")
    
]
