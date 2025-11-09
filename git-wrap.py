#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

def author_get(git_hash):
    cmd = 'git show -s --format="%an" {}'.format(git_hash)
    rawlines = os.popen(cmd).readlines()
    if not rawlines:
        author = ""
    else:
        author = rawlines[0]
        author = author[0:-1].strip()
    return author

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
        index = descr.find(" ")
        git_hash = descr[0:index]
        author = author_get(git_hash)
        branch[i] = {'active': active, 'name':name, 'author':author, 'descr':descr}
        i += 1

    return branch

COLOR_RESET="\033[0;0m"

def show_branches():
    branch = branch_list_get()
    for ibranch in branch:
        br = branch[ibranch]
        if br['active']:
            select_l = '['
            select_r = ']'
            color = "\033[100m"
        else:
            select_l = ' '
            select_r = ' '
            color = ""
        print("{}{}{:>2}{} {:<42} | {:<16} {}{:>2}{} | {}{}".
            format(
                color,
                select_l,
                ibranch,
                select_r,
                br['name'],
                br['author'],
                select_l,
                ibranch,
                select_r,
                br['descr'],
                COLOR_RESET
            )
        )

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

ERR_UNKNOWN_MODE = 1
ERR_INVALID_MODE = 2
ERR_BRANCH_INDEX_NOT_SPECIFIED = 3
ERR_INVALID_BRANCH_INDEX = 4

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
        elif(mode2[-10:] == "git-rebase"):
            mode = "rebase"
            branch_index = 1
        else:
            print("Unknown exec {}".format(mode2))
            return ERR_UNKNOWN_MODE

    if(mode == "branch"):
        if(len(sys.argv) < 2):
            print("Availiable branches:")
            show_branches()
            return ERR_BRANCH_INDEX_NOT_SPECIFIED

        try:
            ibranch = int(sys.argv[branch_index])
        except:
            print("Invalid branch index")
            return ERR_INVALID_BRANCH_INDEX

        if(sys.argv[branch_index - 1] == "-d"):
            return branch_delete(ibranch, '-d')
        elif(sys.argv[branch_index - 1] == "-D"):
            return branch_delete(ibranch, '-D')
        else:
            print("Invalid command")
            return ERR_INVALID_MODE

    elif(mode == "checkout"):
        if(len(sys.argv) < branch_index + 1):
            print("Branch index not specified")
            print("Availiable branches:")
            show_branches()
            return ERR_BRANCH_INDEX_NOT_SPECIFIED
        branch = branch_list_get()
        invalid_index = False
        try:
            ibranch = int(sys.argv[branch_index])
        except:
            invalid_index = True

        if(invalid_index or not(ibranch in branch)):
            print("No such branch index")
            return ERR_INVALID_BRANCH_INDEX

        print("{} [{}] {}".format(mode, ibranch, branch[ibranch]['name'], branch[ibranch]['descr']))
        cmd = 'git checkout "{}"'.format(branch[ibranch]['name'])
        print(cmd)
        os.system(cmd)

    elif(mode == "rebase"):
        if(len(sys.argv) < branch_index + 1):
            print("Branch index not specified")
            print("Availiable branches:")
            show_branches()
            return ERR_BRANCH_INDEX_NOT_SPECIFIED

        branch = branch_list_get()
        invalid_index = False

        try:
            ibranch = int(sys.argv[branch_index])
        except:
            invalid_index = True

        if(invalid_index or not(ibranch in branch)):
            print("No such branch index")
            return ERR_INVALID_BRANCH_INDEX

        print("{} [{}] {}".format(mode, ibranch, branch[ibranch]['name'], branch[ibranch]['descr']))
        cmd = 'git rebase "{}"'.format(branch[ibranch]['name'])
        print(cmd)
        os.system(cmd)

    else:
        print("invalid argument: ", mode)
        return ERR_INVALID_MODE

    return 0

if __name__ == "__main__":
    sys.exit(main())
