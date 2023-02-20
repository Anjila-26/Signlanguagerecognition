from django.urls import path
from . import views

urlpatterns = [
    path('signup',views.signup ,name = 'signup'),
    path('firstpage',views.firstpage ,name='firstpage'),
    path('signin', views.signin, name='signin'),
    path('detect',views.detect,name = 'detect'),
    path('options',views.main,name='options'),
    path('recog',views.Recognition, name = 'recognition'),
    path('english',views.sign_language, name = 'name'),
    path('dict', views.dictonary, name = 'dict'),
    path('a', views.a,name='a'),
    path('about',views.about,name='about'),
]