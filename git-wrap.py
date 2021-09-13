#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

def branch_list_get():
    cmd = 'git branch --list --no-color -v'
    rawlines = os.popen(cmd).readlines()

    branch = {}
    i = 1
    for rawline in rawlines:
        utf8line = rawline
        str_active = utf8line[0:1]
        active = (str_active == "*")
        rest = utf8line[2:-1]
        index = rest.find(" ")
        name = rest[0:index]
        descr = rest[index:-1].strip()
        branch[i] = {'active': active, 'name':name, 'descr':descr}
        i += 1

    return branch

def show_branches():
    branch = branch_list_get()
    for ibranch in branch:
        if branch[ibranch]['active']:
            print("[{:>2}] {:<30} [{:>2}] {}".format(ibranch, branch[ibranch]['name'], ibranch, branch[ibranch]['descr']))
        else:
            print(" {:>2}  {:<30}  {:>2}  {}".format(ibranch, branch[ibranch]['name'], ibranch, branch[ibranch]['descr']))

def branch_delete(ibranch, mode):
    branch = branch_list_get()
    if(not(ibranch in branch)):
        print("No such branch index")
        return 4
    else:
        print("Delete [{}] {}".format(ibranch, branch[ibranch]['name'], branch[ibranch]['descr']))
        cmd = 'git branch {} "{}"'.format(mode, branch[ibranch]['name'])
        print(cmd)
        os.system(cmd)

def main():
    mode2 = sys.argv[0]
    if(mode2[-11:] == "git-wrap.py"):
        mode = sys.argv[1]
    else:
        if(mode2[-10:] == "git-branch"):
            branch_index = 2
            mode = "branch"
        elif(mode2[-12:] == "git-checkout"):
            mode = "checkout"
            branch_index = 1
        else:
            print("Unknown exec")
            return 1

    if(mode == "branch"):
        if(len(sys.argv) < 2):
            print("Availiable branches:")
            show_branches()
            return 3

        try:
            ibranch = int(sys.argv[branch_index])
        except:
            print("Invalid branch index")
            return 4


        if(sys.argv[branch_index - 1] == "-d"):
            return branch_delete(ibranch, '-d')
        elif(sys.argv[branch_index - 1] == "-D"):
            return branch_delete(ibranch, '-D')
        else:
            print("Invalid command")
            return 3
    elif(mode == "checkout"):
        if(len(sys.argv) < branch_index + 1):
            print("Branch index not specified")
            print("Availiable branches:")
            show_branches()
            return 3
        branch = branch_list_get()
        invalid_index = False
        try:
            ibranch = int(sys.argv[branch_index])
        except:
            invalid_index = True
        if(invalid_index or not(ibranch in branch)):
            print("No such branch index")
            return 4
        else:
            print("{} [{}] {}".format(mode, ibranch, branch[ibranch]['name'], branch[ibranch]['descr']))
            cmd = 'git checkout "{}"'.format(branch[ibranch]['name'])
            print(cmd)
            os.system(cmd)
    else:
        print("invalid argument: ", mode)
        return 2
    return 0




if __name__ == "__main__":
    sys.exit(main())
