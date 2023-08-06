"""Error distribution functions"""

# import
## batteries
import sys
from functools import partial
## 3rd party
import numpy as np
import pandas as pd
import scipy.stats as st
from pathos.multiprocessing import ProcessingPool
## application
from OTU_Table import OTU_table
import QSIPCython as SSC
import Utils

def _prop_abund(x):
    """Calculate proportional absolute abundances.
    x = row in OTU dataframe
    """
    # does 'prop_abs_abund' column exist?
    try:
        x = x['prop_abs_abund']
    except KeyError:
        msg = '"prop_abs_abund" column not found!' + \
              ' Check out the `qPCR` subcommand.'
        sys.exit(msg)
    # dividing by total abundance; if div by zero, return zero 
    if np.sum(x) == 0:
        y = (x / np.nan).fillna(0)
    else:
        y = (x / float(np.sum(x))).fillna(0)
    # ret
    return y

def calc_prop_abs_abund(otu, groups):
    """Calculate the proporitonal absolute abundance (see Hungate et al., 2015)
    for each group specified by `groups`. 
    Prop_abs_abund = taxon copy number per sample as a fraction of total 
    copies for the taxon.
    
    Parameters
    ----------
    otu : OTU_Table.OTU_table object
    groups : list-like
        Groupings for applying taxon_abundance / total_abundance
    """
    otu.apply_by_group(_prop_abund, 'prop_abs_abund_frac', groups=groups)

def _calc_wAve_density(x):
    """Calculate weighted avareage density.
    x : row in OTU table dataframe
    """
    rel_abunds = x['prop_abs_abund_frac']
    BD = x['BD_mid']
    if np.sum(rel_abunds) <= 0:
        return np.nan
    else:
        return np.average(BD, weights=rel_abunds)

def calc_wAverage_density(otu, groups):
    """Calculated the weighted average density (W_ij), where weights are 
    defined by taxon proportional absolute abundance.
    
    Parameters
    ----------
    otu : OTU_Table.OTU_table object
    groups : list-like
        Groupings for applying taxon_abundance / total_abundance
    """
    return otu.apply_by_group(_calc_wAve_density, 'density', 
                              groups=groups, inplace=False)

def calc_mean_density(densities, exp_design=None):
    """Calculate mean densities (W_LIGHTi & W_LABi) for control/treatment 
    libraries.

    Parameters
    ----------
    densities : pandas.DataFrame
        output of calc_wAverage_density
    exp_design : pandas.DataFrame
        2-column dataframe (library, sample_type), 
          where sample_type = 'control' or 'treatment'
    """
    # calculating means of W for control/treatment
    ## join densities with exp_design
    if exp_design is not None:
        densities['library'] = densities['library'].astype(str)
        exp_design['library'] = exp_design['library'].astype(str)
        densities = pd.merge(densities, exp_design, how='inner', on='library')
    ## groupby, then apply (mean)
    groups = ['taxon', 'sample_type']
    f = lambda x : np.mean(x['density'])
    mean_densities = densities.groupby(groups).apply(f).reset_index()
    ncol = len(mean_densities.columns)
    mean_densities.columns = mean_densities.columns[:ncol-1].tolist() + \
                             ['mean_density']

    # wide to long table format
    mean_densities = mean_densities.pivot('taxon', 
                                          'sample_type', 
                                          'mean_density').reset_index()
    if mean_densities.shape[1] != 3:
        print mean_densities
        assert mean_densities.shape[1] == 3
    mean_densities.columns = ['taxon', 'control', 'treatment']
    return mean_densities


