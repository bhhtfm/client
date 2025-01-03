import caseus
import pak
import json

class MyProxy(caseus.proxies.LoggingProxy, caseus.proxies.InputListeningProxy):
    # BLOCK INVENTORY ITEMS
    @pak.packet_listener(caseus.clientbound.AddShamanObjectPacket)
    async def fetch_object(self, source, packet):
        if packet.shaman_object_id in {6, 0, 34, 65, 89, 33, 95, 97}:
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

    # REQUEST ROOM LIST
    @pak.packet_listener(caseus.clientbound.RoomListPacket)
    async def save_room(self, source, packet):
        rooms_data = [{"name": room.name, "num_players": room.num_players} for room in packet.rooms]

        with open('vanilla.json', 'w', encoding='utf-8') as file:
            json.dump(rooms_data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    MyProxy().run()
