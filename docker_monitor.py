import psutil
import json
import socket
import time
import isConnect
import docker


with open('config.json', 'r') as f:
    config = json.load(f)
scheduling_addrs=[]
for ip in config['scheduling']['ip']:
    scheduling_addr = (ip, config['scheduling']['heartbeat-port'])
    scheduling_addrs.append(scheduling_addr)
self_ip = config['self']['ip']
self_net_name = config['self']['net_name']
docker_client = docker.from_env(version='1.24', timeout=600)


def get_containers_len():
    return len(docker_client.containers.list())


def send():
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        mem_total = psutil.virtual_memory().total
        mem_use = mem_total - psutil.virtual_memory().available
        cpu_count = psutil.cpu_count(logical=True)
        cpu_use = psutil.cpu_percent()
        former_recv = psutil.net_io_counters(pernic=True).get(self_net_name).bytes_sent
        time.sleep(1)
        later_recv = psutil.net_io_counters(pernic=True).get(self_net_name).bytes_sent
        ping_test = isConnect.Update()
        containers_len = get_containers_len()
        send_json = json.dumps({
            'ip': self_ip,
            'cpu_counts': cpu_count,
            'cpu_use': cpu_use,
            'mem_total': mem_total,
            'mem_use': mem_use,
            'net_use': later_recv - former_recv,
            'containers_len': containers_len,
            'ping_test': ping_test,
        })
        for in_scheduling_addr in scheduling_addrs:
            try:
                sockfd.sendto(send_json, in_scheduling_addr)
                break
            except Exception as e:
                continue
        time.sleep(9)


if __name__ == '__main__':
    send()
