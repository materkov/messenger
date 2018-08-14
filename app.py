import newrelic.agent

newrelic.agent.initialize()
from flask import Flask
import os

with open('.env') as f:
    lines = f.readlines()
    for line in lines:
        k, v = line.split('=', 2)
        k = k.strip()
        v = v.strip()
        os.environ[k] = v

app = Flask(__name__)

import api
