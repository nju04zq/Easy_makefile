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

    def get_values(self):
        return self.var_values

    def set_values(self, values):
        self.var_values= values

    @staticmethod
    def get_ref_name(value):
        if value[1] != "(" or value[-1] != ")":
            raise Exception("Ref for var not valid, " + value)
        ref_name = value[2:-1] # strip $( and )
        if ref_name.lstrip(" ") == "":
            raise Exception("Ref for a var without name, " + value)
        return ref_name

    def dump(self):
        value_str = "+++".join(self.var_values)
        print "var %s, values %s"%(self.var_name, value_str)

    def get_obj_value(self, value):
        if value.endswith(".c"):
            return "$(build_dir)/" + value[:-2] + ".o" #-2 skip trailing .c
        else:
            return value

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
    TARGET_TYPE_SO = 1
    TARGET_TYPE_BIN = 2

    def __init__(self, value, var_list):
        self.target_name = value
        self.target_var = None
        self.identify_target_type()
        self.parse_ldso(var_list)

    def identify_target_type(self):
        self.target_type = self.TARGET_TYPE_BIN
        if self.target_name.endswith(".so"):
            self.target_type = self.TARGET_TYPE_SO
    
    def is_bin_target(self):
        return self.target_type == self.TARGET_TYPE_BIN

    def parse_ldso(self, var_list):
        if self.target_type != self.TARGET_TYPE_BIN:
            return

        self.ldso_name = self.target_name + "_LDSO"
        var_stack = []
        self.reload_one_ldso_var(self.ldso_name, var_list, var_stack)

    def reload_one_ldso_var(self, var_name, var_list, var_stack):
        if var_name in var_stack:
            var_stack.append(var_name)
            raise Exception("Loop ref in ", "->".join(var_stack))

        var = self.find_ldso_var(var_name, var_list)
        if var is None:
            return

        var_stack.append(var.var_name)
        org_values = var.get_values()
        new_values = []

        one_value = ""
        flush_one_value = False
        for value in org_values:
            if value.startswith("$") or value.startswith("-L"):
                flush_one_value = True
            if one_value == "":
                flush_one_value = False
            if flush_one_value:
                new_values.append(one_value)
                one_value = ""
                flush_one_value = False
            if value.startswith("$"):
                ref_name = ContentVar.get_ref_name(value)
                self.reload_one_ldso_var(ref_name, var_list, var_stack)
            if one_value != "":
                value = " " + value
            one_value += value

        if one_value != "":
            new_values.append(one_value)

        var.set_values(new_values)
        var_stack.pop()

    def find_ldso_var(self, var_name, var_list):
        for var in var_list:
            if var.var_name == var_name:
                return var
        else:
            return None

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
            result += "\n\t$(CC) -o $@ $^ $(%s)\n"%self.ldso_name
        else:
            result += "\n\t$(CC) -shared -fPIC -o $@ $^\n"
        result += "\t@echo \"\\n=====Generated $@=====\\n\"\n"

        return result

class ContentTarget(object):
    def __init__(self, var_list):
        self.build_targets = []
        self.build_target_names = set()
        self.var_list = var_list

    def add_build_target(self, target_names):
        for value in target_names:
            if value in self.build_target_names:
                continue
            self.build_target_names.add(value)
            build_target = BuildTarget(value, self.var_list)
            self.build_targets.append(build_target)

    def get_build_targets(self):
        return self.build_targets

    def sort(self):
        self.build_targets.sort(key=lambda x:x.is_bin_target())

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
    def __init__(self, content_target, var_list, include_name, cflag_name):
        self.include_name = include_name
        self.cflag_name = cflag_name
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
            ref_name = ContentVar.get_ref_name(value)
            ref_var = self.read_var_values(ref_name, var_list,
                                           var_stack, file_list)
            if ref_var.var_idx >= var.var_idx:
                print ref_var.var_idx, var.var_idx
                raise Exception("Var %s must be defined before used"%ref_name)

        var_stack.pop()
        return var

    def find_var(self, var_name, var_list):
        for var in var_list:
            if var.var_name == var_name:
                return var
        raise Exception("Var %s not found"%var_name)

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
        cc = "\t$(CC) -o $@ $({}) $({}) -c $(filter %c,$^)\n"
        echo = "\t@echo\n\n"
        result = ""
        dir_list = self.get_build_dir_list()
        for dir_name in dir_list:
            result += "$(build_dir)/%s/%%.o: %s/%%.c\n"%(dir_name, dir_name)
            result += cc.format(self.cflag_name, self.include_name)
            result += echo
        return result

    def make_dep_rule(self):
        result = ""
        rule_str = """
\t@set -e; rm -f $@; \\
\techo "Making $@"; \\
\t$(CC) -MM $({}) $(filter %.c,$^) > $@.$$$$; \\
\tsed 's#\\($*\\)\\.o[ :]*#$(dir $@)\\1.o $@ : #g'<$@.$$$$>$@; \\
\trm -f $@.$$$$
"""
        dir_list = self.get_build_dir_list()
        for dir_name in dir_list:
            result += "$(build_dir)/%s/%%.d: "%dir_name
            result += "%s/%%.c "%dir_name
            result += "$(build_dir)/%s/.probe"%dir_name
            result += rule_str.format(self.include_name)
            result += "\n"

        return result

    def make_mkdir_rule(self):
        result = ""

        i = 0
        dir_list = self.get_build_dir_list()
        for dir_name in dir_list:
            if i != 0:
                result += " \\\n"
            result += "$(build_dir)/%s/.probe"%dir_name
            i += 1
        result += ":\n\t@mkdir -p $@\n"
        return result

