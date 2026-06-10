from django.db import models

class Sensor(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)  
    valor_actual = models.FloatField(default=0.0)
    rep_visual = models.CharField(max_length=50)  
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"


class Lectura(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='lecturas')
    valor = models.FloatField()
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor.nombre} - {self.valor} a las {self.fecha_hora.strftime('%H:%M:%S')}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        #
        Sensor.objects.filter(pk=self.sensor_id).update(
            valor_actual=self.valor
        )