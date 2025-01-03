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
        await source.destination.write_packet(
            caseus.clientbound.ObjectSyncPacket,
             
            objects = [
                caseus.ClientboundObjectInfo(
                    object_id = packet.object_id,
                    shaman_object_id = -1,
                ),
            ],        
        )
        return self.REPLACE_PACKET 

if __name__ == "__main__":
    MyProxy().run()
