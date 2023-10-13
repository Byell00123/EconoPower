from django.urls import path
from .import views

urlpatterns =[
    path('', views.home, name='pagina_home'),
    path('teste/', views.teste, name='tetelogin'),
    # path('home2/', views.home2, name='pagina_home2'),
]
