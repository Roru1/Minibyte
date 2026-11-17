class function:
    def __init__(self,func,args):
        self.func = func
        self.args = args
    def __repr__(self):
        return f"command:{self.func} arguments:{self.args}"

from math import prod, sin, cos
import re
import random
import os
import time
safe_globals = {}

STRING  = r'"[^"]*"'
NUMBER  = r'-?\d+(?:\.\d+)?'
NAME    = r'[A-Za-z_]\w*'
OPERAND = rf'(?:{STRING}|{NUMBER}|{NAME})'
COND    = rf'{OPERAND}(?:==|!=|<=|>=|[<>=]){OPERAND}'      # 4>d   z="y"
ARRAY   = rf'\[\s*(?:(?:{STRING}|{NUMBER})(?:\s*,\s*(?:{STRING}|{NUMBER}))*)?\s*\]'
TAGGED  = r'\w+:\w+'                                        # err:null
TOKEN   = rf'(?:{COND}|{ARRAY}|{STRING}|{TAGGED}|{NUMBER}|{NAME})'
LINE    = re.compile(rf'\s*({NAME})((?:\s+{TOKEN})*)\s*')
FUNCTIONDECLERATION = re.compile(rf'{NAME}\(')

def call(name):
    global codes
    if name not in codes:
        raise NameError(f"no function {name}")

    for cmd in codes[name]:
        if run(cmd) == "stop it now":
            break



def dispatcher(string, index):
    string = string.strip()
    m = FUNCTIONDECLERATION.fullmatch(string)
    if not m:
        pass
    else:
        return string[:-1]
    m = LINE.fullmatch(string)
    if not m:
        if string==")":
            return 8652
            print("ended the thing")
        else:
            return None
    return function(m.group(1), re.findall(TOKEN, m.group(2)))

def join(tojoin):
    global namespace
    string = ""
    for n in tojoin:
        string += str(eval(f"str({n})",safe_globals,namespace))
    return string

safe_globals["join"],safe_globals["prod"],safe_globals["randint"] = join,prod,random.randint


