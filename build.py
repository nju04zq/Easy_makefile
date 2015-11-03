import os

build_dir = "./build"

class ContentVar(object):
    def __init__(self, var_line, var_idx):
        print "var_line " + var_line 
        token_list = var_line.split("=")
        if len(token_list) != 2:
            raise Exception("Variable def not valid, " + var_line)
        self.var_idx = var_idx
        self.var_name = self.parse_name(token_list[0])
        self.var_values = self.parse_values(token_list[1])
        self.var_is_target = False

    def parse_name(self, token):
        token = token.lstrip(" ")
        token = token.rstrip(" ")
        return token
    
    def parse_values(self, token):
        token = token.lstrip(" ")
        token = token.rstrip(" ")
        values = token.split(" ")
        values = self.remove_empty_value(values)
        return values

    def remove_empty_value(self, values):
        values_new = []
        for value in values:
            if value != "":
                values_new.append(value)
        return values_new
    
    def set_target(self, is_target):
        self.var_is_target = is_target

    def dump(self):
        value_str = "+++".join(self.var_values)
        print "var %s, values %s"%(self.var_name, value_str)

    def get_obj_value(self, value):
        return "$(build_dir)/" + value[:-2] + ".o" #-2 skip trailing .c

    def make_def_str(self):
        if self.var_is_target:
            return ""

        tag = "%s = "%self.var_name
        result = ""
        result += tag
        result += self.make_value_def(len(tag))
        result += "\n\n"
        return result

    def make_value_def(self, left_margin):
        result = ""
        i = 0
        for value in self.var_values:
            if i != 0:
                result += " \\\n"
                result += " "*left_margin
            if value.startswith("$") == False:
                value = self.get_obj_value(value)
            result += value
            i += 1
        return result

class BuildTarget(object):
    TARGET_TYPE_BIN = 1
    TARGET_TYPE_SO = 2

    def __init__(self, value):
        self.target_name = value
        self.target_var = None
        self.identify_target_type()

    def identify_target_type(self):
        self.target_type = self.TARGET_TYPE_BIN
        if self.target_name.endswith(".so"):
            self.target_type = self.TARGET_TYPE_SO

    def set_var(self, var):
        self.target_var = var
        self.target_var.set_target(True)

    def dump(self):
        print self.target_name

    def make_target_str(self):
        return build_dir + os.sep + self.target_name

    def make_target_def(self):
        tag = "$(build_dir)/%s: "%self.target_name
        left_margin = len(tag)

        result = ""
        result += tag
        result += self.target_var.make_value_def(left_margin)
        if self.target_type == self.TARGET_TYPE_BIN:
            result += "\n\t$(CC) -o $@ $^\n"
        else:
            result += "\n\t$(CC) -o $@ $^\n"

        return result

class ContentTarget(object):
    def __init__(self, values):
        self.build_targets = []
        for value in values:
            build_target = BuildTarget(value)
            self.build_targets.append(build_target)

    def get_build_targets(self):
        return self.build_targets

    def dump(self):
        print "#"*10 + " build targets " + "#"*10
        for build_target in self.build_targets:
            build_target.dump()
        print "#"*20

    def make_target_list(self):
        left_margin = 0
        result = ""
        result += ".PHONY: all\n"
        result += "all: "
        left_margin = len("all: ")

        i = 0
        for build_target in self.build_targets:
            target_str = build_target.make_target_str()
            if i != 0:
                result += (" \\\n" + " "*left_margin)
            result += target_str
            i += 1

        result += "\n\n"
        return result

    def make_target_def(self):
        result = ""
        for build_target in self.build_targets:
            result += build_target.make_target_def()
            result += "\n"
        return result

