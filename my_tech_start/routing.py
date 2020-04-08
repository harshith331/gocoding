# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.conf.urls import url
# from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
# from delivery_side.consumers import ChatConsumer
# from django.urls import re_path
# # import base_tech.routing

# # application = ProtocolTypeRouter({
# #     # (http->django views is added by default)
# #     'websocket': AuthMiddlewareStack(
# #         URLRouter(
# #             base_tech.routing.websocket_urlpatterns
# #         )
# #     ),
# # })


# application = ProtocolTypeRouter({
#     'websocket': AllowedHostsOriginValidator(
#         AuthMiddlewareStack(
#             URLRouter(
#                 [
#                     re_path(r'ws/chat/$', ChatConsumer),
#                     # url('delivery/pickedup/<int:phone>',
#                     #     views.order_pickedup, name='pickedup'),
#                 ]
#             )
#         )
#     )
# })
