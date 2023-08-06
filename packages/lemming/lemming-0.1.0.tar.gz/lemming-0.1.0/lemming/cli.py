# MIT License
#
# Copyright (c) 2017 Paul Stevens
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import os
import sys

# from lemming import config
from lemming import generator

def main():
    # config = config.read_config()

    parser = argparse.ArgumentParser(description='Project skeleton generator')
    parser.add_argument('name', help='The desired project name')

    parser.add_argument('--license', default='MIT', help='MIT, Apache, BSD')

    args = parser.parse_args()

    if args.license:
        lsn = args.license

    if not args.license:
        lsn = 'MIT'

    if 'config' in args.name:
        print("Creating a config file at {0}".format(os.path.join(os.path.expanduser('~'), '.lemming.yml')))
        generator.ConfigBuilder(license=lsn).mkfile()
    else:
        print("Creating a project structure for {0}".format(args.name))
        build = generator.ProjectBuilder(args.name, license=lsn)

        # Make tree and install files
        build.mktree()
        build.mkfiles()
        build.mklicense()


if __name__ == "__main__":
    main()
