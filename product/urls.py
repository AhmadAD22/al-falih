from django.urls import path
from rest_framework import routers
from . import views

category_router = routers.SimpleRouter()
category_router.register(r'categories',views.CategoryView, basename='category')
subcategory_router = routers.SimpleRouter()
subcategory_router.register(r'subcategories',views.SubcategoryView, basename='subcategory')

urlpatterns = [
    #products 
    path('',views.ProductView.as_view({'get':'list', 'post': 'create'})),
    path('<int:pk>/',views.ProductView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    
    #Products Filtering
    path('filterbycategory/<int:category_id>',views.ProductView.as_view({'get':'listByCategory'})),
    path('filterbysubcategory/<int:subcategory_id>',views.ProductView.as_view({'get':'listBySubcategory'})),
    
]
urlpatterns += category_router.urls
urlpatterns += subcategory_router.urls
