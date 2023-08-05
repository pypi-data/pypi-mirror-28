"""ReSim Flask App

ReSim GUI powered by Flask app.

"""

import os
from flask import Flask, request, render_template, redirect, flash, Markup
from flask_wtf.csrf import CSRFProtect
from resim_compute import run_web_resim
from resim_form import WholeInputForm, tooltipdict

def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.secret_key = os.urandom(24).encode('hex')
    csrf = CSRFProtect(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/download')
    def downloads():
        return render_template('download.html')

    @app.route('/docs')
    def docs():
        return render_template('docs.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/resim', methods=['GET', 'POST'])
    def resim():
        form = WholeInputForm(request.form)

        result=run_web_resim(n=3)
        tmp_ids=result['ids']
        tmp_graphJSON=result['graphJSON']

        if request.method == 'POST' and form.validate():
            result = run_web_resim(
                gr_s=form.GrowthRate.gr_s.data,
                gr_pr=form.GrowthRate.gr_pr.data,
                gr_ar=form.GrowthRate.gr_ar.data,
                dose=form.Drug.dose.data,
                ds=form.Drug.ds.data,
                ke=form.Drug.ke.data,
                ki=form.Drug.ki.data,
                qf=form.Drug.qf.data,
                total_0=form.InitialState.total_0.data,
                s_0=form.InitialState.s_0.data,
                pr_0=form.InitialState.pr_0.data,
                q_0=form.InitialState.q_0.data,
                t=form.Simulation.t.data,
                n=form.Simulation.n.data)
        else:
            result=run_web_resim(n=3)

        tmp_ids=result['ids']
        tmp_graphJSON=result['graphJSON']

        return render_template('resim_dash.html', form=form, ids=tmp_ids, graphJSON=tmp_graphJSON)

    @app.context_processor
    def utility_processor():
        def render_inputaddon_span_withtooltip(fieldname, tooltipdict=tooltipdict):
            dictkey = fieldname.split("-", 1)[1]
            tooltipmsg = tooltipdict[dictkey]
            tmp_msg = '<span class="input-group-addon" data-toggle="tooltip" data-placement="top" title="' + tooltipmsg + '">'
            return Markup(tmp_msg)
        return dict(render_inputaddon_span_withtooltip=render_inputaddon_span_withtooltip)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def page_not_found(e):
        return render_template('500.html'), 404

    return app

#app.run()
