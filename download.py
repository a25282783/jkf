#!/usr/bin/python3
import subprocess

# git pull 
output = subprocess.check_output(["git", "pull"])
input("任意鍵退出")