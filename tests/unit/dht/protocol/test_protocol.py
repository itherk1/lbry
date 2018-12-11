import asyncio
from torba.testcase import AsyncioTestCase
from tests import dht_mocks
from lbrynet.dht import constants
from lbrynet.dht.protocol.protocol import KademliaProtocol
from lbrynet.peer import PeerManager


class TestProtocol(AsyncioTestCase):
    async def test_ping(self):
        loop = asyncio.get_event_loop()
        with dht_mocks.mock_network_loop(loop):
            node_id1 = constants.generate_id()
            peer1 = KademliaProtocol(
                PeerManager(loop), loop, node_id1, '1.2.3.4', 4444, 3333
            )
            peer2 = KademliaProtocol(
                PeerManager(loop), loop, constants.generate_id(), '1.2.3.5', 4444, 3333
            )
            await loop.create_datagram_endpoint(lambda: peer1, ('1.2.3.4', 4444))
            await loop.create_datagram_endpoint(lambda: peer2, ('1.2.3.5', 4444))

            peer = peer2.peer_manager.make_peer('1.2.3.4', dht_protocol=peer2, node_id=node_id1, udp_port=4444)
            result = await peer.ping()
            peer1.transport.close()
            peer2.transport.close()
            self.assertEqual(result, b'pong')
