from app.controllers.estudiante_controller import get_estudiantes, add_estudiante

def register_estudiantes_routes(app):
    @app.get('/api/estudiantes')
    def listar_estudiantes():
        estudiantes = get_estudiantes()
        return {"estudiantes": estudiantes}

    @app.post('/api/estudiantes')
    def crear_estudiante(post_data):
        return add_estudiante(post_data)
