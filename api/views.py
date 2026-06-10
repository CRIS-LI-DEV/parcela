from rest_framework import viewsets
from .models import Sensor, Lectura
from .serializers import SensorSerializer, LecturaSerializer

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class LecturaViewSet(viewsets.ModelViewSet):
    serializer_class = LecturaSerializer

    def get_queryset(self):
        """
        Filtra las lecturas dinámicamente si se pasa el parámetro 'sensor' en la URL.
        Ejemplo: /api/lecturas/?sensor=3
        """
        queryset = Lectura.objects.all()
        sensor_id = self.request.query_params.get('sensor')
        
        if sensor_id is not None:
            queryset = queryset.filter(sensor_id=sensor_id)
            
        return queryset