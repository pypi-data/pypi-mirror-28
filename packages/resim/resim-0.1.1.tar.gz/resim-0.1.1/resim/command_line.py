"""ReSim - entry point
"""

from . import create_app

#def resim_cui():
    #print('This is still in development, please use ReSim in your own python SDE!')

def run_resim_flask():
    """run resim flask from command prompt"""
    print ('setting up the flask app...')
    app = create_app()
    print ('done')
    app.run()
