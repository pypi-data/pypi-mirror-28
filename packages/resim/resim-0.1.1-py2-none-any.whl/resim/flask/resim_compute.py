"""ReSim: chemoREsistance SIMulator

This is a simplified ReSim version for GUI.

"""

import json
import plotly
import resim
from resim_plot import plot_fht, plot_overalldynamics

def run_web_resim(
    gr_s=0.015, gr_pr=0.015, gr_ar=0.015,
    dose=240, ds=0.9, ke=0.7, ki=10, qf=10,
    total_0=0.5, s_0=0.84, pr_0=0.1, q_0=0.06,
    t=365, n=20):

    """Simplified ReSim for GUI

    The function receives input params from web form and using resim to compute

    Args:
        gr_s (float):
        gr_pr (float):


    Returns:
        A dictionary of keys 'ids' and 'graphJSON' back to flask app for plotly.
    """

    tmp_gr = [gr_s, gr_pr, gr_ar]
    tmp_d = [ki, qf, dose, ds, ke]
    tmp_init = [total_0 * s_0, total_0 * pr_0, 0, total_0 * q_0, 0]

    model = resim.Simulator(gr=tmp_gr, d=tmp_d, init=tmp_init, t=t, n=n)
    res = model.simulate()

    fig_fht = plot_fht(res)
    fig_od = plot_overalldynamics(res)

    graphs = [fig_fht, fig_od]

    # Add "ids" to each of the graphs to pass up to the client for templating
    tmp_ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    tmp_graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    result = dict(ids=tmp_ids, graphJSON=tmp_graphJSON)

    return result
