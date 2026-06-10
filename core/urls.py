
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import SensorViewSet, LecturaViewSet,CargaMasivaLecturasView


router = DefaultRouter()
router.register(r'sensores', SensorViewSet) 
router.register(r'lecturas', LecturaViewSet, basename='lectura')

urlpatterns = [
    path('admin/', admin.site.urls),
    # Las rutas de la API quedan directo en la raíz o bajo el prefijo que elijas
    path('api/', include(router.urls)),
    path('api/lecturas/carga-masiva/', CargaMasivaLecturasView.as_view(), name='carga-masiva-lecturas'),

]