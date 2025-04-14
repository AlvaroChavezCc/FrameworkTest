# myframework/scripts/scaffold.py
import os
import sys

def create_directory(path):
    os.makedirs(path, exist_ok=True)
    print(f"Directorio creado: {path}")

def create_file(path, content=""):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Archivo creado: {path}")

def scaffold_project(project_name="sample_app"):
    # Directorio raíz del proyecto
    if not os.path.exists(project_name):
        os.makedirs(project_name)
    
    # Definir rutas para subdirectorios
    app_dir = os.path.join(project_name, "app")
    controllers_dir = os.path.join(app_dir, "controllers")
    routes_dir = os.path.join(app_dir, "routes")
    
    # Crear directorios necesarios
    create_directory(app_dir)
    create_directory(controllers_dir)
    create_directory(routes_dir)
    
    # 1. Archivo: app/__init__.py
    app_init_content = (
        "# app/__init__.py\n"
        "# Aquí se crea la instancia de la app y se registran todas las rutas y middlewares\n\n"
        "from myframework.core import MyFramework\n"
        "from app.routes import register_all_routes\n\n"
        "# Crear la instancia de la app\n"
        "app = MyFramework()\n\n"
        "# Registrar todas las rutas\n"
        "register_all_routes(app)\n\n"
        "# Configuración global de errores y middlewares\n"
        "@app.errorhandler(404)\n"
        "def manejar_404():\n"
        "    return {'error': 'Ruta no encontrada'}\n\n"
        "@app.errorhandler(500)\n"
        "def manejar_500(error):\n"
        "    return {'error': 'Error interno del servidor', 'detalle': error}\n\n"
        "@app.before_request\n"
        "def log_request(environ):\n"
        "    print(f\"➡️  {environ['REQUEST_METHOD']} {environ['PATH_INFO']}\")\n\n"
        "@app.after_request\n"
        "def agregar_cabecera(response):\n"
        "    response['served_by'] = 'myframework'\n"
        "    return response\n"
    )
    create_file(os.path.join(app_dir, "__init__.py"), app_init_content)
    
    # 2. Archivo: app/controllers/__init__.py (vacío o con comentario)
    controllers_init_content = "# app/controllers/__init__.py\n# Este paquete agrupa los controladores del proyecto.\n"
    create_file(os.path.join(controllers_dir, "__init__.py"), controllers_init_content)
    
    # 3. Archivo: app/routes/__init__.py con función register_all_routes
    routes_init_content = (
        "# app/routes/__init__.py\n"
        "def register_all_routes(app):\n"
        "    # Importa y registra los módulos de rutas\n"
        "    from app.routes import estudiantes_routes, cursos_routes\n"
        "    estudiantes_routes.register_estudiantes_routes(app)\n"
        "    cursos_routes.register_cursos_routes(app)\n"
    )
    create_file(os.path.join(routes_dir, "__init__.py"), routes_init_content)
    
    # 4. Archivo: app/routes/estudiantes_routes.py
    estudiantes_routes_content = (
        "# app/routes/estudiantes_routes.py\n"
        "def register_estudiantes_routes(app):\n"
        "    # Define las rutas relacionadas con estudiantes\n"
        "    @app.get('/api/estudiantes')\n"
        "    def listar_estudiantes():\n"
        "        # Lógica para listar estudiantes\n"
        "        return {'mensaje': 'Lista de estudiantes'}\n"
        "\n"
        "    @app.post('/api/estudiantes')\n"
        "    def crear_estudiante(post_data):\n"
        "        # Lógica para crear un estudiante\n"
        "        return {'mensaje': 'Estudiante creado'}\n"
    )
    create_file(os.path.join(routes_dir, "estudiantes_routes.py"), estudiantes_routes_content)
    
    # 5. Archivo: app/routes/cursos_routes.py
    cursos_routes_content = (
        "# app/routes/cursos_routes.py\n"
        "def register_cursos_routes(app):\n"
        "    # Define las rutas relacionadas con cursos\n"
        "    @app.get('/api/cursos')\n"
        "    def listar_cursos():\n"
        "        # Lógica para listar cursos\n"
        "        return {'mensaje': 'Lista de cursos'}\n"
    )
    create_file(os.path.join(routes_dir, "cursos_routes.py"), cursos_routes_content)
    
    # 6. Archivo: run.py en la raíz del proyecto
    run_py_content = (
        "# run.py\n"
        "# Punto de entrada de la aplicación\n\n"
        "from wsgiref.simple_server import make_server\n"
        "from app import app  # Importa la app configurada en app/__init__.py\n\n"
        "if __name__ == '__main__':\n"
        "    with make_server('', 8000, app) as server:\n"
        "        print('Servidor corriendo en http://localhost:8000')\n"
        "        server.serve_forever()\n"
    )
    create_file(os.path.join(project_name, "run.py"), run_py_content)
    
    print(f"\nEsqueleto del proyecto '{project_name}' creado exitosamente.")

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Genera el esqueleto de un nuevo proyecto utilizando myframework."
    )
    parser.add_argument(
        "project_name", nargs="?", default="sample_app",
        help="Nombre del directorio raíz del proyecto (por defecto: sample_app)"
    )
    args = parser.parse_args()
    scaffold_project(args.project_name)

if __name__ == '__main__':
    main()