class ContentDir(object):
    def __init__(self, content_target, var_list):
        self.build_dirs = {}
        build_targets = content_target.get_build_targets()
        for build_target in build_targets:
            self.read_build_target(build_target, var_list)

    def read_build_target(self, build_target, var_list):
        var_stack = []
        file_list = []
        var_name = build_target.target_name

        var = self.read_var_values(var_name, var_list, var_stack, file_list)
        build_target.set_var(var)

        for one_file in file_list:
            self.add_build_dir(one_file)

    def add_build_dir(self, one_file):
        dir_name, file_name = self.get_dir_name(one_file)
        
        file_name = file_name[:-2] # strip trailing .c
        
        build_dir = self.build_dirs.get(dir_name)
        if build_dir is None:
            self.build_dirs[dir_name] = [file_name]
        elif file_name not in build_dir:
            build_dir.append(file_name)
            build_dir.sort()

    def read_var_values(self, var_name, var_list, var_stack, file_list):
        if var_name in var_stack:
            var_stack.append(var_name)
            raise Exception("Var ref loop found, " + "->".join(var_stack))

        var_stack.append(var_name)
        var = self.find_var(var_name, var_list)

        for value in var.var_values:
            if value.startswith("$") == False:
                file_list.append(value)
                continue
            ref_name = self.get_ref_name(value)
            ref_var = self.read_var_values(ref_name, var_list,
                                           var_stack, file_list)
            if ref_var.var_idx >= var.var_idx:
                print ref_var.var_idx, var.var_idx
                raise Exception("Var %s must be defined before used"%ref_name)

        return var

    def find_var(self, var_name, var_list):
        for var in var_list:
            if var.var_name == var_name:
                return var
        raise Exception("Var %s not found"%var_name)

    def get_ref_name(self, value):
        if value[1] != "(" or value[-1] != ")":
            raise Exception("Ref for var not valid, " + value)
        ref_name = value[2:-1]
        if ref_name.lstrip(" ") == "":
            raise Exception("Ref for a var without name, " + value)
        return ref_name

    def get_dir_name(self, one_file):
        file_name = os.path.basename(one_file)
        if file_name.endswith(".c") == False:
            raise Exception("Should include .c file, " + one_file)
        dir_name = os.path.dirname(one_file)
        return dir_name, file_name

    def get_build_dir_list(self):
        dir_list = self.build_dirs.keys()
        dir_list.sort()
        return dir_list

    def dump(self):
        print "#"*10 + " dir list " + "#"*10
        dir_list = self.get_build_dir_list()
        for dir_name in dir_list:
            print dir_name
        print "#"*20

    def make_include_dep_each_dir(self, dir_name):
        build_dir = self.build_dirs[dir_name]

        result = ""
        for file_name in build_dir:
            result += "-include $(build_dir)/%s/%s.d\n"%(dir_name, file_name)
        return result

    def make_include_dep(self):
        result = ""
        result += "ifneq ($(MAKECMDGOALS), clean)\n"

        dir_list = self.get_build_dir_list()
        for dir_name in dir_list:
            result += self.make_include_dep_each_dir(dir_name)

        result += "endif\n\n"
        return result

    def make_obj_rule(self):
        result = ""
        dir_list = self.get_build_dir_list()
        for dir_name in dir_list:
            result += "$(build_dir)/%s/%%.o: %s/%%.c\n"%(dir_name, dir_name)
            result += "\t$(CC) -o $@ -c $(filter %c, $^)\n\n"
        return result

    def make_dep_rule(self):
        result = ""
        rule_str = """
\t@set -e; rm -f $@; \\
\techo "Making $@"; \\
\t$(CC) -MM $(filter %.c,$^) > $@.$$$$; \\
\tsed 's#\\($*\\)\\.o[ :]*#$(dir $@)\\1.o $@ : #g'<$@.$$$$>$@; \\
\trm -f $@.$$$$
"""
        dir_list = self.get_build_dir_list()
        for dir_name in dir_list:
            result += "$(build_dir)/%s/%%.d: "%dir_name
            result += "%s/%%.c "%dir_name
            result += "$(build_dir)/%s/.probe"%dir_name
            result += rule_str
            result += "\n"

        return result

    def make_mkdir_rule(self):
        result = ""

        i = 0
        dir_list = self.get_build_dir_list()
        for dir_name in dir_list:
            if i != 0:
                result += " "
            result += "$(build_dir)/%s/.probe"%dir_name
            i += 1
        result += ":\n\t@mkdir -p $@\n"
        return result

class ContentMk(object):
    def __init__(self, file_name):
        fp = open(file_name, "r")
        lines = fp.readlines()
        lines = self.preprocess_lines(lines)
        self.parse_var(lines)
        self.parse_target()
        self.parse_dir()
        fp.close()

    def preprocess_lines(self, lines):
        new_lines = []
        for line in lines:
            line = line.rstrip("\n")
            line = line.replace("\t", " ")
            line = line.lstrip(" ")
            line = line.rstrip(" ")
            new_lines.append(line)
        return new_lines

    def parse_var(self, lines):
        self.var_list = []
        var_line = ""
        var_idx = 0
        for line in lines:
            if line == "" and var_line == "":
                continue

            if line.startswith("#"):
                continue

            var_line += line

            if line.endswith("\\"):
                var_line = var_line[:-1] + " "
                continue

            var = ContentVar(var_line, var_idx)
            self.var_list.append(var)
            var_line = ""
            var_idx += 1

    def parse_target(self):
        for var in self.var_list:
            if var.var_name == "target":
                self.target = ContentTarget(var.var_values)
                var.set_target(True)
                break

    def parse_dir(self):
        self.content_dir = ContentDir(self.target, self.var_list)

    def dump(self):
        print "#"*10 + " var list " + "#"*10
        for var in self.var_list:
            var.dump()
        print "#"*20
        self.target.dump()
        self.content_dir.dump()

    def generate_makefile(self):
        makefile = ""
        makefile += "build_dir=%s\n\n"%build_dir
        makefile += "CC=gcc\n\n"

        makefile += self.target.make_target_list()
        makefile += self.content_dir.make_include_dep()

        for var in self.var_list:
            makefile += var.make_def_str()

        makefile += self.target.make_target_def()

        makefile += self.content_dir.make_obj_rule()
        makefile += self.content_dir.make_dep_rule()
        makefile += self.content_dir.make_mkdir_rule()
        makefile += self.make_clean()
        return makefile

    def make_clean(self):
        result = """
.PHONY: clean
clean:
\t-rm -rf $(build_dir)/*
"""
        return result

def generate_makefile():
    content_mk = ContentMk("content.mk")
    content_mk.dump()
    makefile = content_mk.generate_makefile()
    fp = open("Makefile", "w")
    fp.write(makefile);
    fp.close()

generate_makefile()