def run(minifunc):
    global namespace
    numtype = "int"
    if minifunc.func in ("add", "sub", "mul", "div", "exp", "sqr", "sqrt"):
        for l in minifunc.args[1:]:
            if l in codes:
                continue
            l = eval(l,safe_globals,namespace)
            if isinstance(l,float):
                numtype = "float"
            elif isinstance(l,int):
                pass #print("integer lol")
            else:
                pass # hmm
    match(minifunc.func):
        case "add":
            exec(f"{minifunc.args[0]} = sum([{numtype}(j) for j in {[eval(h,safe_globals,namespace) for h in minifunc.args[1:]]}])",safe_globals,namespace)
        case "prt"|"dpt":
            exec(f"print({minifunc.args[0]})",safe_globals,namespace)
        case "int"|"sic":
            exec(f"{minifunc.args[0]} = int(float({minifunc.args[1]}))",safe_globals,namespace)
        case "qry":
            exec(f"{minifunc.args[0]} = input()",safe_globals,namespace)
        case "jns":
            exec(f"{minifunc.args[0]} = join({minifunc.args[1:]})",safe_globals,namespace)
        case "run":
            call(minifunc.args[0])
        case "str"|"ssc"|"isc":
            exec(f"{minifunc.args[0]} = str({minifunc.args[1]})", safe_globals, namespace)
        case "lwc":
            exec(f"{minifunc.args[0]} = {minifunc.args[1]}.lower()", safe_globals, namespace)
        case "len":
            exec(f"{minifunc.args[0]} = len({minifunc.args[1]})", safe_globals, namespace)
        case "sac":
            exec(f"{minifunc.args[0]} = list(str({minifunc.args[1]}))", safe_globals, namespace)
        case "arr":
            exec(f"{minifunc.args[0]} = eval('{minifunc.args[1]}')", safe_globals, namespace)
        case "loop" | "lpf":
            for _ in range(eval(minifunc.args[0],safe_globals,namespace)):
                call(minifunc.args[1])
        case "idx":
            exec(f"{minifunc.args[0]} = {minifunc.args[1]}[{minifunc.args[2]}]", safe_globals, namespace)
        case "fnd":
            exec(f"{minifunc.args[0]} = {minifunc.args[1]}.index({minifunc.args[2]})", safe_globals, namespace)
        case "if" | "iff":
            if eval(" ".join(minifunc.args[:-1]),safe_globals,namespace):
                call(minifunc.args[-1])
        case "sub":
            exec(f"uuuuuuuuuhhsd = [{numtype}(j) for j in {[eval(h,safe_globals,namespace) for h in minifunc.args[1:]]}]",safe_globals,namespace)
            exec(f"{minifunc.args[0]} = uuuuuuuuuhhsd[0]-sum(uuuuuuuuuhhsd[1:])",safe_globals,namespace)
        case "mul":
            exec(f"{minifunc.args[0]} = prod([{numtype}(j) for j in {[eval(h,safe_globals,namespace) for h in minifunc.args[1:]]}])",safe_globals,namespace)
        case "div":
            exec(f"{minifunc.args[0]} = {numtype}({minifunc.args[1]})/{numtype}({minifunc.args[2]})",safe_globals,namespace)
        case "flt"|"ifc":
            exec(f"{minifunc.args[0]} = float({minifunc.args[1]})",safe_globals,namespace)
        case "ctn":
            exec(f"{minifunc.args[0]} = {minifunc.args[2]} in {eval(minifunc.args[1],safe_globals,namespace)}",safe_globals,namespace)
        case "clr":
            os.system('cls' if os.name == 'nt' else 'clear')
        case "cry":
            print(":(")
        case "rdi":
            exec(f"{minifunc.args[0]} = randint({minifunc.args[1]},{minifunc.args[2]})",safe_globals,namespace)
        case "unf"|"until":
            while not eval(f"{minifunc.args[0]}",safe_globals,namespace):
                call(minifunc.args[1])
        case "blu"|"blue":
            print("\033[94m",end="")
        case "end":
            print("PROGRAM ENDED")
            exit()
        case "brk":
            return "stop it now"
        case "rdf":
            exec(f"{minifunc.args[0]} = random({minifunc.args[1]},{minifunc.args[2]})",safe_globals,namespace)
        case "exp":
            exec(f"{minifunc.args[0]} = {numtype}({minifunc.args[1]})**{numtype}({minifunc.args[2]})", safe_globals, namespace)
        case "sqr"|"sqrt":
            exec(f"{minifunc.args[0]} = float({minifunc.args[1]})**0.5", safe_globals, namespace)
        case "slp":
            time.sleep(float(minifunc.args[0]))
        case "mod":
            exec(f"{minifunc.args[0]} = {numtype}({minifunc.args[1]})%{numtype}({minifunc.args[2]})", safe_globals, namespace)
        case "wit"|"wte"|"white":
            print("\033[0m",end="")
        case "dtb":
            exec(f"{minifunc.args[0]} = {'{0:b}'.format(int(eval(minifunc.args[1], safe_globals, namespace)))}", safe_globals, namespace)
        case "btd":
            exec(f"{minifunc.args[0]} = int(str({minifunc.args[1]}),2)", safe_globals, namespace)
        case "txi":
            with open(eval(minifunc.args[1], safe_globals, namespace),mode="r") as file:
                namespace[minifunc.args[0]] = file.read()
        case "txe":
            with open(eval(minifunc.args[1], safe_globals, namespace), mode="w") as file:
                temp = eval(f"{minifunc.args[0]}", safe_globals, namespace)
                file.write(temp)
        case "txl":
            with open(eval(minifunc.args[1], safe_globals, namespace), mode="r") as file:
                namespace[minifunc.args[0]] = file.read().splitlines()[int(eval(minifunc.args[2], safe_globals, namespace))]
        case "sin":
            exec(f"{minifunc.args[0]} = sin(float({minifunc.args[1]}))", safe_globals, namespace)
        case "cos":
            exec(f"{minifunc.args[0]} = cos(float({minifunc.args[1]}))", safe_globals, namespace)
        case "amb":
            exec(f"run(dispatcher({minifunc.args[0]},1))", safe_globals, namespace)
        case "apy":
            print("Nope")
        case "rpl":
            exec(f"namespace[{minifunc.args[0]}][{minifunc.args[1]}] = {minifunc.args[2]}", safe_globals, namespace)
        case "app":
            exec(f"namespace[{minifunc.args[0]}] += {minifunc.args[1]}", safe_globals, namespace)
        case "pop":
            exec(f"namespace[{minifunc.args[0]}].pop()", safe_globals, namespace)
        case "rmv":
            exec(f"namespace[{minifunc.args[0]}].pop(int({minifunc.args[1]}))", safe_globals, namespace)
        case _:
            print(f"{minifunc.func} is undefined, define it, now")
    return None
safe_globals = {
    "join":join,
    "prod":prod,
    "randint":random.randint,
    "random":random.uniform,
    "sleep":time.sleep,
    "sin":sin,
    "cos":cos,
    "dispatcher":dispatcher,
    "runmb":run
}

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    script = input("Load script: ")
    os.system('cls' if os.name == 'nt' else 'clear')
    if script == "":
        script = "localscript.mb"

    with open(script, mode="r") as file:
       minibyte = file.read().splitlines()
    index = 0
    codes = {}
    functions = {}
    for x in minibyte:
        thingy = dispatcher(x,index)
        if not thingy:
          pass
        elif isinstance(thingy,str):
            functions[thingy] = index
            key = thingy
        elif isinstance(thingy, int):
           functions[key] = (functions[key],index,key)
           codes[key] = []
        else:
           pass #print("not yet :3") if you're feeling cute and debuggable
        index+=1
    index = 0
    for x in minibyte:
        thingy = dispatcher(x, index)
        if not thingy:
            pass
        elif isinstance(thingy, str):
            pass
        elif isinstance(thingy, int):
            pass
        else:
            for c in functions.values():
                if c[0] < index < c[1]:
                    codes[c[2]].append(thingy)
        index += 1
    namespace = {}
    index = 0
    call("main")
    print("PROGRAM ENDED")
