"""
BD_shift: Determine the shift in BD based on KDE overlap

Usage:
  BD_shift [options] <kde1> <kde2>
  BD_shift -h | --help
  BD_shift --version

Options:
  <kde1>         KDE object
  <kde2>         KDE object 
  --start=<s>    Start of series for integration.
                 [default: 1.66]
  --end=<e>      End of series for integration.
                 [default: 1.85]
  --step=<x>     Step size of series for integration.
                 [default: 0.001]
  --np=<np>      Number of parallel processes.
                 [default: 1]
  --version      Show version.
  --debug        Debug mode (no parallel processes)
  -h --help      Show this screen.

Description:
  Determine the shift in BD value distribution between 2
  KDEs of BD values.
  The BD shift is calculated as 1 - KDE_intersection, 
  where KDE_intersection is calculated from 
  the integral of intersection densities at each point
  in the specified value series (start,end,step).
 
  Output
  ------
  A tab-delimited table of BD shift values is written to STDOUT.
 """

from docopt import docopt
from SIPSim import BD_Shift


def opt_parse(args=None):
    if args is None:        
        args = docopt(__doc__, version='0.1')
    else:
        args = docopt(__doc__, version='0.1', argv=args)
    BD_Shift.main(args)
          
