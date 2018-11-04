#!/usr/bin/env python

# WS server example

import time
import copy
import json
import random
import asyncio
import websockets

import requests
import base64

from collections import OrderedDict
from datetime import datetime

def get_data():
    headers = {"Authorization": "Basic {}".format(base64.b64encode(b"Admin:Admin").decode('ascii'))}
    raw_data = requests.get('http://localhost:9000/stats;csv', headers=headers).text
    lines = raw_data.split('\n')
    data_headers = lines[0][2:].split(',')
    return [
        {
            data_headers[index]: value for index, value in enumerate(x.split(','))
        }
        for x in lines[1:]
    ]

data = OrderedDict()

async def query_data():
    global data
    current = datetime.now().isoformat()
    new_data = get_data()

    data[current] = new_data
    await asyncio.sleep(1)
    asyncio.ensure_future(query_data())

async def hello(websocket, path):
    command = await websocket.recv()
    parameters = json.loads(command) 
    if parameters['command'] == 'update':
        while True:
            await websocket.send(json.dumps(generate_history_data(
                parameters['max_elements'],
                parameters['send_rate']
            ))) 
            await asyncio.sleep(parameters['send_rate'])
            await trigger_update(websocket, next(reversed(data)), parameters['send_rate'])
    if parameters['command'] == 'config':
        await websocket.send(
            json.dumps(get_config())
            )


def get_config():
    last_data = data[next(reversed(data))]
    return [
        {
            'name': "{} ({})".format(x['pxname'], x['svname']),
            'server': "{}_{}".format(x['pxname'], x['svname']),
            'metrics': [{
                'title': "Traffic",
                'unit': "Mb/s",
                'keys': ['d_bin', 'd_bout'], 
            }, {
                'title': 'Request rates',
                'unit': 'Request/s',
                'keys': ['d_hrsp_2xx', 'd_hrsp_3xx', 'd_hrsp_4xx', 'd_hrsp_5xx']
            }]
        }
        for x in last_data if x['pxname'] != ''
    ]

def generate_history_data(max_elements, send_rate):
    current_element = None
    history = {}
    keys = list(data.keys())
    for i in range(len(keys) - 1, max(0, len(keys) - (send_rate * max_elements)),  - send_rate):
        current_element = data[keys[i]]
        previous_element = data[keys[i - send_rate]] if (i - send_rate) > 0 else None
        history[keys[i]] = generate_data_element(previous_element, current_element)
    return history


def generate_data_element(prev_data, new_data):
    if prev_data is None:
        return new_data
    p = copy.deepcopy(prev_data)
    n = copy.deepcopy(new_data)
    for x, y in zip(p, n):
        keys = list(y.keys())
        for key in keys:
            try:
                y['d_{}'.format(key)] = int(y[key]) - int(x[key])
            except ValueError:
                continue
    return n

async def trigger_update(websocket, last_update, send_rate=10):
    last_update_key = next(reversed(data))

    new_data = data[last_update_key]
    prev_data = data[last_update]

    new_data = generate_data_element(prev_data, new_data)

    await websocket.send(json.dumps({last_update_key: new_data}))
    await asyncio.sleep(send_rate)
    await trigger_update(websocket, last_update_key, send_rate)


# socket_name = '/mnt/c/Users/Robin/Projects/haproxy_test.sock'
start_server = websockets.serve(hello, 'localhost', 9001)

asyncio.ensure_future(query_data())

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()