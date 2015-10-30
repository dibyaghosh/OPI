import tornado.ioloop
import tornado.web
import code,sys
from math import *
sessname = 'test'

executer = code.InteractiveInterpreter()
executer.runcode("import sys")
executer.runcode("exec(open('shell.py').read())")

execcode = """
try:
  response_to_code = str(eval(code_to_evaluate))
  print(response_to_code)
except Exception:
  try:
    exec(code_to_evaluate)
    print("Executed")
  except Exception as ex:
    print(str(ex))
"""

def runcode(interpreter, text):
  interpreter.runcode("sys.stdout = open('"+sessname+".txt','w')")
  interpreter.runcode("code_to_evaluate = " + repr(text))
  interpreter.runcode(execcode.format(text))
  sys.stdout = sys.__stdout__
  return open(sessname+'.txt').read() 

def getfunctions(interpreter):
  interpreter.runcode("sys.stdout = open('"+sessname+"_var.txt','w')")
  interpreter.runcode("print(functions())")
  sys.stdout = sys.__stdout__
  return eval(open(sessname+'_var.txt').read().strip())[0]

def heal(n):
    if "os" in n or "sys" in n:
        return '"This code is terrible"'
    return n

class MainHandler(tornado.web.RequestHandler):
        def get(self):
                self.write('<html><body><form action="/" method="POST">'
                           '<input type="text" name="message">'
                           '<input type="submit" value="Submit">'
                           '</form></body<>/html>')

        def post(self):
                self.set_header("Content-Type", "text/html")
                n = heal(str(self.get_body_argument("message")))
                self.write(runcode(executer,n))


class AngularHandler(tornado.web.RequestHandler):
        def get(self):
                self.set_header("Content-Type","text/html")
                f = open(angular_path)
                self.write(f.read())
                clear()


class VariableHandler(tornado.web.RequestHandler):
    def get(self):
            self.write(getfunctions(executer))

def clear():
    n = functions()
    for i in n[0].keys():
        exec("del "+i,globals(),globals())


angular_path = "dashboard.html"
application = tornado.web.Application([
        (r"/interpreter", MainHandler),(r'/', AngularHandler), (r'/variables',VariableHandler)
])
exec(open('shell.py').read())


if __name__ == "__main__":
        application.listen(8888)
        tornado.ioloop.IOLoop.current().start()

