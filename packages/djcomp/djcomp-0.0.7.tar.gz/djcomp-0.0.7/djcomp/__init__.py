from django.template.loader import render_to_string
from django.template.loader import get_template
from .decorators import register

class Component:

    media = []
    css_src = []
    script = []
    script_src = []

    def __init__(self,context):
        self.context = context

    def render_template(self,template,context={}):
        context.update(self.context.flatten())
        # template = get_template(template)
        # return template.render(self.context)
        return render_to_string(template,context)

    def render(self,request,*args,**kwargs):
        pass
