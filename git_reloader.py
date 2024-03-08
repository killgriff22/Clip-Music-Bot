import subprocess
import os
import hashlib

lastdir = [hashlib.md5(open(file).read()) if os.path.isfile(file) else file for file in os.listdir()]
process = subprocess.run("python main.py")
while True:
    new_hashes = [hashlib.md5(open(file).read()) if os.path.isfile(file) else file for file in os.listdir()]
    if new_hashes != lastdir:
        lastdir = new_hashes
        process.kill()
        process = subprocess.run("python main.py")
    else:
        os.system("git pull")