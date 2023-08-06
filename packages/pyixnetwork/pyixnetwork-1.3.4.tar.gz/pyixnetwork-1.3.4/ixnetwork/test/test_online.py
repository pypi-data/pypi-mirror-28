"""
IxNetwork package tests that require actual IxNetwork chassis and active ports.

Note that in many places there are (relatively) long delays to make sure the tests work in all setups.

Test setup:
Two IXN ports connected back to back.

@author yoram@ignissoft.com
"""

from os import path

import time

from ixnetwork.test.test_base import IxnTestBase
from ixnetwork.ixn_statistics_view import IxnPortStatistics, IxnTrafficItemStatistics, IxnFlowStatistics


class IxnTestOnline(IxnTestBase):

    ports = []

    def testReservePorts(self):
        self._reserve_ports(path.join(path.dirname(__file__), 'configs/test_config.ixncfg'))

    def testPortsOnline(self):
        self._reserve_ports(path.join(path.dirname(__file__), 'configs/test_config.ixncfg'))

        for port in self.ports:
            assert(port.is_online())

        for port in self.ports:
            port.release()

    def testReload(self):

        self._reserve_ports(path.join(path.dirname(__file__), 'configs/test_config.ixncfg'))

        for port in self.ports:
            port.release()

        self.ixn.root.get_object_by_name('Port 2').reserve(self.config.get('IXN', 'port1'))
        self.ixn.root.get_object_by_name('Port 1').reserve(self.config.get('IXN', 'port2'))

        self._reserve_ports(path.join(path.dirname(__file__), 'configs/test_config.ixncfg'))

    def testReleasePorts(self):
        self._reserve_ports(path.join(path.dirname(__file__), 'configs/test_config.ixncfg'))
        for port in self.ports:
            port.release()

    def testInterfaces(self):
        self._reserve_ports(path.join(path.dirname(__file__), 'configs/test_config.ixncfg'))
        for port in self.ports:
            port.send_arp_ns()
            time.sleep(8)
            for interface in port.get_children('interface'):
                gateway = interface.get_child('ipv4', 'ipv6').get_attribute('gateway')
                interface.ping(gateway)

    def testProtocolsActions(self):
        self._reserve_ports(path.join(path.dirname(__file__), 'configs/test_config.ixncfg'))
        self.ixn.send_arp_ns()
        self.ixn.protocols_start()
        time.sleep(8)
        self.ixn.protocols_stop()
        time.sleep(8)
        self.ixn.protocol_start('ospf')
        time.sleep(8)
        self.ixn.protocol_stop('ospf')
        pass

    def testGUITraffic(self):
        self._reserve_ports(path.join(path.dirname(__file__), 'configs/test_config.ixncfg'))
        self.ixn.send_arp_ns()
        self.ixn.regenerate()
        self.ixn.traffic_apply()
        self.ixn.l23_traffic_start()
        time.sleep(8)
        self.ixn.l23_traffic_stop()
        port_stats = IxnPortStatistics(self.ixn.root)
        port_stats.read_stats()
        print(port_stats.get_all_stats())
        print(port_stats.get_object_stats('Port 1'))
        assert(int(port_stats.get_stat('Port 1', 'Frames Tx.')) >= 1600)
        self.ixn.l23_traffic_start(blocking=True)
        ti_stats = IxnTrafficItemStatistics(self.ixn.root)
        ti_stats.read_stats()
        assert(int(ti_stats.get_object_stats('Traffic Item 1')['Tx Frames']) == 1600)
        flow_stats = IxnFlowStatistics(self.ixn.root)
        flow_stats.read_stats()
        assert(int(flow_stats.get_stat('Port 2/Port 1/Traffic Item 1', 'Tx Frames')) == 800)

    def testNgpf(self):
        self._reserve_ports(path.join(path.dirname(__file__), 'configs/ngpf_config.ixncfg'))
        topologies = self.ixn.root.get_children('topology')
        self.ixn.protocols_start()
        time.sleep(8)
        assert(topologies[0].get_attribute('status') == 'started')
        self.ixn.protocols_stop()
        time.sleep(2)
        assert(topologies[0].get_attribute('status') == 'notStarted')
        # No need to test since protocol start/stop methods will raise exception if the operation failed.
        topologies[0].start()
        topologies[1].start()
        topologies[0].stop()
        topologies[1].stop()
        device_group = topologies[0].get_child('deviceGroup')
        device_group.start()
        device_group.stop()
        ethernet = device_group.get_child('ethernet')
        ethernet.start()
        ethernet.stop()

    def _reserve_ports(self, config_file):
        self._load_config(config_file)
        self.ports = self.ixn.root.get_children('vport')
        self.ixn.root.get_object_by_name('Port 1').reserve(self.config.get('IXN', 'port1'), wait_for_up=False)
        self.ixn.root.get_object_by_name('Port 2').reserve(self.config.get('IXN', 'port2'), wait_for_up=False)
        for port in self.ports:
            port.wait_for_states(60, 'up')
