import inspect
import sys

#sys.stdout = open('output','w')
var_out = open('variable_output','w')
def allvars():
    g = globals()
    g.update(locals())
    return list(g)

def functions():
    vara = allvars()
    functions = list()
    modules = list()
    variables = dict()
    for i in vara:
        if inspect.isfunction(eval(i)):
            functions.append(i)
        elif inspect.ismodule(eval(i)):
            modules.append(i)
        elif i not in irrev and i!='vara':
            variables[i] = {"name":i, "value":repr(eval(i))}
    return [variables, functions, modules]

if 'irrev' not in globals():
    irrev = []
    irrev = list(functions()[0].keys())+['response_to_code','code_to_evaluate']
    
