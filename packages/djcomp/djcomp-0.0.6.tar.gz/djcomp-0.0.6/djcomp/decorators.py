import inspect

class Register():

    component_apps = {}

    @classmethod
    def register_component(self,app_name,name,component):
        if not app_name in self.component_apps:
            self.component_apps[app_name] = {}
        self.component_apps[app_name][name] = component
        print("%s:%s" %(app_name,name))
        return component

    @classmethod
    def register(self,arg):
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        app_name = mod.__package__

        if isinstance(arg, str):
            def r(component):
                name = arg
                return self.register_component(app_name,name,component)
            return r
        else:
            component = arg
            return self.register_component(app_name,component.__name__,component)

register = Register.register
