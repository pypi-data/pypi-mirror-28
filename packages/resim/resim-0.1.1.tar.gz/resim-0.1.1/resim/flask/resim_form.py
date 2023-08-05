"""ReSim Web Form for GUI

Web forms for run_web_resim input params panel.

Attributes:
    params (list): a list contains the params available in the web form.
    tooltiplabels (list): a list contains tooltips for the params.
    unitlabels (list): a list contains the unit for params.

"""

from wtforms import Form, FloatField, IntegerField, FormField
from wtforms.validators import InputRequired, NumberRange, ValidationError

###---define labels
params = ['gr_s', 'gr_pr', 'gr_ar', 'dose', 'ds', 'ke', 'ki', 'qf', 'total_0', 's_0', 'pr_0', 'q_0', 't', 'n']
tooltiplabels = ['growth rate (sensitive)', 'growth rate (primary resistant)', 'growth rate (aquired resistant)', 'bioavailable dosage', 'maximal death rate', 'drug half-life', 'Ki of the drug', 'drug induced quiescent factor', 'Initial total tumor cells number', 'Initial fraction of senstive cancer cells', 'Initial fraction of primary resistant cells', 'Initial fraction of quiescent cells', 'duration', 'number of simulations']
unitlabels = ['day^-1', 'day^-1', 'day^-1', '', 'day^-1', 'day^-1', '', '', '10^8', '', '', '', 'days', 'times']

def equal_len(labels):
    """A function to add whitespace(s) &nbsp; to match labels"""
    new_labels=[]
    lenlab=[]
    for _, n in enumerate(labels):
        lenlab.append(len(n))
    for i, n in enumerate(labels):
        new_labels.append(n + '&nbsp;'*(max(lenlab)-lenlab[i]))
    return new_labels

padded_params = equal_len(params)
#padded_paramlabels = equal_len(paramlabels)
padded_unitlabels = equal_len(unitlabels)

gr_params = padded_params[0:3]
#gr_paramlabels = padded_paramlabels[0:3]
gr_unitlabels = padded_unitlabels[0:3]

drug_params = padded_params[3:8]
#drug_paramlabels = padded_paramlabels[3:8]
drug_unitlabels = padded_unitlabels[3:8]

init_params = padded_params[8:12]
#init_paramlabels = padded_paramlabels[8:10]
init_unitlabels = padded_unitlabels[8:12]

sim_params = padded_params[12:]
#sim_paramlabels = padded_paramlabels[10:]
sim_unitlabels = padded_unitlabels[12:]

tooltipdict={}
for i, n in enumerate(params):
    tooltipdict[n] = tooltiplabels[i]

###---custom validators
def check_s0(form, field):
    """Custom Form Validator: raise error if sum of (s_0, pr_0, q_0) =/= 1"""
    s_0 = field.data
    pr_0 = form.pr_0.data
    q_0 = form.q_0.data
    if (s_0 + pr_0 + q_0) != 1:
        raise ValidationError('sum of s_0, pr_0 and q_0 should be equal to 1')

def check_pr0(form, field):
    """Custom Form Validator: raise error if sum of (s_0, pr_0, q_0) =/= 1"""
    s_0 = form.s_0.data
    pr_0 = field.data
    q_0 = form.q_0.data
    if (s_0 + pr_0 + q_0) != 1:
        raise ValidationError('sum of s_0, pr_0 and q_0 should be equal to 1')

def check_q0(form, field):
    """Custom Form Validator: raise error if sum of (s_0, pr_0, q_0) =/= 1"""
    s_0 = form.s_0.data
    pr_0 = form.pr_0.data
    q_0 = field.data
    if (s_0 + pr_0 + q_0) != 1:
        raise ValidationError('sum of s_0, pr_0 and q_0 should be equal to 1')

###---forms class
class GrowthRateParamsInput(Form):
    """Web Form for growth rate params input"""
    gr_s = FloatField(
        label=gr_params[0], description=gr_unitlabels[0],
        default=0.015,
        validators=[InputRequired(), NumberRange(min=0, message='gr should be a positive value')])
    gr_pr = FloatField(
        label=gr_params[1], description=gr_unitlabels[1],
        default=0.015,
        validators=[InputRequired(), NumberRange(min=0, message='gr should be a positive value')])
    gr_ar = FloatField(
        label=gr_params[2], description=gr_unitlabels[2],
        default=0.015,
        validators=[InputRequired(), NumberRange(min=0, message='gr should be a positive value')])

class DrugRelatedParamsInput(Form):
    """Web Form for drug related params input"""
    dose = FloatField(
        label=drug_params[0], description=drug_unitlabels[0],
        default=240,
        validators=[InputRequired(), NumberRange(min=0, message='dose should be a positive value')])
    ds = FloatField(
        label=drug_params[1], description=drug_unitlabels[1],
        default=0.9,
        validators=[InputRequired(), NumberRange(min=0.1, max=0.99999, message='ds  &isin; [0.1, 1)')])
    ke = FloatField(
        label=drug_params[2], description=drug_unitlabels[2],
        default=0.7,
        validators=[InputRequired(), NumberRange(min=0.1, max=0.99999, message='ke  &isin; [0.1, 1)')])
    ki = FloatField(
        label=drug_params[3], description=drug_unitlabels[3],
        default=10,
        validators=[InputRequired(), NumberRange(min=0.1, message='q_0 should be larger than 0.1')])
    qf = FloatField(
        label=drug_params[4], description=drug_unitlabels[4],
        default=10,
        validators=[InputRequired(), NumberRange(min=0, max=20, message='qf &isin; [0, 20]')])

class InitialStateParamsInput(Form):
    """Web Form for initial state params input"""
    total_0 = FloatField(
        label=init_params[0], description=init_unitlabels[0],
        default=0.5,
        validators=[InputRequired(), NumberRange(min=0.1, max=100, message='total_0 &isin; [0.1, 100]')])
    s_0 = FloatField(
        label=init_params[1], description=init_unitlabels[1],
        default=0.84,
        validators=[InputRequired(), NumberRange(min=0, max=1, message='s_0 &isin; [0, 1]'), check_s0])
    pr_0 = FloatField(
        label=init_params[2], description=init_unitlabels[2],
        default=0.1,
        validators=[InputRequired(), NumberRange(min=0, max=1, message='pr_0 &isin; [0, 1]'), check_pr0])
    q_0 = FloatField(
        label=init_params[3], description=init_unitlabels[3],
        default=0.06,
        validators=[InputRequired(), NumberRange(min=0, max=1, message='q_0 &isin; [0, 1]'), check_q0])

class SimulationParamsInput(Form):
    """Web Form for simulation params input"""
    t = IntegerField(
        label=sim_params[0], description=sim_unitlabels[0],
        default=365,
        validators=[InputRequired(), NumberRange(min=365, max=720, message='t &isin; [365, 720]')])
    n = IntegerField(
        label=sim_params[1], description=sim_unitlabels[1],
        default=3,
        validators=[InputRequired(), NumberRange(min=3, max=100, message='n &isin; [3, 100]')])

class WholeInputForm(Form):
    """Web Form of params input panel"""
    Drug = FormField(DrugRelatedParamsInput)
    InitialState = FormField(InitialStateParamsInput)
    GrowthRate = FormField(GrowthRateParamsInput)
    Simulation = FormField(SimulationParamsInput)
