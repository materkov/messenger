import newrelic.agent
newrelic.agent.initialize()


from flask import Flask
app = Flask(__name__)

import api
