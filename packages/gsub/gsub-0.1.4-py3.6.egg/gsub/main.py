# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import subprocess
import shutil
import six


def locate_git():
    cd = os.getcwd()
    while True:
        if os.path.isdir(os.path.join(cd, ".git")):
            return cd
        ncd = os.path.dirname(cd)
        if ncd == cd:
            return False
        cd = ncd


def show_help():
    print("""usage: gsub [--version] [--help] <command> <args>

Commands:

  list          List all gsub folders.
  freeze        Update gsub files based on content of managed folders.
  update        Create/update managed folders based on gsub files.
  vendor PATH   Add a new gsub file.""")
    sys.exit(1)


def show_version():
    print("gsub: v0.1.4")
    raise SystemExit


def parse(pth):
    with open(pth) as fd:
        first = fd.readline()
        if not first:
            raise Exception("error: empty file (%s)" % pth)

        parts = first.split()
        if len(parts) > 2:
            raise Exception("invalid file, too many components in first line")

        git = parts[0].strip()
        version = "master"
        if len(parts) > 1:
            version = parts[1].strip()

        patch = fd.read()
        return git, version, patch


def o(folder, cmd):
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, cwd=folder)
    proc.wait()
    return proc.stdout.read().decode("utf-8").strip(), proc.returncode


def folder_status(folder, git, commit, path):
    if not os.path.isdir(os.path.join(folder, ".git")):
        return "not a git repo."

    cgit, code = o(folder, "git config --get remote.origin.url")
    if code != 0:
        return "failed get git url (%s)" % cgit

    if git != cgit:
        return "found %s." % cgit

    version, code = o(folder, "git rev-parse HEAD")
    if code != 0:
        return "failed to get git version (%s)" % version

    if commit != "master" and version != commit:
        return "found %s@%s." % (cgit, version)

    return "Upto date."


def file_status(pwd, name, dirs):
    fullname = os.path.join(pwd, name)
    base = name[:-5]
    fbase = os.path.join(pwd, base)
    rel = os.path.relpath(fbase)

    try:
        git, commit, patch = parse(fullname)
    except Exception as e:
        return rel, str(e)

    if base not in dirs:
        return rel, "folder does not exist.", git, commit

    return rel, folder_status(fbase, git, commit, patch), git, commit


def handle_list(root):
    output = []
    for pwd, dirs, files in os.walk(root, followlinks=True):
        for f in files:
            if not f.endswith(".gsub"):
                continue
            output.append(file_status(pwd, f, dirs))

    if not output:
        print("No .gsub files found in %s." % root)
        return

    maxsize = max(len(x[0]) for x in output)+1
    for x in output:
        print(("%-" + str(maxsize) + "s   %s") % (x[0] + ":", x[1]))
        print(("%-" + str(maxsize) + "s   Expected: %s@%s.") % ("", x[2], x[3][:10]))


