from django.urls import path
from .views import *
from django.urls import path
from . views import *
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from newsfeed import settings

urlpatterns = [
    path('Signup/',SignUpView.as_view(),name='SignUpView'),
    path('signin/',SignInView.as_view(),name='SignInView'),
    path('signout/',SignOutView.as_view(),name='SignOutView'),

    path('',Indexview.as_view(),name='index'),
    path('news/<int:pk>',Newsview.as_view(),name='newsview'),
    path('commentview/',CommentaddView.as_view(),name='commentview'),
    path('subcommentaddview/',SubcommentaddView.as_view(),name='subcommentaddview'),

    path('updatevote/',UpdateVote.as_view(),name='updatevote'),
    path('commentvote/',CommentVote.as_view(),name='commentvote'),

    path('news-api/',NewsAPI.as_view(),name='newsapi'),
    path('chart/',Chart.as_view(),name='chart')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
