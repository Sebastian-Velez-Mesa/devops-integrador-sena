from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os
import logging

# ── Configuración de la app ──────────────────────────────────────────
app = Flask(__name__)
CORS(app)

# Logs
os.makedirs('/app/logs', exist_ok=True)
logging.basicConfig(
    filename='/app/logs/festival.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

# ── Datos del festival ───────────────────────────────────────────────
FESTIVAL_INFO = {
    "nombre": "Festival DevOps Music Fest 2026",
    "fecha": "15-17 Agosto 2026",
    "lugar": "Medellín, Colombia",
    "edicion": 2026
}

ARTISTAS = [
    {"id": 1, "nombre": "Docker DJ",        "genero": "Electronic",  "escenario": "Principal",    "hora": "21:00"},
    {"id": 2, "nombre": "The Kubernetes",    "genero": "Rock",        "escenario": "Secundario",   "hora": "20:00"},
    {"id": 3, "nombre": "CI/CD Soundsystem", "genero": "Hip-Hop",     "escenario": "Open Air",     "hora": "19:00"},
    {"id": 4, "nombre": "Git Merge Band",    "genero": "Jazz Fusion",  "escenario": "Acústico",    "hora": "18:00"},
    {"id": 5, "nombre": "Nginx Waves",       "genero": "Chillout",    "escenario": "Principal",    "hora": "17:00"},
    {"id": 6, "nombre": "Python Beats",      "genero": "Techno",      "escenario": "Secundario",   "hora": "22:00"},
]

TICKETS = [
    {"id": 1, "tipo": "General",    "precio": 80000,  "moneda": "COP", "disponibles": 5000, "descripcion": "Acceso a todos los escenarios"},
    {"id": 2, "tipo": "VIP",        "precio": 200000, "moneda": "COP", "disponibles": 500,  "descripcion": "Zona VIP + Meet & Greet"},
    {"id": 3, "tipo": "Backstage",  "precio": 450000, "moneda": "COP", "disponibles": 50,   "descripcion": "Acceso backstage + cena con artistas"},
    {"id": 4, "tipo": "Full Pass",  "precio": 150000, "moneda": "COP", "disponibles": 2000, "descripcion": "3 días completos + camping"},
]

# ── Rutas ────────────────────────────────────────────────────────────

@app.route('/')
def home():
    logger.info('GET / – Health check')
    return jsonify({
        "status": "ok",
        "mensaje": "🎵 API Festival DevOps Music Fest 2026",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "endpoints": ["/api/festival", "/api/artistas", "/api/tickets", "/api/contacto"]
    })

@app.route('/api/festival')
def get_festival():
    logger.info('GET /api/festival')
    return jsonify({"status": "ok", "data": FESTIVAL_INFO})

@app.route('/api/artistas')
def get_artistas():
    logger.info('GET /api/artistas')
    escenario = request.args.get('escenario')
    resultado = ARTISTAS
    if escenario:
        resultado = [a for a in ARTISTAS if a['escenario'].lower() == escenario.lower()]
    return jsonify({"status": "ok", "total": len(resultado), "data": resultado})

@app.route('/api/artistas/<int:artista_id>')
def get_artista(artista_id):
    logger.info(f'GET /api/artistas/{artista_id}')
    artista = next((a for a in ARTISTAS if a['id'] == artista_id), None)
    if not artista:
        return jsonify({"status": "error", "mensaje": "Artista no encontrado"}), 404
    return jsonify({"status": "ok", "data": artista})

@app.route('/api/tickets')
def get_tickets():
    logger.info('GET /api/tickets')
    return jsonify({"status": "ok", "total": len(TICKETS), "data": TICKETS})

@app.route('/api/contacto', methods=['POST'])
def contacto():
    data = request.get_json(silent=True) or {}
    nombre = data.get('nombre', '').strip()
    email  = data.get('email', '').strip()
    mensaje = data.get('mensaje', '').strip()

    if not nombre or not email or not mensaje:
        return jsonify({"status": "error", "mensaje": "nombre, email y mensaje son requeridos"}), 400

    logger.info(f'Contacto de {nombre} <{email}>')
    return jsonify({
        "status": "ok",
        "mensaje": f"¡Gracias {nombre}! Tu mensaje fue recibido. Te contactaremos pronto.",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 201

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "festival-backend"}), 200

# ── Arranque ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
