import json

# detect type of string
def detectType(data = str()):
    # int
    if data.isdigit() and detectType:
        data = int(data)
    # Float
    elif data.isdecimal and "." in data and detectType:
        data = float(data)

    # Bool
    elif data in ("True", "False") and detectType:
        if data == "True":
            data = True
        elif data == "False":
            data = False
    # Bool
    elif data in ("true", "false") and detectType:
        if data == "true":
            data = True
        elif data == "false":
            data = False

    # try to parse arrays as json
    elif "[" in data and "]" in data and detectType:
        try:
            data = json.loads(data)
        except:
            pass
        # parse dicts as json
    elif "{" in data and "}" in data and detectType:
        try:
            data = json.loads(data)
        except:
            pass
    if data == None:
        return True

    return data


isArg = lambda string: string[0] == "-" # checks if data starts with -

def keyify(Key):
  all = Key[:2]
  if all[0] == "-" and all[1] == "-":
    return Key.replace("--", "-")
  else:
    return Key.replace("-", "")

# set convert to false for python 2 support

def parse(args = list(), convert = False):
    argv = dict() # parsed dict
    for count, thisA in enumerate(args):
        try:
            # if we are on the last argument
            if len(args) - count == 1 and isArg(thisA):
                argv.update({keyify(thisA): True})

            nextA = args[count + 1]
            
            if isArg(thisA) and isArg(nextA):
                argv.update({keyify(thisA): True})

            elif isArg(thisA) and not isArg(nextA):
                if convert:
                    argv.update({keyify(thisA): detectType(nextA)})
                else:
                    argv.update({keyify(thisA): nextA})
            else:
                pass

        except IndexError:
            # No more
            break
    # return parsed dict
    return argv