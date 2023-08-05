import json, string

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
