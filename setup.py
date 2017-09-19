#! /usr/bin/env python3
# encoding: utf-8
'''
Wrapper to install Acpera with Terraform on AWS.

@author:     Andrey N. Petrov
@license:    Apache License 2.0
@contact:    andreynpetrov@gmail.com
'''

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from configparser import ConfigParser
from itertools import chain
import json
import os
import platform
import shutil
import sys
import time

import subprocess as sp


__all__ = []
__version__ = 0.1
__date__ = '2017-04-22'
__updated__ = '2017-04-22'

DEBUG = 0
TESTRUN = 0
PROFILE = 0


class Terraform():
    def __init__(self, args):
        self.args = args
      
    @property
    def aws(self):
        """terraform apply"""
        print("Terraform apply aws")
        sp.call([self.args.terraform_path, "init"])
        sp.call([self.args.terraform_path, "get"])
        sp.call([self.args.terraform_path, "validate"])
        sp.call([self.args.terraform_path, "plan", "-target=module.aws"])
        sp.call([self.args.terraform_path, "apply", "-target=module.aws"])
        sp.call([self.args.terraform_path, "refresh"])
    
    @property
    def destroy_aws(self):
        """terraform destroy"""
        print("Terraform destroy aws")
        sp.call([self.args.terraform_path, "init"])
        sp.call([self.args.terraform_path, "get"])
        sp.call([self.args.terraform_path, "validate"])
        sp.call([self.args.terraform_path, "plan", "-destroy", "-target=module.aws"])
        sp.call([self.args.terraform_path, "destroy", "-target=module.aws"])
    
    
class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg


def is_os_64bit():
    return platform.machine().endswith('64')


def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Andrey N. Petrov on %s.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument('-d', '--domain', help='domain name', default='netanza.com')
        parser.add_argument("action", help="aws|destroy_aws")

        # Process arguments
        args = parser.parse_args()
        action = args.action
          
        if os.name == "posix":
            args.terraform_path = os.path.join("contrib", "terraform-linux", "terraform")
        elif is_os_64bit():
            args.terraform_path = os.path.join("contrib", "terraform-win64", "terraform.exe")
        else:
            args.terraform_path = os.path.join("contrib", "terraform-win32", "terraform.exe")

        t = Terraform(args)
                        
        if action == "aws":
            t.aws
        elif action == "destroy_aws":
            t.destroy_aws
        else:
            print("Unknown action")

        return 0
    
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
        sys.argv.append("-r")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = '_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
