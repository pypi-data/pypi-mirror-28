from __future__ import print_function
import sys
import json
import string

__version__ = "2.1.0"
__author__ = "Javad Shafique"

# check if string is float
def isfloat(fstring):
    return all(c in (string.digits + ".") for c in fstring) and len(fstring) > 1 

# detect type of string
def convert(data = str()):
    data = str(data) # make sure it is a string
    # Int
    if data.isdigit():
        data = int(data)
    # Float
    elif isfloat(data):
        data = float(data)

    # Bool
    elif data in ("True", "False"):
        if data == "True":
            data = True
        elif data == "False":
            data = False
    # Bool
    elif data in ("true", "false"):
        if data == "true":
            data = True
        elif data == "false":
            data = False

    # try to parse arrays as json
    elif "[" in data and "]" in data:
        try:
            data = json.loads(data)
        except json.decoder.JSONDecodeError:
            pass
        # parse dicts as json
    elif "{" in data and "}" in data:
        try:
            data = json.loads(data)
        except json.decoder.JSONDecodeError:
            pass
    if data == None:
        return True

    return data

isArg = lambda string: string[0] == "-" # checks if data starts with -

# set convert to false for python 2 support
def parse(args, detect = True):
    argv = dict() # parsed dict
    for count, thisA in enumerate(args):
        try:
            # if we are on the last argument
            if len(args) - count == 1 and isArg(thisA):
                argv.update({thisA: True})

            nextA = args[count + 1]
            
            if isArg(thisA) and isArg(nextA):
                argv.update({thisA: True})

            elif isArg(thisA) and not isArg(nextA):
                if detect:
                    argv.update({thisA: convert(nextA)})
                else:
                    argv.update({thisA: nextA})
            else:
                pass

        except IndexError:
            # No more
            break
    # return parsed dict
    return argv

class argc:
    # for python2 support set detect type to false
    def __init__(self, args = sys.argv[1:], detectType = False):
        #  dicts for infomation
        self.argc = dict()
        self.cont = dict()
        self.args = dict()
        # Options
        self.detectType = detectType
        # parse args
        self.args.update(parse(args, detectType))
    
    def add(self, command, do, exitOn = False):
        if exitOn:
            self.argc.update({command: {"do": do, "exit":True}})
        else:
            self.argc.update({command: {"do": do, "exit":False}})
    
    # extended options which supports directly to add an command
    def set(self, short, long, dest, desc, default = None, command = None, exitOn = True):
        if isArg(short) and isArg(long):
            self.cont.update({dest: {"short":short, "long":long, "desc":desc, "default":default}})
        else:
            pass

        if not command == None and isArg(short) and isArg(long):
            self.add(short, command, exitOn)
            self.add(long, command, exitOn)
            
    def get(self, string, detectType = False):
        if string in self.cont:
            base = self.cont[string]
            
            if base["short"] in self.args:
                # do something
                return convert(self.args[base["short"]]) if detectType else self.args[base["short"]]

            if base["long"] in self.args:
                # again do 
                return convert(self.args[base["long"]]) if detectType else self.args[base["long"]]

            return base["default"]

        elif string in self.args:
            # return data
            return convert(self.args[string]) if detectType else self.args[string]

        else:
            # is not set
            return None

    # generate docs from self.set
    def generate_docs(self, compact = True):
        docs = ["Options:"]
        keys = self.cont.keys()
        # loop over self.cont(ent) and add them to docs list
        for x in keys:
            base = self.cont[x]
            string = ' '.join([base["short"], base["long"] + ":", base["desc"]])
            docs.append("   " + string)

        # if compact return string
        if compact:
            return "\n".join(docs)
        # else return list
        else:
            return docs

    # run all commands
    def run(self):
        keys = self.args.keys()
        # loop for args
        for i in keys:
            # if it is in the argc (argument commands)
            if i in self.argc:
                # get base
                co = self.argc[i]
                # and get the "do"
                com = co["do"]

                # if its a list loop over it
                if type(com) == list:
                    # and for each item in that list
                    for x in com:
                        # check if it's an function
                        if hasattr(x, "__call__"):
                            # execute it
                            print(x())
                        else:
                            # else print it
                            print(x)

                # check it it's an function
                elif hasattr(com, "__call__"):
                    # execute it
                    print(com())
                else:
                    # else print it
                    print(com)
                
                # if to exit
                if co["exit"]:
                    # exit with sys.exit
                    # the best way to end
                    sys.exit(0)
