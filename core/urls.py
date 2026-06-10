
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import SensorViewSet, LecturaViewSet


router = DefaultRouter()
router.register(r'sensores', SensorViewSet) 
router.register(r'lecturas', LecturaViewSet, basename='lectura')

urlpatterns = [
    path('admin/', admin.site.urls),
  
    path('api/', include(router.urls)),
  

]