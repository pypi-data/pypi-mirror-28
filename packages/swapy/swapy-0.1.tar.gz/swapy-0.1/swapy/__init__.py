import inspect
import json
import uuid
from werkzeug.wrappers import Request as WRequest, Response
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.serving import run_simple, make_ssl_devcert
from werkzeug.routing import Rule, Map
from werkzeug.wsgi import responder, FileWrapper, SharedDataMiddleware
from werkzeug.urls import iri_to_uri
from werkzeug.utils import escape
from .middlewares import ExceptionMiddleware
import os
import mimetypes


_url_map = {}
_middlewares = {}
_on_error = {}
_on_not_found = {}
_routes = {}
_ssl_for = {}
_shared_dir = {}


def _caller():
    """Returns the module which calls swapy"""
    return inspect.currentframe().f_back.f_back.f_globals['__name__']


def _caller_frame():
    return inspect.currentframe().f_back.f_back


def _init(module):
    """Adds every module which is calling first time to routes and middlewares"""
    global _url_map, _middlewares, _on_error, _on_not_found, _ssl_for, _shared_dir

    if module not in _url_map:
        _url_map[module] = Map([])
    if module not in _routes:
        _routes[module] = {}
    if module not in _middlewares:
        _middlewares[module] = []
    if module not in _on_error:
        _on_error[module] = ExceptionMiddleware
    if module not in _on_not_found:
        _on_not_found[module] = ExceptionMiddleware
    if module not in _ssl_for:
        _ssl_for[module] = None
    if module not in _shared_dir:
        _shared_dir[module] = None


def _error_handler(e, module):
    global _on_error
    try:
        res = _on_error[module](e)
        if type(res) == tuple:
            return Response(*res)
        else:
            return Response(res)
    except TypeError:
        return e


def _error(module, f):
    global _on_error
    _init(module)
    _on_error[module] = f


def _not_found_handler(e, module):
    global _on_not_found
    try:
        res = _on_not_found[module](e)
        if type(res) == tuple:
            return Response(*res)
        else:
            return Response(res)
    except TypeError:
        return e


def _shared(frame, directory):
    global _shared_dir
    module_name = frame.f_globals['__name__']
    if directory is True:
        directory = 'shared'
    directory = os.path.join(os.path.dirname(frame.f_globals['__file__']), directory)
    directory = directory.replace('\\', '/')
    _shared_dir[module_name] = directory


def _find_route(name):
    """Returns the route by name"""

    global _url_map
    for module in _url_map.keys():
        routes = _url_map[module]
        for route in routes:
            if route['url'] == name:
                return route
    return None


def _register_route(module, url='/', methods=('GET', 'POST', 'PUT', 'DELETE')):
    """Adds a route to the module which calls this"""

    global _url_map, _middlewares, _on_error, _routes

    _init(module)

    #  Adjust path
    if not url.startswith('/'):
        url = '/{}'.format(url)
    if url == '/*':
        url = '/<path:path>'

    # Check if rule already exists
    for route in _url_map[module].iter_rules():
        if route.rule == url and [method for method in route.methods if method in methods]:
            raise Exception('Path "{}" already exists in "{}". Cannot add route to module "{}". '
                            'Maybe you included routes with the same url?'.format(route.rule, module, module))

    def decorator(f):
        mws = _middlewares[module]

        def handle(*_, **kwargs):
            target = f
            req = kwargs['req']
            for m in mws:
                target = m(target)
            try:
                res = target(req)
            except TypeError:
                res = target()
            if res:
                return res
            else:
                return ''

        name = str(uuid.uuid4())
        rule = Rule(url, methods=methods, endpoint=name, strict_slashes=False)
        _url_map[module].add(rule)
        _routes[module][name] = {'function': handle, 'on_error': _on_error[module], 'url': url}
        return f

    return decorator


def _use(module, *middlewares_):
    global _middlewares

    _init(module)
    for middleware in middlewares_:
        _middlewares[module].append(middleware)


def _ssl(module, host, path=None):
    global _ssl_for
    if path:
        _ssl_for[module] = make_ssl_devcert(path, host=host)
    else:
        import importlib
        # noinspection PyDeprecation
        open_ssl = importlib.find_loader('OpenSSL')
        if open_ssl:
            _ssl_for[module] = 'adhoc'
        else:
            raise ModuleNotFoundError('SSL generation requires the PyOpenSSl module. Please install it or pass the path\
             to your self generated certificate')


def _favicon(module, path):
    def handle():
        with open(path, 'rb') as f:
            return f.read()
    _register_route(module, '/favicon.ico')(handle)


def _not_found(module, f):
    global _on_not_found
    _init(module)
    _on_not_found[module] = f


def _include(module, target, prefix=''):
    """Includes a module into another module"""
    global _url_map
    _init(module)
    _init(target.__name__)
    if not prefix.startswith('/') and len(prefix) >= 1:
        prefix = '/{}'.format(prefix)
    if prefix == '/':
        prefix = ''
    routes = _url_map[target.__name__]
    for route in routes.iter_rules():
        rule = '{}{}'.format(prefix, route.rule)
        for r in _url_map[module].iter_rules():
            if rule == r.rule:
                raise Exception('Path "{}" already exists in "{}". Module "{}" cannot be included in "{}".'
                                .format(rule, module, target.__name__, module))
    for name in _routes[target.__name__].keys():
        _routes[module][name] = _routes[target.__name__][name]
    for route in routes.iter_rules():
        rule = '{}{}'.format(prefix, route.rule)
        new_route = Rule(rule, endpoint=route.endpoint, methods=route.methods, strict_slashes=False)
        _url_map[module].add(new_route)


