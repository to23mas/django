from RestrictedPython.PrintCollector import PrintCollector
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins

# Vytvoříme dummy funkce pro path a include
def path(*args):
    return f"path{args}"

def include(*args):
    return f"include{args}"

# Vytvoříme dummy třídu Post pro testování ORM
class Post:
    class Manager:
        def get(self, **kwargs):
            return f"Post.objects.get({kwargs})"
        
        def filter(self, **kwargs):
            return f"Post.objects.filter({kwargs})"
        
        def all(self):
            return "Post.objects.all()"
    
    objects = Manager()  # Instance Manager třídy jako třídní atribut

with open('/sandbox/file.py', 'r') as file:
    code = file.read()

print_result = 'printed_result_validation_string_collection_grabber'
code += f'\n{print_result} = printed'

restricted_locals = {}

restricted_globals = {
	"__builtins__": safe_builtins,
	"_print_": PrintCollector,
	"_getattr_":  getattr,
	"path": path,      # Přidáme dummy funkce
	"include": include, # do globálního prostředí
	"Post": Post  # Přidáme dummy Post třídu
}

byte_code = compile_restricted(code, '<string>', 'exec')
exec(byte_code, restricted_globals, restricted_locals) #pylint: disable=W0122
output = restricted_locals[print_result]

print(output)
