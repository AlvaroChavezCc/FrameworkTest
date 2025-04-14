from myframework.core import MyFramework
from app.routes import register_all_routes

# Crear una instancia de la aplicación
app = MyFramework()

# Registrar todas las rutas de la aplicación
register_all_routes(app)

# Configurar manejadores de errores y middleware globales

@app.errorhandler(404)
def manejar_404():
    return {"error": "Ruta no encontrada"}

@app.errorhandler(500)
def manejar_500(error):
    return {"error": "Error interno del servidor", "detalle": error}

@app.before_request
def log_request(environ):
    print(f"➡️  {environ['REQUEST_METHOD']} {environ['PATH_INFO']}")

@app.after_request
def agregar_cabecera(response):
    response['served_by'] = 'myframework'
    return response