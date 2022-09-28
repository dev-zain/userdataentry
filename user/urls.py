from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('details/<str:pk>',views.details,name='details'),
    path('add-user/',views.upload, name='upload'),
    path('update-user/<str:pk>',views.update, name='update'),
    path('backside/<str:pk>',views.backside,name='backside'),
    path('check/',views.check,name='check'),
    path('auth/',views.identify,name='identify'),
]