def update_it(folder, name):
    fullname = os.path.join(folder, name)
    base = name[:-5]
    fbase = os.path.join(folder, base)
    rel = os.path.relpath(fbase)

    try:
        git, commit, patch = parse(fullname)
    except Exception as e:
        return rel, str(e)

    if os.path.isdir(fbase) and not os.path.isdir(os.path.join(fbase, ".git")):
        print("%s is not a git folder. What to do?" % fbase)
        if six.moves.input("Nuke %s? [y/N]: " % fbase).lower() == "y":
            try:
                shutil.rmtree(fbase)
            except Exception as e:
                return rel, "Error: failed to remove (%s)." % e
        else:
            return rel, "Not upto date."

    if os.path.isdir(os.path.join(folder, base)):
        cgit, code = o(fbase, "git config --get remote.origin.url")
        if code != 0:
            return "Error: failed to git url (%s)." % cgit

        if cgit != git:
            print(
                "%s contains %s, expected %s, what to do?" % (rel, cgit, git)
            )
            if six.moves.input("Nuke %s [y/N]: " % fbase).lower() == "y":
                try:
                    shutil.rmtree(fbase)
                except Exception as e:
                    return rel, "Error: failed to remove (%s)." % e
            else:
                return rel, "Not upto date."

    cloned = False
    if not os.path.isdir(os.path.join(folder, base)):
        err, code = o(folder, "git clone %s %s" % (git, base))
        if code != 0:
            return rel, "Error: could not clone (%s)." % err
        cloned = True

    if commit == "master":
        if cloned:
            return rel, "Cloned %s @master." % git
        else:
            return rel, "Up to date."

    version, code = o(fbase, "git rev-parse HEAD")
    if code != 0:
        return "Error: failed to get git version (%s)." % version

    if version == commit:
        if cloned:
            return rel, "Cloned %s @%s." % (git, version)
        else:
            return rel, "Up to date."

    if cloned:
        err, code = o(fbase, "git checkout %s" % commit)
        if code != 0:
            return rel, "Error: could not checkout (%s)." % err.strip()
        return rel, "Cloned %s @%s, latest was %s." % (git, commit, version)

    print(
        "%s contains version %s, expected %s, what to do?" % (
            rel, version, commit
        )
    )

    if six.moves.input("Checkout %s [y/N]: " % commit).lower() == "y":
        err, code = o(fbase, "git fetch")
        if code != 0:
            return rel, "Error: could not fetch (%s)." % err.strip()

        err, code = o(fbase, "git checkout %s" % commit)
        if code != 0:
            return rel, "Error: could not checkout (%s)." % err.strip()

        return rel, "Checked out."
    else:
        return rel, "Not up to date."


def handle_update(root):
    output = []
    for pwd, dirs, files in os.walk(root, followlinks=True):
        for f in files:
            if not f.endswith(".gsub"):
                continue
            output.append(update_it(pwd, f))

    if not output:
        print("No .gsub files found in %s." % root)
        return

    maxsize = max(len(x[0]) for x in output) + 1
    for x in output:
        print(("%-" + str(maxsize) + "s  %s") % (x[0] + ":", x[1]))


def handle_vendor(pth):
    pth = pth.rstrip("/")

    dst = ("vendor/src/%s" % pth)
    print("mkdir -p", dst)
    dstdad = dst.rsplit("/", 1)[0]

    giturl = "https://%s.git" % pth
    gclone = "git clone %s" % giturl
    print(dstdad, pth, giturl, gclone)

    if not os.path.isdir("./vendor/src/"):
        print(
            "There is no vendor folder in this directory. "
            "Do I create it? (y/N) "
        )

        if six.moves.input().lower() != "y":
            sys.exit(1)

    if not os.path.exists(dst):
        try:
            os.makedirs(dst)
        except OSError as e:
            print(e)
            sys.exit(1)

    git, code = o(dstdad, gclone)
    if code != 0:
        print(git)
        sys.exit(code)

    commit, code = o(dst, "git rev-parse HEAD")
    if code != 0:
        print(commit)
        sys.exit(code)

    commit = commit.strip()

    try:
        open(dst + ".gsub", "w").write("%s %s\n" % (giturl, commit))
    except IOError as e:
        print(e)
        sys.exit(1)

    o(".", "git add " + dst + ".gsub -f")

    try:
        open(".gitignore", "a+").write(dst + "/\n")
    except IOError as e:
        print(e)
        sys.exit(1)


def main():
    if len(sys.argv) == 1:
        show_help()

    first = sys.argv[1]
    if first == "--help":
        show_help()

    if first == "--version":
        show_version()

    root = locate_git()
    if not root:
        print("not a git repo")
        return

    if first == "list":
        handle_list(root)

    if first == "update":
        handle_update(root)

    if first == "vendor":
        print(sys.argv)
        if len(sys.argv) != 3:
            show_help()
        second = sys.argv[2].replace("https://", "")
        handle_vendor(second)

if __name__ == '__main__':
    main()
