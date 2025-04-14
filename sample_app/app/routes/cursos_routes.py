from app.controllers.curso_controller import get_cursos

def register_cursos_routes(app):
    @app.get('/api/cursos')
    def listar_cursos():
        cursos = get_cursos()
        return {"cursos": cursos}
