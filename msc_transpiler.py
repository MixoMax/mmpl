# 
# @Author: Linus Horn
# @Contact: <linus@linush.org> || <linus.horn@uni-rostock.de>
# @Created on: 2024-11-25
# 


import re
import sys

DEBUG = True

class MSCTranspiler:
    def __init__(self):
        self.indent_level = 0
        
    def parse_range(self, range_str):
        # Parse A...B^C format
        parts = range_str.split("^")
        range_expr = parts[0]
        step = parts[1] if len(parts) > 1 else "1"
        
        start, end = range_expr.split("...")
        start = start.strip() if start.strip() else "0"
        start = self.parse_function_call(start, IF_MODE=True)
        end = self.parse_function_call(end, IF_MODE=True)
        return f"range({start}, {end}, {step})"

    def parse_function_call(self, line, IF_MODE=False):
        assert isinstance(line, str), f"line must be a string, got {type(line)}"
        line = line.strip()
        if line.startswith("if"):
            IF_MODE = True
            line = line[2:-1]
        line = line.strip()

        # Handle both function call formats
        
        # ARGS are seperated by commas
        # ARGS can be variables, literals or other function calls

        assignment_call_re = re.compile(r"((?:.*)|(?:\s*))\((.*)\)\s*\((.+)\)\s*\((.*)\)")
        normal_call_re = re.compile(r"((?:.*)|(?:\s*))?\((.*)\)\s*\((.*)\)")

        # Assignment call format: PREV (VAR) (FUNC) (ARGS)
        if match := assignment_call_re.match(line):
            prev, var, func, args = match.groups()
            if DEBUG:
                print(f"Assignment call: prev={prev}, var={var}, func={func}, args={args}")
            prev = prev.strip()

            if len(prev) != 0:
                if prev[0] == "(" and prev[-1] == ")":
                    var = f"{prev[1:-1]})({var}"
                    prev = ""
            
            if DEBUG:
                print(f"prev={prev}, var={var}, func={func}, args={args}")



            args = var + "," + args

            args = self._parse_args(args)
            
            if DEBUG:
                print(f"ARGS: {args}")

            if "(" in prev and ")" in prev:
                var = prev[prev.index("(")+1:prev.index(")")]
                prev = prev[:prev.index("(")]
                if DEBUG:
                    print(f"VAR: {var}")
                    print(f"PREV: {prev}")



            if func.startswith("!"):
                func = func[1:]
                var = args[0]
            
            if var == "":
                var = None

            if DEBUG:
                print(f"{var}={func}({', '.join(args)})")
            
            if IF_MODE:
                var = None

            if DEBUG:
                print("FUNCTION: ", func, args)

            if func.strip().startswith("?"):
                func = func.strip()[1:]
                var = None

            out = prev + self.transform_function(var, func, args, use_walrus=IF_MODE)

            if DEBUG:
                print(f"Transformed {line} to {out}")

            if normal_call_re.match(out) or assignment_call_re.match(out):
                return self.parse_function_call(out)
            return out


        # ---

        # Normal call format: (FUNC) (ARGS)

        if match := normal_call_re.match(line):
            prev, func, args = match.groups()
            prev = prev.strip()

            if DEBUG:
                print(f"Normal call: prev={prev}, func={func}, args={args}")

            if len(prev) != 0:
                if prev[0] == "(" and prev[-1] == ")":
                    args = f"{prev[1:-1]},{args}"
                    prev = ""

            


            args = self._parse_args(args)
            

            if func.startswith("!"):
                func = func[1:]
                var = args[0]
            else:
                var = None

            out = prev + self.transform_function(var, func, args)

            if DEBUG:
                print(f"Transformed {line} to {out}")

            if normal_call_re.match(out) or assignment_call_re.match(out):
                return self.parse_function_call(out)
            return out
        
        
        return line
    
    def _parse_args(self, args):
        tmp_args = [arg.strip() for arg in args.split(",")]
        parsed_args = []
        levels = {
            "bracket": 0,
            "bracket_square": 0,
            "quote": 0,
            "double_quote": 0,
        }
        current_arg = ""

        for arg in tmp_args:
            levels["bracket"] += arg.count("(") - arg.count(")")
            levels["bracket_square"] += arg.count("[") - arg.count("]")
            levels["quote"] += arg.count("'")
            levels["double_quote"] += arg.count('"')

            current_arg += arg + ","
            if levels["bracket"] == 0 and levels["bracket_square"] == 0 and levels["quote"] % 2 == 0 and levels["double_quote"] % 2 == 0:
                parsed_args.append(current_arg[:-1])
                current_arg = ""
        if current_arg:
            parsed_args.append(current_arg[:-1])

        for idx, arg in enumerate(parsed_args):
            if arg.startswith("(") and arg.endswith(")"):
                parsed_args[idx] = self.parse_function_call(arg)

        parsed_args = [arg.strip() for arg in parsed_args if arg.strip()]

        
        return parsed_args
    
    

    def get_function_args(self, func):

            function_arg_types = { # function: [arg1, arg2, ..., return_type]
                "int": ["int|float|str", "int"],
                "float": ["int|float|str", "float"],
                "str": ["Any", "str"],
                "bool": ["Any", "bool"],

                "add": ["int|float", "int|float", "int|float"],
                "sub": ["int|float", "int|float", "int|float"],
                "mul": ["int|float", "int|float", "int|float"],
                "div": ["int|float", "int|float", "float"],
                "pow": ["int|float", "int|float", "int|float"],
                "mod": ["int", "int", "int"],
                "abs": ["int|float", "int|float"],

                "max": ["list[int|float]", "int|float"],
                "min": ["list[int|float]", "int|float"],

                "split": ["str", "str", "list[str]"],
                "join": ["list[str]", "str", "str"],
                "strcat": ["str", "str", "str"],

                "len": ["list|str", "int"],

                "get": ["list|dict", "int|str", "?Any", "Any"],
                "index": ["list|str", "Any", "int"],
                "append": ["list", "Any", "list"],
                "remove": ["list", "Any", "list"],
                "pop": ["list", "int", "Any"],
                "sort": ["list", "list"],
                "reverse": ["list", "list"],
                "insert": ["list", "int", "Any", "list"],
                "count": ["list", "Any", "int"],
                "extend": ["list", "list", "list"],


                "print": ["Any|List[Any]", "None"],
                "type": ["Any", "type"],

                "eq": ["Any", "Any", "bool"],
                "neq": ["Any", "Any", "bool"],
                "gt": ["int|float", "int|float", "bool"],
                "lt": ["int|float", "int|float", "bool"],
                "gte": ["int|float", "int|float", "bool"],
                "lte": ["int|float", "int|float", "bool"],
                "and": ["bool", "bool", "bool"],
                "or": ["bool", "bool", "bool"],
                "not": ["bool", "bool"],
                "in": ["Any", "list[Any]", "bool"],

                "chr": ["int", "str"],
                "ord": ["str", "int"],
            }
            if func not in function_arg_types:
                return ["Any", "Any"]
            return function_arg_types[func]
    
    def _get_default_args(self, func):
        default_args = {
            "get": ["X", "X", "None"],
        }
        if func not in default_args:
            return []
        return default_args[func]
    

    def _literal_type(self, arg):
        if arg.isdigit():
            return "int"
        if arg.replace(".", "", 1).isdigit():
            return "float"
        if arg.startswith("'") and arg.endswith("'"):
            return "str"
        if arg in ["True", "False"]:
            return "bool"
        if arg.startswith("[") and arg.endswith("]"):
            return "list"
        if arg.startswith("{") and arg.endswith("}"):
            return "dict"
        return "Any"

    def transform_function(self, var, func, args, use_walrus=False):
        if DEBUG:
            print(f"Transforming {var}={func}({', '.join(args)})")

        function_map = {
            # casting functions
            "int": lambda x: f"int({x})",
            "float": lambda x: f"float({x})",
            "str": lambda x: f"str({x})",
            "bool": lambda x: f"bool({x})",
            "list": lambda x: f"list({x})",
            "dict": lambda x: f"dict({x})",

            # math functions
            "add": lambda x, y: f"({x} + {y})",
            "sub": lambda x, y: f"({x} - {y})",
            "mul": lambda x, y: f"({x} * {y})",
            "div": lambda x, y: f"({x} / {y})",
            "pow": lambda x, y: f"({x} ** {y})",
            "mod": lambda x, y: f"({x} % {y})",
            "abs": lambda x: f"abs({x})",
            "round": lambda x: f"round({x})",
            "max": lambda x: f"max({x})",
            "min": lambda x: f"min({x})",

            # string functions
            "split": lambda x, y: f"{x}.split({y})",
            "join": lambda x, y: f"{y}.join({x})",
            "strcat": lambda x, y: f"{x} + {y}",

            "len": lambda x: f"len({x})",

            # list functions
            "get": lambda x, y, z: f"({x}[{y}] if {y} < len({x}) else {z}) if type({x}) == list else ({x}.get({y}, {z}) if type({x}) == dict else {z})",
            "index": lambda x, y: f"{x}.index({y})",
            "append": lambda x, y: f"{x}.append({y})",
            "remove": lambda x, y: f"{x}.remove({y})",
            "pop": lambda x, y: f"{x}.pop({y})",
            "sort": lambda x: f"sorted({x})",
            "reverse": lambda x: f"{x}.reverse()",
            "insert": lambda x, y, z: f"{x}.insert({y}, {z})",
            "count": lambda x, y: f"{x}.count({y})",
            "extend": lambda x, y: f"{x}.extend({y})",


            # universal functions
            "print": lambda *x: f"print({', '.join(x)})",
            "type": lambda x: f"type({x})",

            # comparison functions
            "eq": lambda x, y: f"{x} == {y}",
            "neq": lambda x, y: f"{x} != {y}",
            "gt": lambda x, y: f"{x} > {y}",
            "lt": lambda x, y: f"{x} < {y}",
            "gte": lambda x, y: f"{x} >= {y}",
            "lte": lambda x, y: f"{x} <= {y}",
            "and": lambda x, y: f"{x} and {y}",
            "or": lambda x, y: f"{x} or {y}",
            "not": lambda x, y: f"not {x}",
            "in": lambda x, y: f"{x} in {y}",

            # char functions
            "chr": lambda x: f"chr({x})",
            "ord": lambda x: f"ord({x})",
            "lower": lambda x: f"{x}.lower()",
            "upper": lambda x: f"{x}.upper()",

        }
        
        # get function arguments and do type checking
        func_args = self.get_function_args(func)
        in_args = func_args[:-1]
        ret_arg = func_args[-1]

        n_in_args_max = len(in_args)
        n_in_args_min = len([arg for arg in in_args if not arg.startswith("?")])

        if n_in_args_min > len(args) or len(args) > n_in_args_max:
            raise ValueError(f"Function {func} expects {len(in_args)} arguments, got {len(args)}: {args}")
        
        if len(args) < n_in_args_max:
            args.extend(["X"] * (n_in_args_max - len(args)))
            default_args = self._get_default_args(func)
            for arg_idx in range(n_in_args_max):
                if default_args[arg_idx] == "X":
                    continue
                if args[arg_idx] == "X":
                    args[arg_idx] = default_args[arg_idx]

                


        for idx, (arg, in_arg) in enumerate(zip(args, in_args)):
            arg_type = self._literal_type(arg)
            if in_arg == "Any" or arg_type == "Any":
                # Either in_arg takes in Any or the arg is not a literal
                continue
            if arg_type not in in_arg.split("|"):
                raise ValueError(f"Argument [{idx+1}] of function [{func}] must be of type [{in_arg}], got [{arg_type}]")
            


        if func not in function_map:
            return f"{func}({', '.join(args)})"
        
        if DEBUG:
            print(f"{var}={func}({', '.join(args)})")
        
        result = function_map[func](*args)
        if var:
            if use_walrus:
                return f"{var} := {result}"
            return f"{var} = {result}"
        return result

    def transpile_line(self, line):
        # Handle indentation
        indent = len(line) - len(line.lstrip())
        self.indent_level = indent // 4
        line = line.strip()
        
        # Skip empty lines
        if not line:
            return ""
            
        # Handle for loops
        if line.startswith("for"):

            # Handle X...Y^Z range format
            match = re.match(r"for\s+(\w+)\s+in\s+(.+):", line)
            if match:
                var, range_expr = match.groups()
                if DEBUG:
                    print(f"FORLOOP: var={var}, range_expr={range_expr}")

                if "..." in range_expr:
                    range_expr = self.parse_range(range_expr)
                else:
                    range_expr = self.parse_function_call(range_expr, IF_MODE=True)
                return f"{'    ' * self.indent_level}for {var} in {range_expr}:"
            
            # Handle for loops with function call
            func_call = line[line.index("("):-1]
            return f"{'    ' * self.indent_level}for {self.parse_function_call(func_call)}:"
        
        # Handle while loops
        if line.startswith("while"):
            return f"{'    ' * self.indent_level}{line}"
            
        # Handle if statements
        if line.startswith("if"):
            return f"{'    ' * self.indent_level}if {self.parse_function_call(line, IF_MODE=True)}:"
            
        # Handle break and continue
        if line in ["break", "continue"]:
            return f"{'    ' * self.indent_level}{line}"
            
        # Handle function calls
        if "(" in line:
            return f"{'    ' * self.indent_level}{self.parse_function_call(line)}"

        # Handle variable assignments
        if "=" in line:
            var, expr = line.split("=")
            return f"{'    ' * self.indent_level}{var.strip()} = {self.parse_function_call(expr.strip())}"
        
        return f"{'    ' * self.indent_level}{line}"

    def transpile(self, msc_code):
        python_code = []
        
        for line in msc_code.split("\n"):
            if line.strip():
                # Update indent level
                if line.strip().endswith(":"):
                    self.indent_level += 1
                elif self.indent_level > 0 and len(line) - len(line.lstrip()) < self.indent_level * 4:
                    self.indent_level = (len(line) - len(line.lstrip())) // 4
                try:
                    python_code.append(self.transpile_line(line))
                except Exception as e:
                    print(f"Error in line: {line}")
                    print(e, type(e))
                    return ""
                    
            
        return "\n".join(python_code)


def main():
    argv = sys.argv
    argc = len(argv)

    if argc < 3:
        print("Usage: python(3) msc_transpiler.py <input_file.msc> <output_file.py>")
        return
    
    input_file = argv[1]
    output_file = argv[2]

    with open(input_file, "r") as f:
        msc_code = f.read()

    transpiler = MSCTranspiler()
    python_code = transpiler.transpile(msc_code)

    with open(output_file, "w") as f:
        f.write(python_code)


if __name__ == "__main__":
    main()