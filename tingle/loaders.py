import importnb
import tingle

__all__ = "Markdown", "RST", "YAML"


class LiterateMixin(importnb.Notebook):
    format = None

    def get_data(self, path):
        if self.path.endswith(self.format):
            return self.code(self.decode())
        return super().get_data(path)

    get_source = get_data


class Markdown(LiterateMixin):
    format = ".md"
    extensions = F".py{format} {format} {format}.ipynb".split()

    def code(self, str):
        return tingle.python.md2py(str)

    def exec_module(self, module):
        super().exec_module(module)
        module._ipython_display_ = lambda: print(module.__file__) or __import__(
            "IPython").display.display(__import__("IPython").display.Markdown(filename=module.__file__))


class RST(LiterateMixin):
    format = 'rst'
    extensions = F".py.{format} .{format} .{format}.ipynb".split()

    def code(self, str):
        return tingle.python.rst2py(str)


class LiterateDataMixin(LiterateMixin):

    def code(self, code):
        if self.path.endswith(".md"):
            return tingle.yml.md2yml(code)

        if self.path.endswith(".rst"):
            return tingle.yml.rst2yml(code)
        return code


class YAML(LiterateDataMixin):
    format = '.md'
    extensions = F".yml .yaml .yml.md .yaml.md".split()

    def code(self, str):
        code = F"""data = __import__('yaml').safe_load('''{super().code(str)}''')"""
        return code

    def exec_module(self, module):
        super().exec_module(module)
        module._ipython_display_ = lambda:  __import__(
            "IPython").display.display(__import__("IPython").display.JSON(module.data, root=module.__file__))
