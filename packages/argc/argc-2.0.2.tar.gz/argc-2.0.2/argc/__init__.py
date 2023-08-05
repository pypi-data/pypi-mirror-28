from __future__ import print_function
import sys
from .version import __version__, __author__
from .parse import parse, convert, isArg

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
        docs = ["Arguments:"]
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
                    # exit with SystemExit
                    # the best way to end
                    raise SystemExit
