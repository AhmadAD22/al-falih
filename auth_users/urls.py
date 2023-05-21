from django.urls import path
from . import views

urlpatterns = [
         path('token-auth/',views.CustomAuthToken.as_view()),
         path('',views.UserView.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
         path('<int:pk>/',views.UserView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-detail'),
    ]

