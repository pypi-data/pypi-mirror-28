"""ReSim GUI Plotting Module

Plot the simulation result, including progression free survival estimation and overall dynamics using plotly.

Example:
    fig_fht = plot_fht(res)
    fig_od = plot_overalldynamics(res)

Attributes:
    colorb (list): rgb codes of blue color.
    colorg (list): rgb codes of green color.
    coloro (list): rgb codes of orange color.
    colorp (list): rgb codes of purple color.
    colorr (list): rgb codes of red color.
    colors (list): list contains colorb, colorg, coloro, colorp, colorr.
    celltypes (list): list with all cell types available in resim model.

"""

import pandas as pd
import numpy as np
from plotly.graph_objs import Figure, Layout, Scatter
import plotly.figure_factory as ff
from plotly.plotly import iplot
#from plotly.offline import iplot, init_notebook_mode
#init_notebook_mode(connected=True)

#import resim_core as resim
#model = resim.simulator()
#res = model.simulate()

colorb = ['rgb(8,81,156)','rgb(49,130,189)','rgb(107,174,214)', 'rgb(189,215,231)']
colorg = ['rgb(0,109,44)','rgb(44,162,95)','rgb(102,194,164)', 'rgb(186,228,179)']
coloro = ['rgb(166,54,3)','rgb(230,85,13)','rgb(253,141,60)', 'rgb(253,190,133)']
colorp = ['rgb(84,39,143)','rgb(117,107,177)','rgb(158,154,200)', 'rgb(203,201,226)']
colorr = ['rgb(165,15,21)','rgb(222,45,38)','rgb(251,106,74)', 'rgb(252,174,145)']
colors = [colorb, colorg, coloro, colorp, colorr]

celltypes = ['sensitive', 'primary resistant', 'acquired resistant', 'quiescent', 'total']

def plot_fht(res):
    """plot first hitting time (progress time)

    Args:
        res: result from resim simulation simulate method (dict).

    Returns:
        plotly figure
    """
    controlfht = res['control']['fht']
    casefht = res['case']['fht']
    hist_data = [controlfht, casefht]

    controllabel = 'w/o treatment<br>' + str(round(np.mean(controlfht))) + u' \xb1 ' + str(round(np.std(controlfht))) + ' days'
    caselabel = 'treatment<br>' + str(round(np.mean(casefht))) + u' \xb1 ' + str(round(np.std(casefht))) + ' days'
    group_labels = [controllabel, caselabel]

    fig = ff.create_distplot(hist_data, group_labels, show_hist=False, curve_type='normal')
    fig['layout'].update(title='Simulated PFS Distribution', xaxis=dict(dtick=30, title='days'), legend=dict(orientation="h"))

    return fig

def plot_allN(res, celltype):
    """plot all n simulation result for a cell type

    Args:
        res: result from resim simulation simulate method (dict).
        celltype: string specify which cell type to plot.

    Returns:
        plotly figure
    """

    if celltype!='drug conc':
        df = res['case']['cells']
        tit = 'N Simulations - ' + celltype
        yaxtit = 'No. of cells (10<sup>8</sup>)'
    else:
        df = res['case']['drugs']
        tit = 'N Simulations - Drug Conc'
        yaxtit = 'Drug Conc.'
    #df = df.assign(days=pd.Series(np.tile(tspan, 1)))
    tspan = list(np.unique(df.days))

    traces = []
    for _, n in enumerate(np.unique(df.n)):
        tdf = list(df[df['n']==n][celltype])
        ttr = Scatter(x=tspan, y=tdf, opacity=0.8, showlegend=False, line=Line(width=0.5))
        traces.append(ttr)
    layout = Layout(title=tit, xaxis=dict(dtick=30, title='days'), yaxis=dict(title=yaxtit), hovermode = 'closest')
    fig = Figure(data=traces, layout=layout)

    return fig

def plot_overalldynamics(res, colorlist=colors, celltypelist=celltypes):
    """plot overall subpopulation dynamics with 90 & 95 CI

    Args:
        res: result from resim simulation simulate method (dict).
        colorlist: list with rgb code for plotting (list of lists).
        celltypelist: list specify which cell type to plot (list).

    Returns:
        plotly figure
    """
    df = res['case']['cells']
    #df = df.assign(days=pd.Series(np.tile(tspan, 1)))
    tspan = list(np.unique(df.days))

    mdf = pd.melt(df, id_vars=['days', 'n'])
    mdf.columns = ['days', 'n', 'type', 'number of cells']

    traces = []
    for i, n in enumerate(celltypelist):
        tmdf = mdf[mdf['type']== n]
        tmean = list(tmdf.groupby('days')['number of cells'].mean())
        tlower50 = list(tmdf.groupby('days')['number of cells'].quantile(0.25))
        tupper50 = list(tmdf.groupby('days')['number of cells'].quantile(0.75))
        tlower90 = list(tmdf.groupby('days')['number of cells'].quantile(0.05))
        tupper90 = list(tmdf.groupby('days')['number of cells'].quantile(0.95))
        tlower95 = list(tmdf.groupby('days')['number of cells'].quantile(0.025))
        tupper95 = list(tmdf.groupby('days')['number of cells'].quantile(0.975))
        ttr_m = Scatter(x=tspan, y=tmean, fill=None, mode='lines', line=dict(color=colorlist[i][0],), name=n, legendgroup=n)
        ttr_lower95 = Scatter(x=tspan, y=tlower95, fill=None, mode='lines', line=dict(width='0.1', color=colorlist[i][3],),  legendgroup=n, name='lower 95% CI', showlegend=False)
        ttr_upper95 = Scatter(x=tspan, y=tupper95, fill='tonexty', mode='lines', line=dict(width='0.1', color=colorlist[i][3],),  legendgroup=n, name='upper 95% CI', showlegend=False)
        ttr_lower90 = Scatter(x=tspan, y=tlower90, fill=None, mode='lines', line=dict(width='0.1', color=colorlist[i][2],),  legendgroup=n, name='lower 90% CI', showlegend=False)
        ttr_upper90 = Scatter(x=tspan, y=tupper90, fill='tonexty', mode='lines', line=dict(width='0.1', color=colorlist[i][2],),  legendgroup=n, name='upper 90% CI', showlegend=False)
        ttr_lower50 = Scatter(x=tspan, y=tlower50, fill=None, mode='lines', line=dict(width='0.1', color=colorlist[i][1],),  legendgroup=n, name='lower 50% CI', showlegend=False)
        ttr_upper50 = Scatter(x=tspan, y=tupper50, fill='tonexty', mode='lines', line=dict(width='0.1', color=colorlist[i][1],),  legendgroup=n, name='upper 50% CI', showlegend=False)
        traces.extend([ttr_m, ttr_lower95, ttr_upper95, ttr_lower90, ttr_upper90, ttr_lower50, ttr_upper50])

    layout = Layout(title='Overall Simulated Cellular Dynamics', xaxis=dict(dtick=30, title='days'), yaxis=dict(title='No. of cells (10<sup>8</sup>)'))
    fig = Figure(data=traces, layout=layout)

    return fig
