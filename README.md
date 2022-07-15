# AudioCodes SBC Prometheus exporter
This is an exporter that exposes information gathered from AudioCodes SBC for use by the Prometheus monitoring system.

**This is a work in progress!!**

## Installation
`pip install audiocodes-exporter`

## Usage
Default port is statically set to 9954!

The parameters can be set with env variables as well.
`audiocodes-exporter [-h] -H API_URL -u API_USERNAME -p API_PASSWORD`

## Requirements
AudioCodes SBC v7.4
Python 3.10+