import time
import pytest

from abstract_open_traffic_generator.result import FlowRequest, CaptureRequest
from abstract_open_traffic_generator.control import FlowTransmit, PortCapture
from abstract_open_traffic_generator.port import Capture

from tests.common.helpers.assertions import pytest_assert

from tests.common.reboot import logger
from tests.common.fixtures.conn_graph_facts import conn_graph_facts,\
    fanout_graph_facts 

from tests.common.ixia.ixia_fixtures import ixia_api_serv_ip, \
    ixia_api_serv_user, ixia_api_serv_passwd, ixia_dev, ixia_api_serv_port,\
    ixia_api_serv_session_id, api

from files.configs.ecn import ecn_marking_at_ecress, one_hundred_gbe, serializer
from files.configs.ecn import start_delay, traffic_duration, pause_line_rate,\
    traffic_line_rate, port_bandwidth, bw_multiplier, frame_size
from files.qos_fixtures import lossless_prio_dscp_map, ecn_thresholds

START_DELAY = [1]
TRAFFIC_DURATION = [3]
PAUSE_LINE_RATE = [100]
TRAFFIC_LINE_RATE = [50]
BW_MULTIPLIER = [1000000]
FRAME_SIZE = [1024]
TOLERANCE_THRESHOLD = .97
ECN_THRESHOLD = [250000]

@pytest.mark.parametrize('start_delay', START_DELAY)
@pytest.mark.parametrize('traffic_duration', TRAFFIC_DURATION)
@pytest.mark.parametrize('pause_line_rate', PAUSE_LINE_RATE)
@pytest.mark.parametrize('traffic_line_rate', TRAFFIC_LINE_RATE)
@pytest.mark.parametrize('bw_multiplier', BW_MULTIPLIER)
@pytest.mark.parametrize('frame_size', FRAME_SIZE)
@pytest.mark.parametrize('ecn_thresholds', ECN_THRESHOLD)
def test_ecn_marking_at_ecress(api, 
                               duthost, 
                               ecn_marking_at_ecress, 
                               start_delay,
                               pause_line_rate,
                               traffic_line_rate, 
                               traffic_duration,
                               port_bandwidth,
                               frame_size,
                               ecn_thresholds) :

    duthost.shell('sudo pfcwd stop')
    duthost.shell('sudo sudo ecnconfig -p AZURE_LOSSLESS -gmax %s' %(ecn_thresholds))
    duthost.shell('sudo sudo ecnconfig -p AZURE_LOSSLESS -gmin %s' %(ecn_thresholds))

    for base_config in ecn_marking_at_ecress:
        rx_port=base_config.ports[1]
        rx_port.capture=Capture(choice=[], enable=True)

        # create the configuration
        api.set_config(base_config)

        # start capture
        api.set_port_capture(PortCapture(port_names=[rx_port.name]))

        # start all flows
        api.set_flow_transmit(FlowTransmit(state='start'))

        exp_dur = start_delay + traffic_duration
        logger.info("Traffic is running for %s seconds" %(traffic_duration))
        time.sleep(exp_dur)

        # stop all flows
        api.set_flow_transmit(FlowTransmit(state='stop'))

        pcap_bytes = api.get_capture_results(CaptureRequest(port_name=rx_port.name))

        # Get statistics
        test_stat = api.get_flow_results(FlowRequest())

        for rows in test_stat['rows'] :
            tx_frame_index = test_stat['columns'].index('frames_tx')
            rx_frame_index = test_stat['columns'].index('frames_rx')
            caption_index = test_stat['columns'].index('name')   
            if ((rows[caption_index] == 'Test Data') or
                (rows[caption_index] == 'Background Data')):
                tx_frames = float(rows[tx_frame_index])
                rx_frames = float(rows[rx_frame_index])
                if ((tx_frames != rx_frames) or (rx_frames == 0)) :
                    pytest_assert(False,
                        "Not all %s reached Rx End" %(rows[caption_index]))

        # write the pcap bytes to a local file
        with open('%s.pcap' % rx_port.name, 'wb') as fid:
            fid.write(pcap_bytes) 

        from scapy.all import PcapReader
        reader = PcapReader('%s.pcap' % rx_port.name)
        for item in reader:
            logger.info(tem.time)
            logger.info(item.show())

        # Trafic verification is still pending 
        # issue https://github.com/open-traffic-generator/ixnetwork/issues/55 

