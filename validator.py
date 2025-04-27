from RestrictedPython.PrintCollector import PrintCollector
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins

def path(route, view, name=None):
    if name:
        return f"path({route}, {view}, name={name})"
    return f"path({route}, {view})"

def include(*args):
    return f"include{args}"

class Post:
    class Manager:
        def get(self, **kwargs):
            return f"Post.objects.get({kwargs})"

        def filter(self, **kwargs):
            return f"Post.objects.filter({kwargs})"

        def all(self):
            return "Post.objects.all()"

    objects = Manager()  

class User:
    def __init__(self):
        self.username = "johan"

class os:
    class environ:
        @staticmethod
        def get(key, default=None):
            return default

class views:
    @staticmethod
    def room(*args, **kwargs):
        return "views.room"
    
    @staticmethod
    def home(*args, **kwargs):
        return "views.home"
    
    @staticmethod
    def login(*args, **kwargs):
        return "views.login"
    
    @staticmethod
    def register(*args, **kwargs):
        return "views.register"
    
    @staticmethod
    def profile(*args, **kwargs):
        return "views.profile"
    
    @staticmethod
    def logout(*args, **kwargs):
        return "views.logout"

with open('/sandbox/file.py', 'r') as file:
    code = file.read()

print_result = 'printed_result_validation_string_collection_grabber'
code += f'\n{print_result} = printed'

user = User()

restricted_locals = {}

restricted_globals = {
    "__builtins__": safe_builtins,
    "_print_": PrintCollector,
    "_getattr_": getattr,
    "path": path,
    "include": include,
    "Post": Post,
    "user": user,
    "os": os,
    "views": views
}

byte_code = compile_restricted(code, '<string>', 'exec')
exec(byte_code, restricted_globals, restricted_locals)
output = restricted_locals[print_result]

print(output)
