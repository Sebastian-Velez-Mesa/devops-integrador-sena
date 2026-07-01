from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timezone
import os
import json
import logging
import time
import platform

# ── Configuración de la Aplicación ──────────────────────────────────
app = Flask(__name__)
CORS(app)

# Directorio de logs y persistencia
LOGS_DIR = os.environ.get('LOGS_DIR', '/app/logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# Configuración de logs
log_file = os.path.join(LOGS_DIR, 'festival.log')
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s]: %(message)s'
)
logger = logging.getLogger('devops-backend')

# Ruta para el archivo de persistencia de contactos (Demostración de Volumen)
CONTACTS_FILE = os.path.join(LOGS_DIR, 'contactos.json')

# Variables globales para métricas del dashboard
START_TIME = time.time()
REQUEST_COUNT = 0

# ── Datos en Memoria (Simulando Base de Datos) ────────────────────────
FESTIVAL_INFO = {
    "nombre": "SENA DevOps & Cloud Fest 2026",
    "fecha": "15 al 17 de Agosto, 2026",
    "lugar": "Centro de Tecnología y Manufactura Avanzada, Medellín",
    "edicion": "4ta Edición (Digital & Presencial)",
    "organizador": "SENA CTMA DevOps Group"
}

ARTISTAS = [
    {"id": 1, "nombre": "Docker DJ", "genero": "Techno/House", "escenario": "DevOps Stage", "hora": "19:00", "descripcion": "Loops rítmicos optimizados en microsegundos y beats basados en contenedores."},
    {"id": 2, "nombre": "The Kubernetes Trio", "genero": "Jazz Fusion", "escenario": "Cloud Stage", "hora": "20:30", "descripcion": "Orquestación armónica autogestionada con cero tiempo de inactividad."},
    {"id": 3, "nombre": "CI/CD Soundsystem", "genero": "Electropop", "escenario": "Main Stage", "hora": "22:00", "descripcion": "Lanzamientos continuos de sintetizadores y pipelines musicales fluidos."},
    {"id": 4, "nombre": "Git Merge Band", "genero": "Rock Alternativo", "escenario": "DevOps Stage", "hora": "17:30", "descripcion": "Riffs potentes sin conflictos de fusión y solos limpios en la rama main."},
    {"id": 5, "nombre": "Nginx & The Proxies", "genero": "Chillwave", "escenario": "Cloud Stage", "hora": "16:00", "descripcion": "Sonidos envolventes y balanceo de carga auditivo de alta eficiencia."},
    {"id": 6, "nombre": "Python Beats", "genero": "Minimal Tech", "escenario": "Main Stage", "hora": "18:00", "descripcion": "Scripts musicales legibles y dinámicos que corren de forma síncrona."}
]

TICKETS = [
    {"id": 1, "tipo": "Acceso General (Dev)", "precio": 60000, "moneda": "COP", "disponibles": 3000, "descripcion": "Entrada general para los 3 días de talleres y conciertos tech."},
    {"id": 2, "tipo": "Pase VIP (Ops)", "precio": 150000, "moneda": "COP", "disponibles": 400, "descripcion": "Acceso preferente a primera fila + Catering ilimitado + Gorra exclusiva Docker."},
    {"id": 3, "tipo": "Full Stack Pass (Backstage)", "precio": 350000, "moneda": "COP", "disponibles": 50, "descripcion": "Acceso VIP completo + Meet & Greet con los expositores + Cena DevOps final."},
    {"id": 4, "tipo": "Estudiante CTMA", "precio": 0, "moneda": "COP", "disponibles": 1000, "descripcion": "Entrada gratuita para aprendices SENA activos (requiere verificación de carnet)."}
]

# Helper para registrar peticiones
@app.before_request
def count_requests():
    global REQUEST_COUNT
    REQUEST_COUNT += 1

