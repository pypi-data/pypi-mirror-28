from functools import wraps
from inspect import signature, getsourcelines, getclosurevars
from textwrap import indent, dedent
from types import ModuleType
import re

CODE_INDENT = '    '

EXPORT_FUNCTION_SIGNATURE = 'def exported_pipeline(df):\n'

STEP_CODE_PREFIX = indent('\ndataframe = df.copy()\n\n', CODE_INDENT)

STEP_CODE_SUFFIX = indent('return dataframe', CODE_INDENT)

def replace(string, substitutions):
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)

class RenderableFunction(object):

    def __init__(self, function):
        self.function = function
        self.substitutions = {}
        self.get_module_dependencies()

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def render_code(self, **kwargs):

        substitutions = {}
        comment = ''

        if 'code_comment' in kwargs:
            for line in kwargs['code_comment'].split('\n'):
                comment += '#' + line + '\n'

        code = getsourcelines(self.function)

        #[2:-1] slice removes decorator, declaration and return statement
        code = dedent("".join(code[0][2:-1]))

        for arg_name in signature(self.function).parameters.keys():
            if arg_name in kwargs:
                if isinstance(kwargs[arg_name], type):
                    substitutions[arg_name] = kwargs[arg_name].__name__
                else:
                    substitutions[arg_name] = repr(kwargs[arg_name])

        substitutions.update(self.substitutions)

        if substitutions:
            code = replace(code, substitutions)

        return indent(comment + code, CODE_INDENT)

    def get_module_dependencies(self):
        import_list = []
        import_statement = None

        for name,imported in getclosurevars(self.function).globals.items():

            if hasattr(imported, "__module__"):
                import_statement = 'from {0} import {1}'.format(
                    imported.__module__,
                    imported.__name__
                )

                if (imported.__name__ != name):
                    import_statement += ' as {0}'.format(name)

                import_statement += '\n'
            elif isinstance(imported, ModuleType):
                import_statement = 'import {0} as {1}\n'.format(
                    imported.__name__,
                    name
                )
            else:
                self.substitutions[name] = repr(imported)

            if import_statement:
                import_list += [indent(import_statement, CODE_INDENT)]

        return import_list

def renderable(function):
    wrapped = RenderableFunction(function)
    return wraps(function)(wrapped)