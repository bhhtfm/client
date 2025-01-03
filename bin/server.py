import caseus
import pak
import json
import re

class MyProxy(caseus.proxies.LoggingProxy, caseus.proxies.InputListeningProxy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object_id = None
        self.shaman_object_id = None
        self.round_id = None

    # BLOCK INVENTORY ITEMS
    @pak.packet_listener(caseus.clientbound.AddShamanObjectPacket)
    async def fetch_object(self, source, packet):
        self.object_id = packet.object_id
        self.shaman_object_id = packet.shaman_object_id 

        await source.destination.write_packet(
            caseus.clientbound.AddShamanObjectPacket,

            object_id = packet.object_id,
            shaman_object_id = -1,
            mice_collidable=False,
        )
        return self.REPLACE_PACKET

    @pak.packet_listener(caseus.clientbound.ObjectSyncPacket)
    async def get_sync_object(self, source, packet):
        for object in packet.objects:
            if object.shaman_object_id == self.shaman_object_id:
                await source.destination.write_packet(
                    caseus.clientbound.ObjectSyncPacket,

                     objects = [
                         caseus.ClientboundObjectInfo(
                             object_id = self.object_id,
                             shaman_object_id = 10,
                         )
                     ]
                )
                return self.REPLACE_PACKET

 #   @pak.packet_listener(caseus.clientbound.LegacyWrapperPacket)
 #   async def get_legacy(self, source, packet):
 #       await source.destination.write_packet(
 #           caseus.clientbound.LegacyWrapperPacket,
 #       )
 #       return self.REPLACE_PACKET   
        
    # REQUEST ROOM LIST
    @pak.packet_listener(caseus.clientbound.RoomListPacket)
    async def save_room(self, source, packet):
        rooms_data = [{"name": room.name, "num_players": room.num_players} for room in packet.rooms]

        with open('vanilla.json', 'w', encoding='utf-8') as file:
            json.dump(rooms_data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    MyProxy().run()
