# Copyright (c) 2018, Mayo Clinic
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#     Neither the name of the Mayo Clinic nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
import re
from argparse import Namespace
import shlex
from typing import List, Optional

import sys

import os
from fhirtordf.rdfsupport.namespaces import FHIR

from i2fhirb2 import __version__
from i2fhirb2.fhir.fhirspecific import DEFAULT_FMV, DEFAULT_PROVIDER_ID
from i2fhirb2.generate_i2b2 import Default_Sourcesystem_Code, Default_Path_Base
from i2fhirb2.sqlsupport.dbconnection import FileAwareParser, add_connection_args

defaults = {
            # "base": Default_Path_Base,
            # "uribase": str(FHIR),
            # "providerid": DEFAULT_PROVIDER_ID,
            # "sourcesystem": Default_Sourcesystem_Code,
            # "onttable": "custom_meta"
    }

meta_parameters = ["file", "show", "create", "createorrep"]


def print_conf_file(opts: Namespace) -> Optional[str]:
    """ Print the config file contents

    :param opts: Options carrying file name
    :return: None if success otherwise error message
    """
    with open(opts.file) as f:
        args = shlex.split(f.read())
    parser = create_parser(use_defaults=False)
    opts = parser.parse_args(args)
    for k, v in opts.__dict__.items():
        if v is not None and defaults.get(k) != v:
            print(f"{k}:\t\t{v}")
    return None


def create_conf_file(opts: Namespace) -> Optional[str]:
    """ Create the configuration file

    :param opts: Creation options
    :return: Error message if problems, otherwise None
    """
    if not opts.createorrep:
        if os.path.exists(opts.file):
            return f"{opts.file} already exists!"
    with open(opts.file, 'w') as f:
        for k, v in opts.__dict__.items():
            if k not in meta_parameters and v is not None and defaults.get(k) != v:
                f.write(f"--{k} {esc(v)}\n")
    return None


def esc(arg: str) -> str:
    """ Escape arg in a way that the shlex (argv) processor keeps it whole

    :param arg: argument to escape
    :return: What to write in the file
    """
    arg = re.sub(r'\\', r'\\\\', str(arg))
    return f'"{arg}"' if re.search(r'\s', arg) else arg

def add_meta_args(parser: FileAwareParser) -> None:
    """ dd the control (meta) arguments to the parser

    :param parser: Parser to add arguments to
    """
    parser.add_argument("-v", "--version", help="Show software version number and exit", action="version",
                        version=f'Version: {__version__}')
    parser.add_argument("-f", "--file", help="Configuration file", default="db_conf")
    parser.add_argument("-s", "--show", help="Display current configuration", action="store_true")
    parser.add_argument("-c", "--create", help="Create new configuration file if not exists", action="store_true")
    parser.add_argument("-c!", "--createorrep", help="Create or replace configuration file ", action="store_true")


def create_parser(use_defaults: bool = True) -> FileAwareParser:
    """
    Create a command line argument parser

    :param use_defaults: Add defaults
    :return: parser
    """
    parser = FileAwareParser(description="Create configuration file for i2FHIRb2 software", prog="conf_file",
                             use_defaults=use_defaults)
    parser.add_file_argument("-mv", "--metadatavoc", help="Location of FHIR Metavocabulary file",
                             default=DEFAULT_FMV)
    parser.add_argument("-ss", "--sourcesystem", metavar="SOURCE SYSTEM CODE", default=Default_Sourcesystem_Code,
                        help="Sourcesystem code")
    parser.add_argument("-u", "--uploadid", metavar="UPLOAD IDENTIFIER",
                        help="Upload identifer -- uniquely identifies this batch", type=int)
    parser.add_argument("--base", metavar="CONCEPT IDENTIFIER BASE", default=Default_Path_Base,
                        help="Concept dimension and ontology base path")
    parser.add_argument("-ub", "--uribase", help="RESOURCE URI BASE", default=str(FHIR))
    parser.add_argument("-p", "--providerid", metavar="DEFAULT PROVIDER ID", help="Default provider id",
                        default=DEFAULT_PROVIDER_ID)
    return add_connection_args(parser)


def conf_file(argv: List[str]) -> bool:
    """
    Create and/or print a configuration file

    :param argv: Parameter list -- see create_parser for details
    :return: True if success - otherwise an exception is thrown
    """
    parser = create_parser()
    add_meta_args(parser)
    opts = parser.parse_args(argv)

    # Note that "help" and "version" exit immediately
    if not (opts.create or opts.createorrep or opts.show):
        parser.print_usage()
        return False

    rval = create_conf_file(opts) if opts.create or opts.createorrep else None

    if not rval and opts.show:
        rval = print_conf_file(opts)

    if rval:
        parser.error(rval)

    return True


if __name__ == "__main__":
    conf_file(sys.argv[1:])
