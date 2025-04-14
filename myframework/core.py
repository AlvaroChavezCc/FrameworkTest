import re
import json

class MyFramework:
    def __init__(self):
        self.routes = []
        self.error_handlers = {}
        self._before_request = None
        self._after_request = None

    def errorhandler(self, status_code):
        def wrapper(func):
            self.error_handlers[status_code] = func
            return func
        return wrapper

    def route(self, path, methods=['GET']):
        # Convierte la ruta en un patrón regex (por ejemplo, /usuario/<id>)
        pattern = re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', path)
        pattern = f'^{pattern}$'

        def wrapper(func):
            self.routes.append({
                'pattern': re.compile(pattern),
                'methods': methods,
                'func': func
            })
            return func
        return wrapper

    # Atajos para métodos HTTP
    def get(self, path):
        return self.route(path, methods=['GET'])

    def post(self, path):
        return self.route(path, methods=['POST'])

    # Decorador para ejecutar una función después de la ruta
    def after_request(self, func):
        self._after_request = func
        return func

    # Decorador para ejecutar una función antes de la ruta
    def before_request(self, func):
        self._before_request = func
        return func

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '/')
        method = environ.get('REQUEST_METHOD', 'GET')

        if self._before_request:
            self._before_request(environ)

        try:
            for route in self.routes:
                match = route['pattern'].match(path)
                if match and method in route['methods']:
                    kwargs = match.groupdict()

                    if method in ['POST', 'PUT']:
                        try:
                            size = int(environ.get('CONTENT_LENGTH', 0))
                        except ValueError:
                            size = 0
                        body = environ['wsgi.input'].read(size).decode()

                        try:
                            post_data = json.loads(body)
                        except json.JSONDecodeError:
                            post_data = {}
                        result = route['func'](post_data=post_data, **kwargs)
                    else:
                        result = route['func'](**kwargs)

                    # Permite retornar (dict, status)
                    if isinstance(result, tuple):
                        response, status = result
                    else:
                        response = result
                        status = '200 OK'

                    if not isinstance(response, dict):
                        error_message = json.dumps({'error': 'La respuesta debe ser un JSON (dict)'})
                        start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
                        return [error_message.encode()]

                    if self._after_request:
                        response = self._after_request(response)

                    start_response(status, [('Content-Type', 'application/json')])
                    return [json.dumps(response).encode()]

            # Ruta no encontrada: usa el manejador de error 404 si está configurado.
            if 404 in self.error_handlers:
                response_dict = self.error_handlers[404]()
                start_response('404 Not Found', [('Content-Type', 'application/json')])
                return [json.dumps(response_dict).encode()]

            start_response('404 Not Found', [('Content-Type', 'application/json')])
            return [json.dumps({'error': 'Ruta no encontrada'}).encode()]

        except Exception as e:
            # Manejador de error 500 personalizado
            if 500 in self.error_handlers:
                response_dict = self.error_handlers[500](str(e))
                start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
                return [json.dumps(response_dict).encode()]
            start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
            return [json.dumps({'error': str(e)}).encode()]