def atomFracExcess(df, isotope='13C'):
    """Calculate atom fraction excess.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe of weighted mean densities averaged across gradients.
    isotope : string
        Which isotope to calculate?
    """
    ## control GC
    df['control_GC'] = SSC.BD2GC(df['control'].values)

    ## control molecular weight    
    df['control_MW'] = SSC.GC2M_light(df['control_GC'].values)
        
    ## max heavy molecular weight
    df['treatment_max_MW'] = SSC.M_light2heavyMax(df['control_MW'].values)
    
    ## molecular weight of labeled DNA
    df['treatment_MW'] = SSC.calc_M_lab(df['BD_diff'].values,
                                        df['control'].values,
                                        df['control_MW'].values)
        
    ## % atom excess
    df['atom_fraction_excess'] = SSC.atomFracExcess(df['treatment_MW'].values,
                                                    df['control_MW'].values,
                                                    df['treatment_max_MW'].values,
                                                    isotope=isotope)


def subsample_densities(df, sample_type):
    """Subsampling buoyant density values for bootstrapping. 
    (e.g., shuffling samplings). Subsampling with replacment from
    density values of `sample_type`.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame that contains 'sample_type'  (values: control or treatment)
    sample_type : string
        Which sample type (control|treatment) to sub-sample for.
    """
    idx = df.loc[df['sample_type'] == sample_type].index.tolist()
    subsamps = np.random.choice(idx, len(idx), replace=True)
    x = df.loc[subsamps,:].reset_index()
    x['sample_type'] = sample_type
    return x


def _bootstrap(df, isotope):
    """Subsampling with replacement
    """
    # checking for NAs in densities; if so, returning NA
    if pd.isnull(df['density']).any():
        return np.nan

    # subsample with replacement
    ## control
    idx = df['sample_type'] == 'control'
    df_cont = subsample_densities(df, 'control')
    ## treatment
    idx = df['sample_type'] == 'treatment'
    df_treat = subsample_densities(df, 'treatment')
    ## cat
    df_i = pd.concat([df_cont, df_treat])
    
    # calculate weighted-mean density (wmd)
    df_i_wmd = calc_mean_density(df_i)
    
    # calculating density shifts 
    df_i_wmd['BD_diff'] = SSC.calc_density_shift(df_i_wmd['treatment'].values,
                                                 df_i_wmd['control'].values)
    
    # calculating atom fraction excess 
    atomFracExcess(df_i_wmd, isotope=isotope)
    
    # return
    return df_i_wmd.loc[0,'atom_fraction_excess']


def _bootstrap_CI(df, n=1000, a=0.1, isotope='13C', pool=None, name=None):
    # status
    taxon = df['taxon'].unique()[0]
    msg = 'Bootstrap CI (n={}), processing taxon: {}\n'
    sys.stderr.write(msg.format(n, taxon))

    # bootstrapping (in parallel)
    if pool is None:        
        boot_afx = [_bootstrap(df, isotope) for i in xrange(n)]
    else:
        dfs = [df for i in xrange(n)]
        _bootstrap_p = partial(_bootstrap, isotope=isotope)
        boot_afx = pool.map(_bootstrap_p, dfs)

    # returning CI of nan if atom_fraction_excess is nan
    msg = 'WARNING! "{}" --> NAs in bootstrap values.' \
          ' CI values set to nan.' \
          ' This is probably due to a very low abundance in >=1 library.\n'
    if np.isnan(boot_afx).any():
        sys.stderr.write(msg.format(taxon))
        if name is not None:
            return pd.Series({'taxon':name, 'atom_CI_low':np.nan, 
                             'atom_CI_high':np.nan})
        else:
            return pd.Series({'atom_CI_low':np.nan, 'atom_CI_high':np.nan})
        
    # calculating CIs
    CI_low = np.percentile(boot_afx, a / 2.0 * 100)
    CI_high = np.percentile(boot_afx, (1 - a / 2.0) * 100)
    assert CI_low <= CI_high, 'CI_low is > CI_high'

    # formating & returning
    if name is not None:
        ret = pd.Series({'taxon':name, 'atom_CI_low':CI_low, 
                         'atom_CI_high':CI_high})
    else:
        ret = pd.Series({'atom_CI_low' : CI_low, 'atom_CI_high' : CI_high})

    return ret


