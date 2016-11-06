#!/usr/local/bin/python2.7
# encoding: utf-8
'''
main -- shortdesc

main is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2016 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import os


import mechanize
import cookielib


from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from smappee.smappee import Smappee
import traceback
import time
from energycounter import EnergyCounter
import domoticz.energy

__all__ = []
__version__ = 0.1
__date__ = '2016-11-05'
__updated__ = '2016-11-05'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

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

  Created by user_name on %s.
  Copyright 2016 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)

        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose

        if verbose > 0:
            print("Verbose mode on")
    
        sm = Smappee("192.168.7.20")
        sm.login_test()
        
        consumption_counter = EnergyCounter("Consumption")
        solar_counter = EnergyCounter("Solar")
        consumption = domoticz.energy.EnergyCounter(consumption_counter, 317, "192.168.7.2", 8080)
        solar = domoticz.energy.EnergyCounter(solar_counter, 318, "192.168.7.2", 8080)
        sm.set_counter("phase0ActivePower", consumption_counter)
        sm.set_counter("phase1ActivePower", solar_counter)
        
        print("Starting reader thread")
        sm.start_instantaneous_reader()
        print("Starting domoticz updater thread")
        consumption.start_update_thread()
        solar.start_update_thread()
        
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            traceback.print_exc()
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'main_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    main()