from django.urls import path
from .import views

urlpatterns =[
    path('', views.home, name='pagina_home'),
    # path('home1/', views.home1, name='pagina_home1'),
    # path('home2/', views.home2, name='pagina_home2'),
]
