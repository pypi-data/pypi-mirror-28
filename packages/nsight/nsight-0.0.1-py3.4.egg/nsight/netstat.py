import os
from collections import namedtuple
from subprocess import check_output
from .config import DATA_DIR

NMAP_SERVICES_PATH = os.path.join(DATA_DIR, 'nmap-services.txt')
PORTMAP = {}


PortMapping = namedtuple('PortMapping', 'name port proto')
NetstatLine = namedtuple('NetstatLine', 'proto recvq sendq local foreign state '
                         'pid prog')


def _parse_portmap_line(line):
    line = line.strip()
    if not line or line.startswith('#'):
        return None
    name, port_proto = line.split()[:2]
    port, proto = port_proto.split('/')
    return PortMapping(
        name=name,
        port=int(port),
        proto=proto,
    )


def load_portmap():
    if PORTMAP:
        return
    with open(NMAP_SERVICES_PATH) as f:
        for line in f:
            pm = _parse_portmap_line(line)
            if pm is None:
                continue
            PORTMAP[pm.proto, pm.port] = pm.name


def netstat():
    out = check_output(['netstat', '--ip', '-pltn'])
    netstats = []
    for line in out.splitlines():
        spl = line.split()
        proto = spl[0]
        if proto not in ['tcp', 'udp']:
            continue
        recvq = spl[1]
        sendq = spl[2]
        local = spl[3]
        foreign = spl[4]
        state = spl[5]
        pid_prog = spl[6]
        if pid_prog and pid_prog != '-':
            pid, prog = pid_prog.split('/', 1)
        else:
            pid, prog = None, None
        nsl = NetstatLine(
            proto=proto,
            recvq=recvq,
            sendq=sendq,
            local=local,
            foreign=foreign,
            state=state,
            pid=pid,
            prog=prog,
        )
        netstats.append(nsl)
    return netstats
