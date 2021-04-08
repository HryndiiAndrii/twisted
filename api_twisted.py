import json
import logging

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, gatherResults
from twisted.internet.ssl import ClientContextFactory
from twisted.web.client import Agent, readBody
from twisted.web.http_headers import Headers

# ---------- Channels ----------

channels = ['nyc_timescape',]

# ---------- Getting authentication token ----------

with open('key.txt', 'r') as f:
    token = f.read()

# ---------- Authentication variables ----------

# authURL = 'https://id.twitch.tv/oauth2/token'
Client_ID = ['50vngdkhl7a1e7hndy4jde5vn86jil']
# Secret = ['1f3od2iruizc6opve05afluo4qni7m']
# AutParams = {'client_id': Client_ID,
#              'client_secret': Secret,
#              'grant_type': ['client_credentials']}

# ---------- API URL and headers ----------

URL = 'https://api.twitch.tv/helix/streams?user_login='

headers = {'Client-ID': Client_ID,
           'Authorization': ["Bearer " + token]}

# ---------- Logging functions ----------

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

# ---------- Twisted client ----------

class WebClientContextFactory(ClientContextFactory):
    def getContext(self, hostname, port):
        return ClientContextFactory.getContext(self)


@inlineCallbacks
def display(response):
    print "Received response"
    body = yield readBody(response)
    cbBody(body)


def cbBody(body):
    jsonbody = json.loads(body)
    data = jsonbody['data'][0]
    logger = setup_logger(channels[0], channels[0]+'.log')
    logger.info('Modeling data:')
    moddeling_data = "User login: {0}, Language: {1}, Thumbnail URL: {2}".format(data['user_login'], data['language'], data['thumbnail_url'])
    logger.info('Modeling data: ' + moddeling_data)
    logger.info('Monitoring data:')
    monitoring_data = "Game name: {0}, Started at: {1}, Viewer count: {2}".format(data['game_name'], data['started_at'], data['viewer_count'])
    logger.info('Modeling data: ' + monitoring_data)


@inlineCallbacks
def get_response(agent, url):
    response = yield agent.request("GET", url, Headers(headers))
    display(response)


def main():
    contextFactory = WebClientContextFactory()
    agent = Agent(reactor, contextFactory)
    d = gatherResults([get_response(agent, URL + channels[0])])
    d.addBoth(lambda stop: reactor.stop())


if __name__ == '__main__':
    main()
    reactor.run()