def _build_app(module):
    """Returns the app"""

    global _url_map, _routes, _shared_dir

    @responder
    def application(environ, _):
        urls = _url_map[module].bind_to_environ(environ)
        req = Request(environ)

        def dispatch(endpoint, args):
            try:
                args = dict(args)
                setattr(req, 'url_args', args)
                f = _routes[module][endpoint]['function']
                try:
                    res = f(req=req)
                except TypeError:
                    res = f()

                # Checks if the type is iterable to prevent more errors
                iter(res)

                if isinstance(res, tuple) or isinstance(res, tuple) and isinstance(res[0], FileWrapper):
                    return Response(*res, direct_passthrough=True)
                elif isinstance(res, FileWrapper):
                    return Response(res, direct_passthrough=True)
                else:
                    return Response(res)
            except NotFound as ex:
                return _not_found_handler(ex, module)
            except HTTPException as ex:
                return _error_handler(ex, module)
        return urls.dispatch(dispatch)
    if _shared_dir[module]:
        return SharedDataMiddleware(application, {
            '/shared': _shared_dir[module]
        })
    return application


def redirect(location, code=301):
    location = iri_to_uri(location, safe_conversion=True)
    response = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'\
        '<title>Redirecting...</title>\n'\
        '<h1>Redirecting...</h1>\n'\
        '<p>You should be redirected automatically to target URL: '\
        '<a href="{}">{}</a>.  If not click the link.'.format(escape(location), escape(location))
    return response, code, {'Location': location, 'Content-Type': 'text/html'}


def file(path, name=None):
    if not os.path.isabs(path):
        path = os.path.abspath(_caller_frame().f_globals['__file__'])
    f = open(path, 'rb')
    if file:
        mime = mimetypes.guess_type(path)[0]
        size = os.path.getsize(path)
        filename = os.path.basename(path) if not name else name
        headers = {'Content-Type': mime, 'Content-Disposition': 'attachment;filename='+filename, 'Content-Length': size}
        return FileWrapper(f, 8192), 200, headers
    raise FileNotFoundError()


def favicon(path):
    _favicon(_caller(), path)


def ssl(host, path=None):
    _ssl(_caller(), host, path)


def error(f):
    _error(_caller(), f)


def shared(directory):
    module = _caller_frame()
    _shared(module, directory)


def not_found(f):
    _not_found(_caller(), f)


def on(url='/', methods=('GET', 'POST', 'PUT', 'DELETE')):
    """Route registerer for all http methods"""
    return _register_route(_caller(), url, methods)


def on_get(url='/'):
    """Route registerer for GET http method"""
    return _register_route(_caller(), url, methods=['GET'])


def on_post(url='/'):
    """Route registerer for POST http method"""
    return _register_route(_caller(), url, methods=['POST'])


def on_put(url='/'):
    """Route registerer for PUT http method"""
    return _register_route(_caller(), url, methods=['PUT'])


def on_delete(url='/'):
    """Route registerer for DELETE http method"""
    return _register_route(_caller(), url, methods=['DELETE'])


def include(module, prefix=''):
    """Includes a module into another module"""
    _include(_caller(), module, prefix)


def config(cfg):
    module = _caller()
    if isinstance(cfg, dict):
        if cfg.get('use'):
            middlewares_ = cfg['use']
            if isinstance(middlewares_, (tuple, list)):
                _use(module, *middlewares_)
            else:
                _use(module, middlewares_)
        if cfg.get('include'):
            modules_ = cfg['include']

            def handle(args):
                if isinstance(args, (tuple, list)):
                    _include(module, *args)
                else:
                    _include(module, args)
            if isinstance(modules_, list):
                for target in modules_:
                    handle(target)
            else:
                handle(modules_)
        if cfg.get('error'):
            _error(module, cfg['error'])
        if cfg.get('ssl'):
            ssl_ = cfg['ssl']
            if isinstance(ssl_, (tuple, list)):
                _ssl(module, *ssl_)
            else:
                _ssl(module, ssl_)
        if cfg.get('favicon'):
            _favicon(module, cfg['favicon'])
        if cfg.get('not_found'):
            _not_found(module, cfg['not_found'])
        if cfg.get('shared'):
            _shared(_caller_frame(), cfg['shared'])
    else:
        raise TypeError('Type {} is not supported as config. Please use a dict.'.format(type(cfg)))


def use(*middlewares_):
    """Registers middlewares for global use"""
    _use(_caller(), *middlewares_)


def app():
    """Returns the built app"""
    return _build_app(_caller())


def run(host='127.0.0.1', port=5000, debug=False, module_name=None):
    """Runs the app"""
    global _ssl_for

    module = module_name if module_name else _caller()
    run_simple(host, port, _build_app(module), use_debugger=debug, use_reloader=debug, ssl_context=_ssl_for[module])


class Request(WRequest):
    @property
    def json(self):
        try:
            content = json.loads(self.data.decode())
        except json.JSONDecodeError:
            content = {}
        return content
