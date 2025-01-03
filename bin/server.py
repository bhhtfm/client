import caseus
import pak

# MAIN
class MyProxy(caseus.proxies.LoggingProxy, caseus.proxies.InputListeningProxy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.round_id = None
        self.object_id = None
        self.shaman_object_id = None

    @pak.packet_listener(caseus.clientbound.AddShamanObjectPacket)
    async def fetch_object(self, source, packet):
        self.object_id = packet.object_id
        self.shaman_object_id = packet.shaman_object_id

    @pak.packet_listener(caseus.serverbound.HandshakePacket)
    async def init_listening(self, source, packet):
        await source.listen_to_keyboard(117)

    async def on_keyboard(self, client, packet):
        if self.shaman_object_id in (6, 0, 34, 33, 65, 89, 95, 97):
            await client.write_packet(
                caseus.clientbound.ObjectSyncPacket,
            
                objects = [
                    caseus.ClientboundObjectInfo(
                        object_id = self.object_id,
                        shaman_object_id = -1,
                    ),
                ],        
            )
            return self.REPLACE_PACKET


if __name__ == "__main__":
    MyProxy().run()
