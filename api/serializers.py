from rest_framework import serializers
from .models import Sensor, Lectura

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'nombre', 'tipo', 'valor_actual', 'rep_visual', 'ultima_actualizacion']
        # Evitamos que alteren el valor actual manualmente desde la API de sensores
        read_only_fields = ['valor_actual', 'ultima_actualizacion']


class LecturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lectura
        fields = ['id', 'sensor', 'valor', 'fecha_hora']
        read_only_fields = ['fecha_hora']