# Helper para leer contactos desde el archivo persistente
def read_contacts():
    if not os.path.exists(CONTACTS_FILE):
        return []
    try:
        with open(CONTACTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error al leer archivo de contactos: {e}")
        return []

# Helper para escribir contactos en el archivo persistente
def write_contacts(contacts):
    try:
        with open(CONTACTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(contacts, f, indent=2, ensure_ascii=False)
        logger.info(f"Contacto guardado exitosamente en volumen: {CONTACTS_FILE}")
        return True
    except Exception as e:
        logger.error(f"Error al escribir en archivo de contactos: {e}")
        return False

# ── Rutas de la API ──────────────────────────────────────────────────

@app.route('/')
def index():
    logger.info("GET / - Índice de la API consultado.")
    return jsonify({
        "proyecto": "SENA DevOps Festival API",
        "estado": "Online",
        "descripcion": "API REST para consulta de artistas, tickets y registro de contactos del festival.",
        "endpoints": {
            "GET /": "Índice del servicio",
            "GET /health": "Chequeo de salud del contenedor",
            "GET /api/festival": "Información general del festival",
            "GET /api/artistas": "Listado de artistas (filtrable por ?escenario o ?genero)",
            "GET /api/artistas/<id>": "Detalle de artista por ID",
            "GET /api/tickets": "Tipos de entradas disponibles",
            "POST /api/contacto": "Registro de contactos/reservas (Persistencia en Volumen)",
            "GET /api/stats": "Estadísticas DevOps en vivo del sistema"
        }
    }), 200

@app.route('/health')
def health():
    # Retorna salud del servicio
    logger.debug("GET /health - Healthcheck consultado.")
    return jsonify({
        "status": "healthy",
        "service": "devops-festival-backend",
        "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    }), 200

@app.route('/api/festival')
def get_festival():
    logger.info("GET /api/festival - Consultado información de festival.")
    return jsonify({
        "status": "success",
        "data": FESTIVAL_INFO
    }), 200

@app.route('/api/artistas')
def get_artistas():
    logger.info("GET /api/artistas - Consultado listado de artistas.")
    escenario = request.args.get('escenario')
    genero = request.args.get('genero')
    
    resultados = ARTISTAS
    
    if escenario:
        resultados = [a for a in resultados if a['escenario'].lower() == escenario.lower()]
    if genero:
        resultados = [a for a in resultados if a['genero'].lower() == genero.lower()]
        
    return jsonify({
        "status": "success",
        "count": len(resultados),
        "data": resultados
    }), 200

@app.route('/api/artistas/<int:artista_id>')
def get_artista_detalle(artista_id):
    logger.info(f"GET /api/artistas/{artista_id} - Consultado detalle de artista.")
    artista = next((a for a in ARTISTAS if a['id'] == artista_id), None)
    if not artista:
        logger.warning(f"Artista ID {artista_id} no encontrado.")
        return jsonify({
            "status": "error",
            "message": "Artista no encontrado"
        }), 404
    return jsonify({
        "status": "success",
        "data": artista
    }), 200

@app.route('/api/tickets')
def get_tickets():
    logger.info("GET /api/tickets - Consultado listado de tickets.")
    return jsonify({
        "status": "success",
        "count": len(TICKETS),
        "data": TICKETS
    }), 200

@app.route('/api/contacto', methods=['POST'])
def post_contacto():
    data = request.get_json(silent=True) or {}
    nombre = data.get('nombre', '').strip()
    email = data.get('email', '').strip()
    mensaje = data.get('mensaje', '').strip()
    ticket_id = data.get('ticket_id')  # Opcional, si reserva ticket

    if not nombre or not email or not mensaje:
        logger.warning("POST /api/contacto - Intento de envío incompleto.")
        return jsonify({
            "status": "error",
            "message": "Los campos 'nombre', 'email' y 'mensaje' son obligatorios."
        }), 400

    # Crear el nuevo registro de contacto
    nuevo_contacto = {
        "id": int(time.time() * 1000),
        "nombre": nombre,
        "email": email,
        "mensaje": mensaje,
        "ticket_id": ticket_id,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Leer archivo persistente, añadir contacto, escribir archivo persistente
    contactos = read_contacts()
    contactos.append(nuevo_contacto)
    
    if write_contacts(contactos):
        logger.info(f"POST /api/contacto - Mensaje de {nombre} registrado correctamente.")
        return jsonify({
            "status": "success",
            "message": f"¡Gracias {nombre}! Tu solicitud ha sido registrada en el volumen de Docker.",
            "data": nuevo_contacto
        }), 201
    else:
        logger.error("POST /api/contacto - Fallo al escribir en almacenamiento persistente.")
        return jsonify({
            "status": "error",
            "message": "Error interno al guardar los datos en el volumen persistente."
        }), 500

@app.route('/api/stats')
def get_stats():
    # Retorna métricas en vivo útiles para el dashboard DevOps en el frontend
    uptime = round(time.time() - START_TIME, 2)
    contactos = read_contacts()
    
    # Comprobar si el archivo de log existe y su tamaño
    log_size = 0
    if os.path.exists(log_file):
        log_size = os.path.getsize(log_file)
        
    return jsonify({
        "status": "success",
        "data": {
            "uptime_seconds": uptime,
            "uptime_formatted": f"{int(uptime // 3600)}h {int((uptime % 3600) // 60)}m {int(uptime % 60)}s",
            "request_count": REQUEST_COUNT,
            "contacts_count": len(contactos),
            "log_file_size_bytes": log_size,
            "os_platform": platform.system(),
            "os_release": platform.release(),
            "python_version": platform.python_version(),
            "container_environment": "Docker (Linux Container)" if os.path.exists('/.dockerenv') else "Host Local",
            "logs_directory": LOGS_DIR,
            "contacts_persisted": contactos[-5:] if contactos else []  # Últimos 5 contactos registrados
        }
    }), 200

# ── Ejecución de la App ──────────────────────────────────────────────
if __name__ == '__main__':
    # Flask de desarrollo corre en el puerto 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Iniciando API del Festival DevOps en el puerto {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
