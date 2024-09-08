import re
import sys
import types
from urllib.request import urlopen
from importlib.abc import PathEntryFinder
from importlib.util import spec_from_loader, module_from_spec


class URLFinder(PathEntryFinder):
    def __init__(self, url, available):
        self.url = url
        self.available = available

    def find_spec(self, fullname, target=None):

        parts = fullname.split('.')
        path = f"{self.url}/{'/'.join(parts)}"
        

        if f"{fullname}/__init__" in self.available:
            origin = f"{path}/__init__.py"
            loader = URLLoader()
            return spec_from_loader(fullname, loader, origin=origin, is_package=True)
        
        elif fullname in self.available:
            origin = f"{path}.py"
            loader = URLLoader()
            return spec_from_loader(fullname, loader, origin=origin)
        
        raise ModuleNotFoundError(f"No module named '{fullname}'")


class URLLoader:
    def create_module(self, spec):
        module = module_from_spec(spec)
        if spec.submodule_search_locations:
            module.__path__ = spec.submodule_search_locations
        return module

    def exec_module(self, module):
        if module.__spec__.submodule_search_locations:
            url = module.__spec__.origin
        else:
            url = f"{module.__spec__.origin}"

        with urlopen(url) as page:
            source = page.read()

        code = compile(source, url, mode="exec")
        exec(code, module.__dict__)


def url_hook(some_str):
    if not some_str.startswith(("http", "https")):
        raise ImportError
    with urlopen(some_str) as page:
        data = page.read().decode("utf-8")
    
    filenames = re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*)(?:\.py|/__init__\.py)", data)
    modnames = {name for name in filenames}
    
    return URLFinder(some_str, modnames)


sys.path_hooks.append(url_hook)
sys.path.append('http://localhost:8000')

try:
    import myremotepackage
    myremotepackage.myfoo()
except Exception as e:
    print(f"Ошибка получения файла: {e}")