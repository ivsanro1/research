import mlflow
from pyngrok import ngrok
import subprocess
from time import sleep


def launch_and_publicly_expose_mlflow_server(mlflow_tracking_uri, ngrok_auth_token, nb=True):
    
    
    command = f'''mlflow server --port 5000 --backend-store-uri {mlflow_tracking_uri} --gunicorn-opts "--worker-class gevent --threads 3 --workers 3 --timeout 300 --keep-alive 300 --log-level INFO" &''' # run tracking UI in the background
    # run tracking UI in the background
    if nb:
        get_ipython().system_raw(command)
    else:
        subprocess.Popen(command, shell=True)

    # create remote tunnel using ngrok.com to allow local port access
    # borrowed from https://colab.research.google.com/github/alfozan/MLflow-GBRT-demo/blob/master/MLflow-GBRT-demo.ipynb#scrollTo=4h3bKHMYUIG6

    # Terminate open tunnels if exist
    ngrok.kill()

    # Setting the authtoken (optional)
    # Get your authtoken from https://dashboard.ngrok.com/auth
    ngrok.set_auth_token(ngrok_auth_token)

    # Open an HTTPs tunnel on port 5000 for http://localhost:5000
    ngrok_tunnel = ngrok.connect(addr="5000", proto="http", bind_tls=True)
    print("MLflow Tracking UI:", ngrok_tunnel.public_url)
    if not nb:
        while True:
            sleep(10000000)
    
from pathlib import Path
import os

NGROK_AUTH_TOKEN = '222nASPBPUk74ebQAdocLSQmDiz_2WhhYPUrHhZCSHddFGyAJ'

# Override/set credentials in env var
os.environ['CWD'] = str(Path(os.getcwd()).parent)

# Base paths
cwd = Path(os.environ['CWD'])
dir_data = cwd / 'data'

# Set mlflow artifacts location
dir_exp_root = Path(cwd / 'experiments')
dir_exp_this = Path(dir_exp_root / 'record_linkage')
dir_exp_mlflow = dir_exp_this / 'mlflow'
dir_exp_mlflow.mkdir(exist_ok=True, parents=True)

import mlflow
mlflow_tracking_uri = (dir_exp_mlflow / 'mlruns').as_uri()
print(f'mlflow URI: {mlflow_tracking_uri}') # file:///root/work/research/experiments/record_linkage/mlflow/mlruns

launch_and_publicly_expose_mlflow_server(
    mlflow_tracking_uri=mlflow_tracking_uri,
    ngrok_auth_token=NGROK_AUTH_TOKEN,
    nb=False
)