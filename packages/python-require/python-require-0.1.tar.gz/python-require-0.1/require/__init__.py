import importlib.util, os, inspect, re, sys

class require:

  def _path_to_name(self, path):
    return re.sub('/+', '.', re.sub('^/|_py$', '', re.sub('[^a-zA-Z0-9_/]', '_', str(path))))

  def __call__(self, module_path):
    if not os.path.isabs(module_path):
      caller_path = os.path.dirname(os.path.abspath(inspect.stack()[1][1]))
      module_path = os.path.join(caller_path, module_path)
    module_name = self._path_to_name(module_path)
    try:
      return sys.modules[module_name]
    except KeyError:
      pass
 
    if os.path.isdir(module_path):
      module_path = os.path.join(module_path, '__init__.py')

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None:
      raise ImportError(f'Could not find {module_path!r}')
  
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
  
    sys.modules[module_name] = module
  
    return module

sys.modules[__name__] = require()
