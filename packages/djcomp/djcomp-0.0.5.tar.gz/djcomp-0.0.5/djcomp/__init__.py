from django.template.loader import render_to_string

from .decorators import register

class Component:

    media = []
    css_src = []
    script = []
    script_src = []

    def __init__(self,context):
        self.context = context

    def render_template(self,*args,**kwargs):
        return render_to_string(*args,**kwargs)

    def render(self,request,*args,**kwargs):
        pass
