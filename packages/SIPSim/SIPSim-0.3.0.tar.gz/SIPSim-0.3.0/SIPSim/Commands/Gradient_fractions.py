#!/usr/bin/env python

"""
gradient_fractions: Simulate the fraction produced during gradient fractionation

Usage:
  gradient_fractions [options] <comm_file>
  gradient_fractions -h | --help
  gradient_fractions --version

Options:
  <comm_file>       Name of file produced by gradientComms subcommand.
  --dist=<d>        Distribution used to select gradient sizes.
                    [default: normal]
  --params=<p>      Params passed to distribution 
                    (see pymix.mixture for distribution params).
                    [default: mu:0.004,sigma:0.0015]
  --BD_min=<x>      Minimum BD of any fraction. [default: 1.66]
  --BD_max=<y>      Maximum BD of any fraction. [default: 1.78]
  --frac_min=<m>    Minimum fraction size. [default: 0.001]
  -h --help         Show this screen.
  --version         Show version.
  --debug           Debug mode

Description:
  Simulate the gradient fractionation for each library as specified in the
  community file (created with the gradientComm subcommand).
  Specifically, the sizes (in bouyant density) of each gradient fraction
  is simulated. Assuming 1 isopycnic gradient per library (sample).

  The fraction size range and variance is selected from a user-defined
  distribution.
"""

# import
## batteries
from docopt import docopt
import os, sys
import re

## application libraries
from SIPSim.Fractions import Fractions
from SIPSim.CommTable import CommTable


def main(Uargs):    
    # load comm file
    comm = CommTable.from_csv(Uargs['<comm_file>'], sep='\t')

    # parse param string
    l = re.split('[:,]', Uargs['--params'])
    params = {k.lower():float(v) for k,v in zip(l[0::2],l[1::2])}

    # initialize fraction
    fracs = Fractions(Uargs['--dist'], params,
                      Uargs['--BD_min'], Uargs['--BD_max'],
                      Uargs['--frac_min'])

    
    # simulate gradients for each library
    libFracs = [[libID,fracs.simFractions(libID)] for libID in comm.iter_libraries()]
    
    # writing output
    ## header: libraryID, fractionID, BD_min, BD_max
    print '\t'.join(['library','fraction','BD_min','BD_max','fraction_size'])
    ## body
    for lib in libFracs:
        libID = str(lib[0])
        frac_cnt = 0
        for frac in lib[1]:
            frac_cnt += 1
            frac_str = [str(round(x, 3)) for x in frac]
            print '\t'.join([libID, str(frac_cnt)] + frac_str)
    
    
def opt_parse(args=None):
    if args is None:        
        args = docopt(__doc__, version='0.1')
    else:
        args = docopt(__doc__, version='0.1', argv=args)
    main(args)

        
