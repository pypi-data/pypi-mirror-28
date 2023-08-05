import inspect
from django import template
from copy import copy
import re

register = template.Library()


from django.conf import settings
from importlib import import_module
import inspect

from ..decorators import Register

apps = settings.INSTALLED_APPS


# lay component_views o cac app
for app_name in apps:
    # try:
    #     component_module = import_module(app_name + '.components')
    #     component_views = component_module.register.__globals__[
    #         'component_views']
    #     component_apps[app_name] = component_views
    # except Exception as e:
    #     pass

    try:
        import_module(app_name + '.components')
    except Exception as e:
        pass

component_apps = Register.component_apps

media_collect = []
script_collect = []

css_src_collect = []
script_src_collect = []

for app in component_apps:

    for name in component_apps[app]:
        comp = component_apps[app][name]
        if inspect.isclass(comp):
            media = comp.media
            if media:
                media_collect.extend(media)

            script = comp.script
            if script:
                script_collect.extend(script)

            css_src = comp.css_src
            if css_src:
                css_src_collect.extend(css_src)

            script_src = comp.script_src
            if script_src:
                script_src_collect.extend(script_src)

print("Debug --------------Component template tag ")



@register.tag(name='componentmedia')
def do_componentmedia(parser,token):
    return ComponentMediaNode()

class ComponentMediaNode(template.Node):
    def render(self,*args,**kwarg):
        s = ''
        for media in media_collect:
            s += media
        for src in css_src_collect:
            s += '<link rel="stylesheet" type="text/css" href="%s">' % src
        return s

@register.tag(name='componentscript')
def do_componentscript(parser,token):
    return ComponentScriptNode()

class ComponentScriptNode(template.Node):
    def render(self,*args,**kwarg):
        s = ''
        for script in script_collect:
            s += script + '\n'
        for src in script_src_collect:
            s += '<script src="%s"></script>\n'% src
        return s

@register.tag(name='component')
def do_component(parser, token):
    return ComponentNode(parser, token)


class ComponentNode(template.Node):

    def __init__(self, parser, token):
        self.parser = parser
        self.token = token

    def get_component_view(self, component_view_str):
        bits = component_view_str.split(':')
        if len(bits) != 2:
            raise template.TemplateSyntaxError(
                "%r Error, not find component '%s'" % ('component', component_view))
        app_name = bits[0]
        component_name = bits[1]

        component_view = None
        try:
            component_view = component_apps[app_name][component_name]
            return component_view
        except Exception as e:
            template.TemplateSyntaxError(
                " %r Components error: Not find '%s:%s' component" % ('Component', app_name, component_name))

    def parse_values(self, parser, token, context):
        component_view = None
        args = []
        kwargs = {}

        bits = token.contents.split(None,2)

        component_view = parser.compile_filter(bits[1]).resolve(context,True)
        component_view = self.get_component_view(component_view)

        if len(bits) >2:
            args,kwargs = self.get_args_and_kwargs(bits[2],context.flatten())

        return component_view, args, kwargs

    # khong dung
    def parse_text(self, text):
        component_view = None
        args = []
        kwargs = {}

        bits = text.split(None, 2)

        component_view = bits[1]

        args_kwargs = bits[2].strip()

        if len(args_kwargs) != 0:
            p = re.compile(r'''((?:[^,"']|"[^"]*"|'[^']*')+)''')
            bits = p.split(args_kwargs)[1::2]
            bits = [x.strip() for x in bits]

            p = re.compile(r'''((?:[^="']|"[^"]*"|'[^']*')+)''')
            for bit in bits:
                bits2 = p.split(bit)[1::2]

                if len(bits2) == 1:
                    args.append(bits2[0].strip())
                elif len(bits2) == 2:
                    kwargs[bits2[0]] = bits2[1]

        return component_view, args, kwargs



    def get_args_and_kwargs(self,text,dict_context):

        def get_ak(*args,**kwargs):
            return args,kwargs

        dict_context.update({'get_ak': get_ak})
        try:
            return eval('get_ak(%s)' % text,{},dict_context)
        except:
            raise Exception("Component Tag: khong phan tich duoc args kwargs")

    @classmethod
    def test(self):
        n = ComponentNode(None,None)
        context = {'msg': 'xin chao', 'user_id':1}
        s = " 'user_id', user_id, msg = msg "

        args, kwargs = n.get_args_and_kwargs(s,context)

        print(args)
        print(kwargs)

    def render(self, context):

        component_view, args, kwargs = self.parse_values(
            self.parser, self.token, context)

        request = context['request']

        if inspect.isclass(component_view):
            component_instance = component_view(context)
            return component_instance.render(request,*args,**kwargs)
        else:
            return component_view(request, *args, **kwargs)
