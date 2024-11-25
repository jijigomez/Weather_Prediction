from django.urls import path
from . import views

urlpatterns = [
    path('reg/', views.reg, name='reg'),
    path('log/', views.log, name='log'),
    path('about/', views.about, name='about'),
    path('cont/', views.cont, name='cont'),
    # path('cont/', views.cont, name='cont'),
    path('index/',views.index, name='index'),
        path('predict/', views.predict_weather, name='predict_weather'),
    
    
]