class ContentInclude(object):
    def __init__(self, var):
        var.set_target(True)
        self.include_name = var.var_name
        self.parse_includes(var.var_values)

    def parse_includes(self, values):
        self.include_values = []
        include_value = ""
        for value in values:
            if value == "-I" and include_value != "":
                raise Exception("No include dir after -I")
            elif value == "-I" and include_value == "":
                include_value += value
                continue

            if include_value == "" and value.startswith("-I") == False:
                raise Exception("Include dir should start with -I, " + value)
            if include_value != "" and value.startswith("-I"):
                raise Exception("No dir found after -I, " + value)
            
            self.include_values.append(include_value+value)
            include_value = ""

    def make_include_str(self):
        tag = "{} = ".format(self.include_name)
        left_margin = len(tag)

        result = ""
        result += tag
        i = 0
        for include_value in self.include_values:
            if i != 0:
                result += (" \\\n" + left_margin*" ")
            result += include_value
            i += 1
        result += "\n\n"
        return result

class ContentCflags(object):
    def __init__(self, var):
        var.set_target(True)
        self.cflag_name = var.var_name
        self.parse_cflags(var.var_values)
        print "*"*15 + "include dirs" + "*"*15
        print self.wflags
        print self.oflags
        print "*"*30

    def parse_cflags(self, values):
        self.wflags = [] # like -Wall
        self.oflags = [] # others

        for value in values:
            self.add_one_cflag(value)

        self.sort_cflags(self.wflags)
        self.sort_cflags(self.oflags)
    
    def add_one_cflag(self, cflag):
        if cflag.startswith("-W"):
            self.wflags.append(cflag)
        else:
            self.oflags.append(cflag)

    def sort_cflags(self, cflags):
        cflags.sort()
        cflags.sort(key=lambda x:len(x))

    def add_cflags(self, cflags):
        for cflag in cflags:
            self.add_one_cflag(cflag)

        self.sort_cflags(self.wflags)
        self.sort_cflags(self.oflags)

    def make_cflag_str(self):
        tag = "{} = ".format(self.cflag_name)
        left_margin = len(tag)
        max_char = 80

        result = ""
        result += tag

        cflags = self.oflags + self.wflags

        chars_in_line = left_margin
        for cflag in cflags:
            cflag += " "
            if chars_in_line == left_margin and len(cflag) > max_char:
                chars_in_line += len(cflag)
                result += cflag
                continue

            chars_in_line += len(cflag)
            if chars_in_line > max_char:
                result += ("\\\n" + left_margin*" ")
                chars_in_line = left_margin + len(cflag)
            result += cflag

        result += "\n\n"
        return result

class ContentMk(object):
    include_name = "INCLUDE_DIR"
    cflag_name = "MK_CFLAGS"

    def __init__(self, file_name, build_defs, cflags):
        fp = open(file_name, "r")
        lines = fp.readlines()
        fp.close()

        lines = self.preprocess_lines(lines)
        self.parse_var(lines)
        self.parse_target(build_defs)
        self.parse_includes()
        self.parse_cflags()
        self.parse_dir()
        self.cflags.add_cflags(cflags)

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

    def parse_target(self, build_defs):
        self.target = ContentTarget(self.var_list)
        for var in self.var_list:
            if var.var_name in build_defs:
                self.target.add_build_target(var.var_values)
                var.set_target(True)
                build_defs.remove(var.var_name)

        if len(build_defs) != 0:
            raise Exception("These build defs not found, " + str(build_defs))

        self.target.sort()

    def parse_includes(self):
        self.includes = None
        for var in self.var_list:
            if var.var_name == self.include_name:
                self.includes = ContentInclude(var)
                break

    def parse_cflags(self):
        self.cflags = None
        for var in self.var_list:
            if var.var_name == self.cflag_name:
                self.cflags = ContentCflags(var)
                break

    def parse_dir(self):
        self.content_dir = ContentDir(self.target, self.var_list,
                                      self.include_name, self.cflag_name)

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

        makefile += self.includes.make_include_str()
        makefile += self.cflags.make_cflag_str()

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

def generate_makefile(build_defs, cflags):
    content_mk = ContentMk("content.mk", build_defs, cflags)
    content_mk.dump()
    makefile = content_mk.generate_makefile()
    fp = open("Makefile", "w")
    fp.write(makefile);
    fp.close()

build_defs = ["ch_proc_ver", "ch_lib_ver", "gvd_proc_ver", "gvd_lib_ver"]
generate_makefile(build_defs, ["-g", "-D__LINUX__"])
