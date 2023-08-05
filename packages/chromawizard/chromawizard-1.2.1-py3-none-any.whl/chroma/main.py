#! /usr/bin/env python3
# encoding: utf-8
"""
ChromaWizard -- an application to create karyotype images from M-FISH chromosome painting images

@author:     Norbert Auer
        
@copyright:  2016 ACIB GmbH, Vienna. All rights reserved.

@license:    GPL 3.0

@contact:    norbert.auer@boku.ac.at
"""

import sys
import os
import logging

from PyQt5.QtCore import QLocale
from argparse import ArgumentParser, RawDescriptionHelpFormatter, Action,  ArgumentTypeError

from chroma.Manager import Manager
import chroma.Settings as S

LogLevels = ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

def required_length(nmin,nmax):
    class RequiredLength(Action):
        def __call__(self, parser, args, values, option_string=None):
            if not nmin <= len(values) <= nmax:
                msg = 'argument "{}" requires between {} and {} arguments'.format(self.dest, nmin, nmax)
                raise ArgumentTypeError(msg)
            setattr(args, self.dest, values)
    return RequiredLength


def start(args):
    args.logger.debug("Start ChromaWizard")
    args.logger.info("Current Local: {}".format(QLocale().name()))

    # Initiate Manager Class
    m = Manager(args)

    # Run Gui-App
    return m.run()


def main(argv=None):
    """ Command line options """

    if argv is None:
        argv = sys.argv[1:]
    else:
        sys.argv.extend(argv)    

    program_name = os.path.basename(sys.argv[0])
    program_version = "v{}".format(S.__version__)
    program_build_date = str(S.__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __doc__.split("\n")[1]
    program_license = '''%s

  Created by Norbert Auer on %s.
  Copyright 2017 ACIB GmbH, Vienna. All rights reserved.

  Licensed under the GPL 3.0
  https://www.gnu.org/licenses/gpl-3.0.html

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(S.__date__))
    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument('-q', '--quiet', action='store_true', help="Turn off log")
        parser.add_argument('-l', '--log', choices=LogLevels, type=str, default='WARN', help="Set the log level")
        parser.add_argument('-b', '--batch', action='store_true', help="Run in batch mode without gui. Is not implemented yet")
        #parser.add_argument('-i', '--input', help="For each channel one filename. First file is DAPI", type=str,
        #                    nargs='+', action=required_length(1, CHANNEL_NR))
        parser.add_argument('-c', '--config', nargs='?', type=str,
                            default=os.path.expanduser('~/.c.default.conf.json'),
                            help="Path to config file [default]='~/.c.default.conf.json'")

        # Process arguments
        args = parser.parse_args()

        if args.quiet:
            args.log = LogLevels['NOTSET'].value

        # Create logger
        args.logger = logging.getLogger('ChromaWizard')

        # Set logger level
        args.logger.setLevel(args.log)

        # Create console handler and set level to debug
        log = logging.StreamHandler()

        # Create formatter
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')

        # Add formatter to ch
        log.setFormatter(formatter)

        # Add ch to logger
        args.logger.addHandler(log)

        args.logger.debug("Argparse args: {}".format(args))

        return start(args)
    except KeyboardInterrupt:
        ### Handle keyboard interrupt ###
        return 0
    except Exception as e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        raise e

if __name__ == "__main__":
    sys.exit(main())
