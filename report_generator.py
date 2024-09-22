import matplotlib.pyplot as plt
import io
import base64

class ReportGenerator:
    def __init__(self):
        pass

    def generate_report(self):
        # Obtener las respuestas desde un archivo o base de datos (aquí simuladas)
        responses = {"feliz": 10, "neutral": 5, "triste": 2}
        
        # Crear un gráfico circular
        labels = responses.keys()
        sizes = responses.values()
        colors = ['#66b3ff','#99ff99','#ff9999']
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Asegura que el gráfico sea un círculo

        # Guardar gráfico en un formato base64 para enviar en Slack
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        base64_img = base64.b64encode(img.getvalue()).decode('utf8')

        # Devuelve el gráfico como un attachment de Slack
        return [
            {
                "title": "Reporte de Clima Laboral",
                "image_url": f"data:image/png;base64,{base64_img}"
            }
        ]
