#!/usr/bin/env python3

import argparse
import sys
import time

from raiblocks import RPCClient

from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY


class RaiblocksCollector(object):
    def __init__(self, conn):
        self.conn = conn

    def collect(self):
        # Version
        version = self.conn.version()
        yield GaugeMetricFamily('rpc_version', 'Version of RPC', float(version['rpc_version']))
        yield GaugeMetricFamily('store_version', 'Version of store', float(version['store_version']))

        # Available Supply
        available_supply = self.conn.available_supply()
        yield GaugeMetricFamily('available_supply', 'Available supply', float(available_supply))

        # Total block count
        block_count = self.conn.block_count()
        yield GaugeMetricFamily('block_count', 'Number of blocks', float(block_count['count']))
        yield GaugeMetricFamily('block_count_unchecked', 'Number of unchecked blocks', float(block_count['unchecked']))

        # Block type counts
        block_count_type = self.conn.block_count_type()
        yield GaugeMetricFamily('block_count_open', 'Number of open blocks', float(block_count_type['open']))
        yield GaugeMetricFamily('block_count_send', 'Number of send blocks', float(block_count_type['send']))
        yield GaugeMetricFamily('block_count_change', 'Number of change blocks', float(block_count_type['change']))
        yield GaugeMetricFamily('block_count_receive', 'Number of receive blocks', float(block_count_type['receive']))

        # Frontier count
        frontier_count = self.conn.frontier_count()
        yield GaugeMetricFamily('frontier_count', 'Number of frontiers', float(frontier_count))


def parse_args():
    parser = argparse.ArgumentParser(description='Prometheus exporter for Raiblocks.')
    parser.add_argument(
        '-l', metavar='LISTEN', default='localhost:9410',
        help='address on which to expose metrics (default ":9410")'
    )
    parser.add_argument(
        '-n', metavar='HOST', default='localhost',
        help='address of Raiblocks server (default "localhost")'
    )
    parser.add_argument(
        '-p', metavar='PORT', default='7076',
        help='RPC port of Raiblocks server (default "7076")'
    )
    return parser.parse_args()


def main():
    try:
        args = parse_args()
        addr, port = args.l.split(':')
        rpc = RPCClient('http://localhost:7076')
        REGISTRY.register(RaiblocksCollector(rpc))
        start_http_server(int(port), addr)
        print("Exporter successfully started. CTRL+C to exit.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(' Interrupted')
        sys.exit(0)

if __name__ == '__main__':
    main()
