# import asyncio
# import json
# from django.contrib.auth import get_user_model
# from channels.consumer import AsyncConsumer
# from channels.db import database_sync_to_async

# from .models import DeliveryBoyOrders


# class ChatConsumer(AsyncConsumer):
#     async def websocket_connect(self, event):
#         # when the socket connects
#         # self.kwargs.get("username")
#         # self.other_username = self.scope['url_route']['kwargs']['username']
#         user = self.scope['user']
#         print(user)
#         thread_obj = user
#         self.cfe_chat_thread = thread_obj
#         self.room_group_name = "10"  # group
#         print(self.room_group_name)
#         print(self.channel_name)
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         # self.rando_user = await self.get_name()
#         await self.send({
#             "type": "websocket.accept"
#         })

#     async def websocket_receive(self, event):  # websocket.receive
#         message_data = json.loads(event['text'])
#         # print()
#         user = self.scope['user']
#         username = "unknown"
#         if user.is_authenticated:
#             username = user.username
#         message_data["user"] = username
#         await self.create_chat_message(user, message_data['msg'])
#         final_message_data = json.dumps(message_data)
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': final_message_data
#             }
#         )

#     async def broadcast_message(self, event):
#         await self.send({
#             "type": "websocket.send",
#             "text": json.dumps({'msg': "Loading data please wait...", 'user': 'admin'})
#         })
#         # chatbot? API -> another service --> response --> send
#         await asyncio.sleep(15)
#         await self.send({
#             "type": "websocket.send",
#             "text": event['message']
#         })

#     async def chat_message(self, event):
#         print(event)
#         await self.send({
#             "type": "websocket.send",
#             "text": event['text']
#         })

#     async def websocket_disconnect(self, event):
#         # when the socket connects
#         # print(event)
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # @database_sync_to_async
#     # def get_name(self):
#     #     return User.objects.all()[0].username

#     # @database_sync_to_async
#     # def get_thread(self, user, other_username):
#     #     return Thread.objects.get_or_new(user, other_username)[0]

#     # @database_sync_to_async
#     # def create_chat_message(self, user, message):
#     #     thread = self.cfe_chat_thread
#     #     return ChatMessage.objects.create(thread=thread, user=user, message=message)

# # class ChatConsumer(AsyncConsumer):
# #     async def websocket_connect(self, event):
# #         print("connected", event)
# #         await self.send((
# #             {
# #                 "type": "websocket.accept"
# #             }
# #         ))
# #         await asyncio.sleep(20)
# #         await self.send({
# #             "type": "websocket.close"
# #         })

# #     async def websocket_receive(self, event):
# #         print("receive", event)

# #     async def websocket_disconnect(self, event):
# #         print("disconnected", event)


# # class Send_Delivery_Order(AsyncConsumer):
# #     async def websocket_connect(self, event):
# #         print("connected", event)
# #         await self.send((
# #             {
# #                 "type": "websocket.accept"
# #             }
# #         ))
# #         await asyncio.sleep(20)
# #         await self.send({
# #             "type": "websocket.close"
# #         })

# #     async def websocket_receive(self, event):
# #         print("receive", event)

# #     async def websocket_disconnect(self, event):
# #         print("disconnected", event)


# # class order_delivered(AsyncConsumer):
# #     async def websocket_connect(self, event):
# #         print("connected", event)
# #         await self.send((
# #             {
# #                 "type": "websocket.accept"
# #             }
# #         ))
# #         await asyncio.sleep(20)
# #         await self.send({
# #             "type": "websocket.close"
# #         })

# #     async def websocket_receive(self, event):
# #         print("receive", event)

# #     async def websocket_disconnect(self, event):
# #         print("disconnected", event)


# # class reached_vendor(AsyncConsumer):
# #     async def websocket_connect(self, event):
# #         print("connected", event)
# #         await self.send((
# #             {
# #                 "type": "websocket.accept"
# #             }
# #         ))
# #         await asyncio.sleep(20)
# #         await self.send({
# #             "type": "websocket.close"
# #         })

# #     async def websocket_receive(self, event):
# #         print("receive", event)

# #     async def websocket_disconnect(self, event):
# #         print("disconnected", event)


# # class reached_checkpoint(AsyncConsumer):
# #     async def websocket_connect(self, event):
# #         print("connected", event)
# #         await self.send((
# #             {
# #                 "type": "websocket.accept"
# #             }
# #         ))
# #         await asyncio.sleep(20)
# #         await self.send({
# #             "type": "websocket.close"
# #         })

# #     async def websocket_receive(self, event):
# #         print("receive", event)

# #     async def websocket_disconnect(self, event):
# #         print("disconnected", event)


# # class order_pickedup(AsyncConsumer):
# #     async def websocket_connect(self, event):
# #         print("connected", event)
# #         await self.send((
# #             {
# #                 "type": "websocket.accept"
# #             }
# #         ))
# #         await asyncio.sleep(20)
# #         me = self.scope['user']

# #     async def websocket_receive(self, event):
# #         user = self.scope['user']
# #         data = {
# #             'order_id': event.get('order_id', None),
# #             'user': user
# #             'status': 'pickedup'
# #         }
# #         print("receive", event)
# #         await self.send({
# #             "type": "websocket.send"
# #             "text": json.dumps(data)
# #         })

# #     async def chat_message(self, event):
# #         await self.send({
# #             "type": "websocket.send",
# #             "text": event['message']
# #         })

# #     async def websocket_disconnect(self, event):
# #         print("disconnected", event)


# # class Send_Delivery_Order(AsyncConsumer):
# #     async def websocket_connect(self, event):
# #         print("connected", event)
# #         await self.send((
# #             {
# #                 "type": "websocket.accept"
# #             }
# #         ))
# #         await asyncio.sleep(20)
# #         await self.send({
# #             "type": "websocket.close"
# #         })

# #     async def websocket_receive(self, event):
# #         print("receive", event)

# #     async def websocket_disconnect(self, event):
# #         print("disconnected", event)
