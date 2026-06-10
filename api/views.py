from rest_framework import viewsets
from .models import Sensor, Lectura
from .serializers import SensorSerializer, LecturaSerializer
from django.db import transaction


from rest_framework.response import Response
from rest_framework import status



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
    
    class CargaMasivaLecturasView(APIView):

        def post(self, request, *args, **kwargs):
            diccionario_datos = request.data
            
            # Validar que efectivamente nos llegó un diccionario
            if not isinstance(diccionario_datos, dict):
                return Response(
                    {"error": "El formato de datos debe ser un objeto/diccionario {id_sensor: valor}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            lecturas_creadas = 0
            errores = []

            # Usamos transaction.atomic para procesar todo en un solo bloque seguro
            try:
                with transaction.atomic():
                    for sensor_id, valor in diccionario_datos.items():
                        try:
                            # 1. Verificar si el sensor existe en la base de datos
                            sensor = Sensor.objects.get(id=sensor_id)
                            
                            # 2. Crear la lectura (asumiendo que tus campos se llaman 'sensor' y 'valor')
                            # Modifica 'valor' por el nombre real de tu campo (ej. 'voltaje', 'nivel', etc.)
                            Lectura.objects.create(
                                sensor=sensor,
                                valor=float(valor)  # Lo convertimos a float por seguridad
                            )
                            lecturas_creadas += 1
                            
                        except Sensor.DoesNotExist:
                            errores.append(f"El sensor con ID {sensor_id} no existe en la base de datos.")
                        except ValueError:
                            errores.append(f"El valor '{valor}' para el sensor {sensor_id} no es un número válido.")

                # Si hubo errores pero se lograron procesar algunos, avisamos al usuario
                if errores and lecturas_creadas == 0:
                    return Response({"errores": errores}, status=status.HTTP_400_BAD_REQUEST)
                    
                return Response({
                    "mensaje": f"Se registraron exitosamente {lecturas_creadas} lecturas.",
                    "alertas_o_errores": errores if errores else None
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response(
                    {"error": f"Error inesperado al procesar la carga masiva: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )