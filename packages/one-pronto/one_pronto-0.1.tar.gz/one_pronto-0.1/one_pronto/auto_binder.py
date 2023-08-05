import japronto
import os
import importlib
from functools import wraps
import inspect
from collections import OrderedDict


class JaprontoAutoBinder(japronto.Application):
    routes_dir = None

    def _imp(self, name):
        return importlib.import_module(name, package=os.path.join(self.routes_dir, name))

    @staticmethod
    def _create_response(f):
        @wraps(f)
        async def wrapped_async_call(request):
            resp = await f(request)
            return request.Response(text=resp)

        @wraps(f)
        def wrapped_sync_call(request):
            return request.Response(text=f(request))

        if inspect.iscoroutinefunction(f):
            return wrapped_async_call
        return wrapped_sync_call

    @staticmethod
    def _has_specify_args(f):
        return len(inspect.signature(f).parameters) > 1

    @staticmethod
    def _params_str(f):
        parameters = OrderedDict(inspect.signature(f).parameters)
        parameters.pop('request')

        return '/' + '/'.join('{' + arg_name + '}' for arg_name in parameters.keys())

    @staticmethod
    def _call_with_args(f):
        def wrapped_call(request):
            kwargs = request.match_dict
            return f(request, **kwargs)

        return wrapped_call

    def _init_modules(self):
        modules_list = (x for x in next(os.walk(self.routes_dir))[1])

        modules = {module_name: self._imp(module_name) for module_name in modules_list}

        for module_name in modules:
            for method_name in dir(modules[module_name]):
                if method_name.startswith('_') or not callable(getattr(modules[module_name], method_name)):
                    continue

                url = module_name

                method = getattr(modules[module_name], method_name)

                if self._has_specify_args(method):
                    url = url + self._params_str(method)
                    method = self._call_with_args(method)

                method = self._create_response(method)
                self.router.add_route('/{url}'.format(url=url), method, method_name.upper())

    def start_serve(self, routes_dir):
        self.routes_dir = routes_dir

        if not os.path.exists(self.routes_dir):
            raise FileNotFoundError(self.routes_dir)

        self._init_modules()
        self.run()
