from django import template

register = template.Library()

@register.tag(name='raw_python')
def do_raw_python(parser,token):
    print("DEBUG --------------")
    node = parser.parse(('end_raw_python',))
    parser.delete_first_token()
    return RawPythonNode(node)

class RawPythonNode(template.Node):

    def __init__(self,node):
        self.node = node

    def render(self,context):
        text = self.node.render(context)
        exec(text,{},{'context': context})
        return ''
