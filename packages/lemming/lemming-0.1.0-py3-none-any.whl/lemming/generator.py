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

import datetime
import os
import pkg_resources
import pathlib
import sys

from jinja2 import Environment, FileSystemLoader

from lemming import config

class ConfigBuilder(object):

    def __init__(self, license):
        self.license = str(license)

    def mkfile(self):
        base_path = pkg_resources.resource_filename(__name__, "templates/config")
        env = Environment(loader=FileSystemLoader(base_path))

        directory = os.fsencode(str(base_path))
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            template = env.get_template(filename)
            newfname = filename.rstrip(".j2")

            print(self.license)
            with open(os.path.join(os.path.expanduser('~'), '.lemming.yml'), "w") as f:
                try:
                    f.write(template.render(license=self.license))
                except Exception:
                    print(newfname)
                    raise

class ProjectBuilder(object):

    def __init__(self, name, **kwargs):
        self.config = config.read_config()
        self.name = name
        self.testdir = 'tests'
        self.author = self.config['lemming']['author']
        self.email = self.config['lemming']['author_email']
        self.license = str(kwargs['license'])

        self.year = datetime.datetime.now().strftime('%Y')

    def mktree(self):
        print("Creating project {0} using the {1} license.".format(self.name, self.license))
        pathlib.Path("{0}/{1}".format(self.name, self.name)).mkdir(parents=True, exist_ok=True)
        pathlib.Path("{0}/{1}".format(self.name, self.testdir)).mkdir(parents=True, exist_ok=True)

    def mkfiles(self):
        templdirs = ['modfiles', 'rootfiles', 'testfiles']

        for tpldir in templdirs:
            base_path = pkg_resources.resource_filename(__name__, "templates/{0}".format(tpldir))
            env = Environment(loader=FileSystemLoader(base_path))

            if tpldir is 'modfiles':
                savepath = "{0}/{1}".format(self.name, self.name)

            if tpldir is 'rootfiles':
                savepath = "{0}".format(self.name)

            if tpldir is 'testfiles':
                savepath = "{0}/{1}".format(self.name, self.testdir)

            directory = os.fsencode(str(base_path))
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                template = env.get_template(filename)
                newfname = filename.rstrip(".j2")

                if 'dot' in newfname:
                    newfname = newfname.lstrip("dot")

                with open("{0}/{1}".format(savepath, newfname), "w") as f:
                    try:
                        # sorry purists...
                        f.write(template.render(name=self.name, year=self.year, author=self.author, email=self.email, license=self.license))
                    except Exception:
                        print(newfname)
                        raise

    def mklicense(self):
        valid_licenses = ['apache', 'bsd', 'mit']
        apache, bsd, mit = valid_licenses

        if self.license.lower() not in valid_licenses:
            print("Please choose a valid license: {0}, {1} or {2}".format(apache, bsd, mit))
            sys.exit(0)

        tpldir = 'licenses'

        base_path = pkg_resources.resource_filename(__name__, "templates/{0}".format(tpldir))
        env = Environment(loader=FileSystemLoader(base_path))

        if tpldir is 'licenses':
            savepath = "{0}".format(self.name)

        directory = os.fsencode(str(base_path))

        filename = os.fsdecode("{0}-LICENSE.j2".format(str(self.license).upper()))
        template = env.get_template(filename)
        newfname = filename.lstrip("{0}-".format(str(self.license).upper())).rstrip(".j2")
        newfname = "{0}".format(newfname)

        with open("{0}/{1}".format(savepath, newfname), "w") as f:
            try:
                # sorry purists...
                f.write(template.render(name=self.name, year=self.year, author=self.author, email=self.email, license=self.license))
            except Exception:
                print(newfname)
                raise
