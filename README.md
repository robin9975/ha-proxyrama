# HA-proxyrama

HA-proxyrama aims to deliver real-time haproxy statistics easy and quickly. It's name comes from a real clever (ugh) combination of ha-proxy (obviously) and panorama.  

## Goal

In the shortterm, ha-proxyrama should deliver a docker container that only requires a URL to the HA-proxy stats page.  A frontend is made available that serves realtime statistics to the user. 

I didn't want to spend time configuring a time-series database, HA-proxy scraper, built a dashboard, etc. So, I did the most sensible thing to do and built an entire new tool, because hey, who doesn't want to learn how to do stuff with websockets?

## Features

- Scrape the HA-proxy statistics page every X seconds
- Serve these stats through websockets
- Do some 'smart' operations to create more insight and make visualisation easier 
- Dynamically define which servers and metrics you want to show


## Dependencies

- Vue.js
- Chart.js


## Disclaimer

This tool is pretty much untested for real-life usecases right now. Use with caution. 


