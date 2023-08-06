#!/usr/bin/env python

"""
KDE_sample: sample from each KDE and write a table of values

Usage:
  KDE_sample [options] <kde>
  KDE_sample -h | --help
  KDE_sample --version

Options:
  <kde>         Pickled KDE object
                ('-' if input from STDIN) 
  -n=<n>        Sample size.
                [Default: 10000]
  -h --help     Show this screen.
  --version     Show version.
  --debug       Debug mode

Description:
  Sample values from each KDE in the pickled KDE object
  and produce a table of values.

  Output
  ------
  Tab-delim file: <taxon><tab><value>
"""

# import
## batteries
from docopt import docopt
import sys,os
## 3rd party
import pandas as pd
## application libraries
from SIPSim import Utils
    


def to_df(x, libID):
    df = pd.DataFrame(x)
    df['libID'] = libID
    return df
    
def main(args=None):
    # input
    KDEs = Utils.load_kde(args['<kde>'])
    n = int(args['-n'])

    # KDE object type
    kde_type = Utils.KDE_type(KDEs)

    # sampling from KDEs
    vals = {}
    if kde_type == 1: 
        vals['1'] = {taxon:kde.resample(n)[0,] for taxon,kde in KDEs \
                if kde is not None}
    elif kde_type == 2:
        vals['1'] = {taxon:kde.resample(n)[0,] for taxon,kde in KDEs.items() \
                if kde is not None}
    elif kde_type == 3:
        for x,y in KDEs.items():
            vals[x] = {taxon:kde.resample(n)[0,] for taxon,kde in y.items() \
                       if kde is not None}
    elif kde_type == 4:
        for libID,filename in KDEs.items(): 
            KDE_bylib = Utils.load_kde(filename)
            vals[libID] = {taxon:kde.resample(n)[0,] for 
                           taxon,kde in KDE_bylib.items() if kde is not None}
    else:
        raise TypeError, 'KDE object type not recognized'

    # writing out results
    tbl = pd.concat([to_df(y,x) for x,y in vals.items()])
    tbl.to_csv(sys.stdout, sep='\t', index=False)

    
def opt_parse(args=None):
    if args is None:        
        args = docopt(__doc__, version='0.1')
    else:
        args = docopt(__doc__, version='0.1', argv=args)
    main(args)
