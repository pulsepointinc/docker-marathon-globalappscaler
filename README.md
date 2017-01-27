# docker-marathon-globalappscaler

At this time, marathon does not support global applications ( i.e. applications that should run on every node ). This project seeks to provide some minimal support for those to address some specific needs of ours.

It is implemented as a docker container which we run as a marathon app. Basically, it:

* Determines the number of mesos agents
* For each configured app, check the current value of the `instances` attribute
* Update the `instances` attribute if not equal to the number of mesos agents
* Sleep for some configured number of seconds
* Repeat forever

## Configuration

The following values are read from the environment:

env | default
--- | ---
MARATHON_URL | http://localhost:8080/ 
MESOS_URL | http://localhost:5050/
SLEEP_SECONDS | 60
GLOBAL_APPS | None

`GLOBAL_APPS` should be a comma-separated list of application ids. For example,

    GLOBAL_APPS="/my/apps/foo,/my/apps/bar"

## Usage

    docker run ... \
    --env MESOS_URL="http://mesos.example.org:5050/" \
    --env MARATHON_URL="http://marathon.example.org:8080/" \
    --env GLOBAL_APPS="/my/apps/foo,/my/apps/bar" \
    pulsepointinc/marathon-globalappscaler

## Known Issues

There is a total lack of error handling, and the simple python script hasn't seen much use. YMMV.