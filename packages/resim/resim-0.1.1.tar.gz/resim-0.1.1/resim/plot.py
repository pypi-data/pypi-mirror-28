"""ReSim - Plotting Module

Visualize resim result.

Examples:
    Available functions:
        >>> snsplt_cells = resim.plot_cells(res)
        >>> snsplt_drug = resim.plot_drug(res)
        >>> snsplt_fht = resim.plot_fht(res)

    You may save the plots in png.
        >>> snsplt_cells.figure.savefig('resim_cells.png')
        >>> snsplt_drug.figure.savefig('resim_drug.png')
        >>> snsplt_fht.figure.savefig('resim_fht.png')

"""

#import warnings; warnings.simplefilter('ignore')
import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns

def plot_cells(res, subplot=False):
    """Plot cells

    Args:
        res (dict): dict return by .simulate().
        subplot (bool): Default is False. True to plot different type of cells
        in different plot.

    Returns:
        seaborn plot object

    """
    tdf = res['case']['cells']
    mdf = pd.melt(tdf, id_vars=['days', 'n'])
    mdf.columns = ['days', 'n', 'type', 'number of cells']

    if subplot is False:
        tplt = sns.tsplot(data=mdf, time='days', condition='type', value='number of cells', unit='n', ci='sd')
    else:
        tplt = sns.FacetGrid(mdf, row='type')
        tplt = tplt.map_dataframe(sns.tsplot, data=mdf, time='days', condition='type', value='number of cells', unit='n', err_style='unit_traces', err_palette='husl')

    return tplt

def plot_drug(res):
    """Plot Drug Dynamics

    Args:
        res (dict): dict return by .simulate().

    Returns:
        seaborn plot object

    """
    tdf = res['case']['drugs']

    tplt = sns.tsplot(data=tdf, time='days', value='drug conc', unit='n', err_style='unit_traces', err_palette='husl')

    return tplt

def plot_fht(res):
    """Plot first hitting time (progression free survival)

    Args:
        res (dict): dict return by .simulate().

    Returns:
        seaborn plot object

    """
    tdf1 = pd.DataFrame(res['control']['fht'])
    tdf1.columns = ['progression time']
    tdf2 = pd.DataFrame(res['case']['fht'])
    tdf2.columns = ['progression time']

    tdf1anno = 'w/o treatment mean = ' + str(round(tdf1.mean()[0], 1)) + u' \xb1 ' +  str(round(tdf1.std()[0], 1)) + ' days'
    tdf2anno = 'treatment mean = ' + str(round(tdf2.mean()[0], 1)) + u' \xb1 ' +  str(round(tdf2.std()[0], 1)) + ' days'
    anno = tdf1anno + '\n' + tdf2anno

    fig, ax = plt.subplots()
    sns.distplot(tdf1, kde=False, fit=norm, ax=ax, axlabel='days', fit_kws={'color':'b', 'label':'w/o treatment'})
    sns.distplot(tdf2, kde=False, fit=norm, ax=ax, fit_kws={'color':'r', 'label':'treatment'})
    ax.text(1, 0.99, tdf1anno, horizontalalignment='right', verticalalignment='top', transform=ax.transAxes, color='b')
    ax.text(1, 0.92, tdf2anno, horizontalalignment='right', verticalalignment='top', transform=ax.transAxes, color='r')

    return tplt
