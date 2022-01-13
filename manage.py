#!/usr/bin/python3

import argparse
import os
from glob import glob

UTILS_FILE = "/tmp/tdsp_utils"

parser = argparse.ArgumentParser(description='asdf')
parser.add_argument('--init', dest='init', action='store_true')
parser.add_argument('--deinit', dest='deinit', action='store_true')
parser.add_argument('--commit', dest='commit', help='asdfas')

args = parser.parse_args()

def get_submodules_list():
    if not os.path.exists('.gitmodules'):
        return []
    with open('.gitmodules', 'r') as f:
        lines = f.readlines()
    submodules = []
    for line in lines:
        if "[submodule " in line:
            splitted = line.split('"')
            submodules.append(splitted[1])
    return submodules

def checkout_branch():
    os.system("git checkout main")

def checkout_all_branches():
    d = '.'
    dirs = get_submodules_list()
    for directory in dirs:
        os.chdir(directory)
        os.system("pwd")
        checkout_branch()
        checkout_all_branches()
        os.chdir('..')

def make_commit(message):
    os.system('git add .gitignore .gitsubmodule')
    os.system('git add *')
    os.system('git commit -m ' + message)
    os.system('git push origin main')

def commit_all_submodules(message):
    d = '.'
    dirs = get_submodules_list()
    for directory in dirs:
        os.chdir(directory)
        os.system('pwd')
        commit_all_submodules(message)
        make_commit(message)
        os.chdir('..')

def commit_top_levels(message):
    while(os.getcwd() != ROOT_DIR):
        os.chdir('..')
        make_commit(message)
        os.system('pwd')
    make_commit(message)

ROOT_DIR = None

def main():
    global ROOT_DIR
    if os.path.exists(UTILS_FILE):
        with open(UTILS_FILE) as f:
            lines = f.readlines()
        ROOT_DIR = lines[1][:-1]
        print(ROOT_DIR)

    if args.init:
        if ROOT_DIR != None:
            os.system('rm -rf ' + UTILS_FILE)
            print('There was existing ML project, so it has been reinitialized.')
        os.system("echo \"root_dir\" >> " + UTILS_FILE)
        os.system("pwd >> " + UTILS_FILE)
        os.system("git checkout main")
        os.system('git branch')
        checkout_all_branches()
    elif args.deinit:
        if ROOT_DIR != None:
            os.system('rm /tmp/tdsp_utils')
            print('ML project was deinitialized')
        else:
            print('There is not any active ML projects.')
    elif args.commit != None:
        if ROOT_DIR == None:
            print('There is no initialized ML project.')
        else:
            commit_all_submodules(args.commit)
            make_commit(args.commit)
            commit_top_levels(args.commit)
        
    else:
        print("No parameters")

main()


