# encoding=utf-8

import glob
import os
import random
import subprocess
import sys
import time


def run_command(command):
    path = os.getenv("PATH").split(":")
    for folder in path:
        exe = os.path.join(folder, command[0])
        if os.path.exists(exe):
            p = subprocess.Popen([exe] + command[1:])
            p.wait()
            return True


def main():
    hour = time.strftime('%H')
    folder = os.path.dirname(__file__)
    pattern = "%s/sounds/%s/*.ogg" % (folder, hour)

    files = glob.glob(pattern)
    if not files:
        print "No files matching %s" % pattern
        return

    sound = random.choice(files)

    if run_command(["play", "-q", sound]):
        return

    if run_command(["paplay", sound]):
        return

    if run_command(["mplayer", sound]):
        return

    print "Don't know how to play sounds."


if __name__ == "__main__":
    main()
