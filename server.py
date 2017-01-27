import logging
import time
from os import environ

import requests

def num_agents():
  url = '/'.join([mesos.rstrip('/'), "slaves"])
  r = requests.get(url)
  agents = len([slave for slave in r.json()["slaves"] if slave["active"]])
  logging.debug("Discovered {} agents.".format(str(agents)))
  return agents

def app_url(app):
  return '/'.join([marathon.rstrip('/'), "v2/apps", app.strip('/')])

def app_instances(app):
  r = requests.get(app_url(app))
  instances = r.json()["app"]["instances"]
  logging.debug("{} currently running with {} instances.".format(app, str(instances)))
  return instances

def scale_app(app, instances):
    logging.warn("Scaling {} to {} instances.".format(app, str(instances)))
    requests.put(app_url(app), json={"instances": instances})

if __name__ == "__main__":

  marathon = environ["MARATHON_URL"] if "MARATHON_URL" in environ else "http://localhost:8080/"
  mesos = environ["MESOS_URL"] if "MESOS_URL" in environ else "http://localhost:5050/"
  sleep = int(environ["SLEEP_SECONDS"]) if "SLEEP_SECONDS" in environ else 60
  loglevel = environ["loglevel"] if "loglevel" in environ else "DEBUG"

  apps = environ["GLOBAL_APPS"].replace(' ', '').split(',')

  level = getattr(logging, loglevel.upper())
  logging.basicConfig(level=level)

  while True:
    agents = num_agents()
    for app in apps:
      if app_instances(app) != agents:
        scale_app(app, agents)

    time.sleep(sleep)