def bootstrap_CI(densities, mean_densities, exp_design,
                 n=1000, a=0.1, isotope='13C', nodes=1, byBoot=False):
    """Calculate qSIP bootstraped confidence intervals.
    Reference: Hungate et al., 2015.

    Parameters
    ----------
    densities : pandas.DataFrame
        Table of all weighted mean densities for each library-taxon.
    mean_densities : pandas.DataFrame
        Table of library-averaged densities for each taxon.
    exp_design : pandas.DataFrame
        Table with 'library' and 'sample_type' columns (control|treatment)
    n : int
        Number of bootstrap replicates
    a : float
        Alpha for confidence interval calculation
    isotope : str
        Which isotope to calculate atom fraction excess?
    nodes : int
        Number of parallel processes.    
    """    
    # multiprocessing
    if nodes is None:
        pool = None
    else:
        pool = ProcessingPool(nodes=nodes)

    # add: mean_densities
    cols = ['taxon', 'BD_diff', 'atom_fraction_excess']
    densities = densities.merge(mean_densities[cols], on=['taxon'], how='inner')
    # add: experimental design
    densities = densities.merge(exp_design, on=['library'], how='inner')

    # calculate CI: parallel by taxon
    if byBoot:
        func = lambda x : _bootstrap_CI(x, n=n, a=a, isotope=isotope, pool=pool)
        CIs = densities.groupby(['taxon']).apply(func).reset_index()
    else:
        func = lambda x : _bootstrap_CI(x[1], n=n, a=a, isotope=isotope, 
                                        pool=None, name=x[0])
        if pool is None:        
            CIs = map(func, [(name,group) for name,group 
                             in densities.groupby(['taxon'])])
        else:
            CIs = pool.map(func, [(name,group) for name,group 
                                  in densities.groupby(['taxon'])])
        CIs = pd.DataFrame(CIs)

    cols = ['taxon', 'atom_CI_low', 'atom_CI_high']
    return CIs[cols]


def qSIP_atomExcess(Uargs):
    """Main function for calculating atom fraction excess (and density shift)
    for qSIP data (OTU table where relative abundances were multipled by qPCR
    values (total gene copies) to get proportinoal absolute abundances).

    Parameters
    ----------
    Uargs : dict
        See qSIP_atomExcess.py
    """    
    # loading tables
    sys.stderr.write('Loading files...\n')
    ## experimental design
    exp_design = Utils.load_exp_design(Uargs['<exp_design>'])
        
    ## OTU table 
    otu = OTU_table.from_csv(Uargs['<OTU_table>'], sep='\t')
    
    #-- calculating BD shift (Z) --#
    sys.stderr.write('Calculating density shifts (Z)...\n')
    # getting proportional absolute abundancs for each taxon
    groups = ('library', 'taxon',)
    calc_prop_abs_abund(otu, groups)
    
    # calculated weighted average BD (W_ij)        
    densities = calc_wAverage_density(otu, groups)
    
    # calculating means of W for control/treatment
    mean_densities = calc_mean_density(densities, exp_design)

    # calculating density shifts 
    mean_densities['BD_diff'] = SSC.calc_density_shift(mean_densities['treatment'].values,
                                                       mean_densities['control'].values)

    #-- calculating atom fraction excess --#
    sys.stderr.write('Calculating atom fraction excess (A)...\n')
    atomFracExcess(mean_densities, isotope=Uargs['-i'])

    #-- calculating CIs --#
    sys.stderr.write('Calculating bootstrap CIs...\n')
    if Uargs['--debug']:
        taxa = mean_densities['taxon'].tolist()
        densities = densities.loc[densities['taxon'].isin(taxa[:20])]
        Uargs['--np'] = None
    else:
        Uargs['--np'] = int(Uargs['--np'])
    CIs = bootstrap_CI(densities, mean_densities, exp_design, 
                       n=int(Uargs['-n']), 
                       a=float(Uargs['-a']), 
                       nodes=Uargs['--np'],
                       isotope=Uargs['-i'], 
                       byBoot=Uargs['--byBoot'])
    mean_densities = mean_densities.merge(CIs, on=['taxon'], how='inner')
    
    # return
    return mean_densities
