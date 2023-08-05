"""The asynchronous rickshaw server that communicates with scheduling queues and
provides randomly generated input files.
"""
import sys
import json
import socket
import asyncio
import concurrent.futures
from argparse import ArgumentParser

import docker
import websockets

from rickshaw.docker_scheduler import DockerScheduler
from rickshaw.server_scheduler import ServerScheduler
import rickshaw.generate as generate


SEND_QUEUE = asyncio.Queue()

def all_archetypes():
    arches = generate.DEFAULT_SOURCES | generate.DEFAULT_SINKS
    for v in generate.NICHE_ARCHETYPES.values():
        arches |= v
    return arches


async def gather_annotations(scheduler, frequency=0.001):
    """The basic consumer of actions."""
    all_arches = all_archetypes()
    curr_arches = set(generate.ANNOTATIONS.keys())
    staged_tasks = []
    while curr_arches < all_arches:
        if SEND_QUEUE.qsize() > 0:
            await asyncio.sleep(min(frequency*1e3, 1.0))
            curr_arches = set(generate.ANNOTATIONS.keys())
            continue
        for arche in all_arches - curr_arches:
            msg = {'event': 'agent_annotations', 'params': {'spec': arche}}
            msg = json.dumps(msg)
            action_task = asyncio.ensure_future(SEND_QUEUE.put(msg))
            staged_tasks.append(action_task)
        if len(staged_tasks) > 0:
            await asyncio.wait(staged_tasks)
            staged_tasks.clear()
        await asyncio.sleep(frequency)
        curr_arches = set(generate.ANNOTATIONS.keys())
    await SEND_QUEUE.put('{"event": "shutdown", "params": {"when": "now"}}')
    scheduler.gathered_annotations = True


async def get_send_data():
    """Asynchronously grabs the next data to send from the queue."""
    data = await SEND_QUEUE.get()
    return data


async def queue_message_action(message):
    event = json.loads(message)
    params = event.get("params", {})
    kind = event["event"]
    if kind == 'agent_annotations':
        spec = params['spec']
        print('received agent annotations for ' + spec, file=sys.stderr)
        generate.ANNOTATIONS[spec] = event['data']
    else:
        print("ignoring received " + kind + " event", file=sys.stderr)


async def websocket_handler(websocket, scheduler):
    """Sends and recieves data via a websocket."""
    while not scheduler.gathered_annotations:
        recv_task = asyncio.ensure_future(websocket.recv())
        send_task = asyncio.ensure_future(get_send_data())
        done, pending = await asyncio.wait([recv_task, send_task],
                                           return_when=asyncio.FIRST_COMPLETED)
        # handle incoming
        if recv_task in done:
            message = recv_task.result()
            await queue_message_action(message)
        else:
            recv_task.cancel()
        # handle sending of data
        if send_task in done:
            message = send_task.result()
            await websocket.send(message)
        else:
            send_task.cancel()


async def websocket_client(port, scheduler, frequency=1.0):
    """Runs a websocket client on a host/port."""
    while not scheduler.cyclus_server_ready:
        await asyncio.sleep(frequency)
    host = scheduler.cyclus_server_host
    url = 'ws://{}:{}'.format(host, port)
    n = 0
    connected = False
    while not connected:
        try:
            async with websockets.connect(url) as websocket:
                connected = True
                print("connected to cyclus server websocket")
                await websocket_handler(websocket, scheduler)
        except Exception:
            n += 1
            if n > 10:
                raise
            print("failed to connect to websocket, retrying {0}/10".format(n))
    scheduler.stop_cyclus_server()


async def start_annotations_server(loop, executor, scheduler):
    """Starts up remote cyclus server"""
    run_task = loop.run_in_executor(executor, scheduler.start_annotations_server)
    await asyncio.wait([run_task])


async def schedule_sims(scheduler, frequency=0.001):
    """Loads jobs into the hopper, as needed."""
    freq = min(frequency*1e3, 1.0)
    while not scheduler.gathered_annotations:
        await asyncio.sleep(freq)
    while True:
        n = scheduler.want_n_more_jobs()
        if n == 0:
            await asyncio.sleep(freq)
            continue
        for i in range(n):
            sim = generate()
            scheduler.schedule(sim)


def _start_debug(loop):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('websockets.server')
    logger.setLevel(logging.ERROR)
    logger.addHandler(logging.StreamHandler())
    loop.set_debug(True)


def _find_open_port(host, port):
    found = False
    while not found:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((host, port))
        except socket.error as e:
            if e.errno == 98:
                port += 1
                continue
            else:
                raise
        finally:
            s.close()
        found = True
    return port


def make_parser():
    """Makes the argument parser for the rickshaw server."""
    p = ArgumentParser("rickshaw-server", description="Rickshaw Server CLI")
    p.add_argument('--debug', action='store_true', default=False,
                   dest='debug', help="runs the server in debug mode.")
    p.add_argument('--host', dest='host', default='localhost',
                   help='hostname to run the server on')
    p.add_argument('-p', '--port', dest='port', type=int, default=4242,
                   help='port to run the server on')
    p.add_argument('-n', '--nthreads', type=int, dest='nthreads', default=4,
                   help='Maximum number of thread workers to run with.')
    p.add_argument('-s', '--swarm', action='store_true', dest='swarm', default=False,
                   help='Run the server in swarm mode.')
    return p


def main(args=None):
    p = make_parser()
    ns = p.parse_args(args=args)
    # start up tasks
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=ns.nthreads)
    loop = asyncio.get_event_loop()
    if ns.swarm:
        print('started in swarm mode')
        scheduler = ServerScheduler(debug=ns.debug)
    else:
        print('started in docker mode')
        scheduler = DockerScheduler(debug=ns.debug)
    if ns.debug:
        _start_debug(loop)
    print("serving rickshaw at http://{}:{}".format(ns.host, ns.port))
    # run the loop!
    try:
        loop.run_until_complete(asyncio.gather(
            asyncio.ensure_future(websocket_client(ns.port, scheduler)),
            asyncio.ensure_future(gather_annotations(scheduler)),
            asyncio.ensure_future(start_annotations_server(loop, executor, scheduler)),
            asyncio.ensure_future(schedule_sims(scheduler)),
            ))
    finally:
        if not loop.is_closed():
            loop.close()


if __name__ == '__main__':
    main()
