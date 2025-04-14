from app.routes.estudiantes_routes import register_estudiantes_routes
from app.routes.cursos_routes import register_cursos_routes

def register_all_routes(app):
    register_estudiantes_routes(app)
    register_cursos_routes(app)