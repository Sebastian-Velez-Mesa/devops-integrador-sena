import unittest
import json
import os
import sys

# Añadir directorio actual al path para importar app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

class TestDevOpsFestivalAPI(unittest.TestCase):

    def setUp(self):
        # Configurar cliente de prueba de Flask
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home_endpoint(self):
        """Verifica que la raíz de la API responda correctamente"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["proyecto"], "SENA DevOps Festival API")
        self.assertEqual(data["estado"], "Online")

    def test_health_endpoint(self):
        """Verifica el endpoint de chequeo de salud (health check)"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "devops-festival-backend")

    def test_get_festival_info(self):
        """Verifica que retorne los datos generales del festival"""
        response = self.client.get('/api/festival')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        self.assertIn("nombre", data["data"])

    def test_get_artistas(self):
        """Verifica la carga de artistas y filtros"""
        response = self.client.get('/api/artistas')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        self.assertTrue(len(data["data"]) > 0)

        # Probar filtro por escenario
        response_filtered = self.client.get('/api/artistas?escenario=DevOps Stage')
        data_filtered = json.loads(response_filtered.data)
        for artista in data_filtered["data"]:
            self.assertEqual(artista["escenario"].lower(), "devops stage")

    def test_get_tickets(self):
        """Verifica que retorne los tipos de tickets disponibles"""
        response = self.client.get('/api/tickets')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        self.assertTrue(len(data["data"]) > 0)

    def test_post_contacto_validation(self):
        """Verifica la validación del formulario de contacto"""
        # Envío incompleto (falta mensaje)
        payload = {
            "nombre": "Juan Perez",
            "email": "juan@example.com"
        }
        response = self.client.post('/api/contacto', 
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "error")
        self.assertIn("obligatorios", data["message"])

    def test_get_stats(self):
        """Verifica que el endpoint de estadísticas de DevOps devuelva datos esperados"""
        response = self.client.get('/api/stats')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        self.assertIn("uptime_seconds", data["data"])
        self.assertIn("request_count", data["data"])

if __name__ == '__main__':
    unittest.main()
