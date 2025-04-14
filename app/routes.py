from myframework.core import MyFramework
from app.controllers.user_controller import get_user_by_id

app = MyFramework()

@app.get('/api/usuario/<id>')
def usuario_json(id):
    return get_user_by_id(id)

@app.post('/api/saludo')
def saludar(post_data):
    # Se asume que post_data es un dict parseado del JSON
    nombre = post_data.get('nombre', '')
    return {"mensaje": f"Hola, {nombre}!"}

@app.errorhandler(404)
def not_found():
    return {"error": "Ruta no encontrada"}

@app.errorhandler(500)
def server_error(error):
    return {"error": "Error interno del servidor", "detalle": error}

@app.before_request
def log_request(environ):
    print(f"➡️ {environ['REQUEST_METHOD']} {environ['PATH_INFO']}")

# Ejemplo de uso del after_request: modificar la respuesta antes de enviarla
@app.after_request
def modify_response(response):
    # Agrega un campo extra a todas las respuestas
    response['extra'] = 'valor extra'
    return response