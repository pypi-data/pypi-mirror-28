# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bakerstreet/bakerstreet.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='bakerstreet/bakerstreet.proto',
  package='com.appknox.bakerstreet',
  syntax='proto3',
  serialized_pb=_b('\n\x1d\x62\x61kerstreet/bakerstreet.proto\x12\x17\x63om.appknox.bakerstreet\"\x17\n\x07Message\x12\x0c\n\x04\x44\x61ta\x18\x01 \x01(\t\"1\n\x04\x41pps\x12)\n\x03\x41pp\x18\x01 \x03(\x0b\x32\x1c.com.appknox.bakerstreet.App\"\x13\n\x03\x41pp\x12\x0c\n\x04Name\x18\x01 \x01(\t\"S\n\x06\x44\x65vice\x12\x0c\n\x04Uuid\x18\x01 \x01(\t\x12\x10\n\x08IsTablet\x18\x02 \x01(\x08\x12\x10\n\x08Platform\x18\x03 \x01(\x05\x12\x17\n\x0fPlatformVersion\x18\x04 \x01(\t\"-\n\x07\x46inding\x12\r\n\x05Title\x18\x01 \x01(\t\x12\x13\n\x0b\x44\x65scription\x18\x02 \x01(\t\"\x19\n\nInstallReq\x12\x0b\n\x03URL\x18\x01 \x01(\t\"9\n\x0e\x43onfigProxyReq\x12\n\n\x02IP\x18\x01 \x01(\t\x12\x0c\n\x04Port\x18\x02 \x01(\t\x12\r\n\x05Hosts\x18\x03 \x03(\t\"\x07\n\x05\x45mpty2\xb6\x06\n\x08Moriarty\x12J\n\x04\x45\x63ho\x12 .com.appknox.bakerstreet.Message\x1a .com.appknox.bakerstreet.Message\x12K\n\tLaunchApp\x12\x1c.com.appknox.bakerstreet.App\x1a .com.appknox.bakerstreet.Message\x12N\n\nClearProxy\x12\x1e.com.appknox.bakerstreet.Empty\x1a .com.appknox.bakerstreet.Message\x12O\n\x0bHealthCheck\x12\x1e.com.appknox.bakerstreet.Empty\x1a .com.appknox.bakerstreet.Message\x12O\n\rRemovePackage\x12\x1c.com.appknox.bakerstreet.App\x1a .com.appknox.bakerstreet.Message\x12W\n\x0eInstallPackage\x12#.com.appknox.bakerstreet.InstallReq\x1a .com.appknox.bakerstreet.Message\x12[\n\x0e\x43onfigureProxy\x12\'.com.appknox.bakerstreet.ConfigProxyReq\x1a .com.appknox.bakerstreet.Message\x12Q\n\x0f\x43onfigureGadget\x12\x1c.com.appknox.bakerstreet.App\x1a .com.appknox.bakerstreet.Message\x12G\n\x04Info\x12\x1e.com.appknox.bakerstreet.Empty\x1a\x1f.com.appknox.bakerstreet.Device\x12M\n\x0cListPackages\x12\x1e.com.appknox.bakerstreet.Empty\x1a\x1d.com.appknox.bakerstreet.Appsb\x06proto3')
)




_MESSAGE = _descriptor.Descriptor(
  name='Message',
  full_name='com.appknox.bakerstreet.Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='Data', full_name='com.appknox.bakerstreet.Message.Data', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=58,
  serialized_end=81,
)


_APPS = _descriptor.Descriptor(
  name='Apps',
  full_name='com.appknox.bakerstreet.Apps',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='App', full_name='com.appknox.bakerstreet.Apps.App', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=83,
  serialized_end=132,
)


_APP = _descriptor.Descriptor(
  name='App',
  full_name='com.appknox.bakerstreet.App',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='Name', full_name='com.appknox.bakerstreet.App.Name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=134,
  serialized_end=153,
)


_DEVICE = _descriptor.Descriptor(
  name='Device',
  full_name='com.appknox.bakerstreet.Device',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='Uuid', full_name='com.appknox.bakerstreet.Device.Uuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='IsTablet', full_name='com.appknox.bakerstreet.Device.IsTablet', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='Platform', full_name='com.appknox.bakerstreet.Device.Platform', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='PlatformVersion', full_name='com.appknox.bakerstreet.Device.PlatformVersion', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=155,
  serialized_end=238,
)


_FINDING = _descriptor.Descriptor(
  name='Finding',
  full_name='com.appknox.bakerstreet.Finding',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='Title', full_name='com.appknox.bakerstreet.Finding.Title', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='Description', full_name='com.appknox.bakerstreet.Finding.Description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=240,
  serialized_end=285,
)


_INSTALLREQ = _descriptor.Descriptor(
  name='InstallReq',
  full_name='com.appknox.bakerstreet.InstallReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='URL', full_name='com.appknox.bakerstreet.InstallReq.URL', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=287,
  serialized_end=312,
)


_CONFIGPROXYREQ = _descriptor.Descriptor(
  name='ConfigProxyReq',
  full_name='com.appknox.bakerstreet.ConfigProxyReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='IP', full_name='com.appknox.bakerstreet.ConfigProxyReq.IP', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='Port', full_name='com.appknox.bakerstreet.ConfigProxyReq.Port', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='Hosts', full_name='com.appknox.bakerstreet.ConfigProxyReq.Hosts', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=314,
  serialized_end=371,
)


_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='com.appknox.bakerstreet.Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=373,
  serialized_end=380,
)

_APPS.fields_by_name['App'].message_type = _APP
DESCRIPTOR.message_types_by_name['Message'] = _MESSAGE
DESCRIPTOR.message_types_by_name['Apps'] = _APPS
DESCRIPTOR.message_types_by_name['App'] = _APP
DESCRIPTOR.message_types_by_name['Device'] = _DEVICE
DESCRIPTOR.message_types_by_name['Finding'] = _FINDING
DESCRIPTOR.message_types_by_name['InstallReq'] = _INSTALLREQ
DESCRIPTOR.message_types_by_name['ConfigProxyReq'] = _CONFIGPROXYREQ
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), dict(
  DESCRIPTOR = _MESSAGE,
  __module__ = 'bakerstreet.bakerstreet_pb2'
  # @@protoc_insertion_point(class_scope:com.appknox.bakerstreet.Message)
  ))
_sym_db.RegisterMessage(Message)

Apps = _reflection.GeneratedProtocolMessageType('Apps', (_message.Message,), dict(
  DESCRIPTOR = _APPS,
  __module__ = 'bakerstreet.bakerstreet_pb2'
  # @@protoc_insertion_point(class_scope:com.appknox.bakerstreet.Apps)
  ))
_sym_db.RegisterMessage(Apps)

App = _reflection.GeneratedProtocolMessageType('App', (_message.Message,), dict(
  DESCRIPTOR = _APP,
  __module__ = 'bakerstreet.bakerstreet_pb2'
  # @@protoc_insertion_point(class_scope:com.appknox.bakerstreet.App)
  ))
_sym_db.RegisterMessage(App)

Device = _reflection.GeneratedProtocolMessageType('Device', (_message.Message,), dict(
  DESCRIPTOR = _DEVICE,
  __module__ = 'bakerstreet.bakerstreet_pb2'
  # @@protoc_insertion_point(class_scope:com.appknox.bakerstreet.Device)
  ))
_sym_db.RegisterMessage(Device)

Finding = _reflection.GeneratedProtocolMessageType('Finding', (_message.Message,), dict(
  DESCRIPTOR = _FINDING,
  __module__ = 'bakerstreet.bakerstreet_pb2'
  # @@protoc_insertion_point(class_scope:com.appknox.bakerstreet.Finding)
  ))
_sym_db.RegisterMessage(Finding)

InstallReq = _reflection.GeneratedProtocolMessageType('InstallReq', (_message.Message,), dict(
  DESCRIPTOR = _INSTALLREQ,
  __module__ = 'bakerstreet.bakerstreet_pb2'
  # @@protoc_insertion_point(class_scope:com.appknox.bakerstreet.InstallReq)
  ))
_sym_db.RegisterMessage(InstallReq)

ConfigProxyReq = _reflection.GeneratedProtocolMessageType('ConfigProxyReq', (_message.Message,), dict(
  DESCRIPTOR = _CONFIGPROXYREQ,
  __module__ = 'bakerstreet.bakerstreet_pb2'
  # @@protoc_insertion_point(class_scope:com.appknox.bakerstreet.ConfigProxyReq)
  ))
_sym_db.RegisterMessage(ConfigProxyReq)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), dict(
  DESCRIPTOR = _EMPTY,
  __module__ = 'bakerstreet.bakerstreet_pb2'
  # @@protoc_insertion_point(class_scope:com.appknox.bakerstreet.Empty)
  ))
_sym_db.RegisterMessage(Empty)


try:
  # THESE ELEMENTS WILL BE DEPRECATED.
  # Please use the generated *_pb2_grpc.py files instead.
  import grpc
  from grpc.beta import implementations as beta_implementations
  from grpc.beta import interfaces as beta_interfaces
  from grpc.framework.common import cardinality
  from grpc.framework.interfaces.face import utilities as face_utilities


  class MoriartyStub(object):
    # missing associated documentation comment in .proto file
    pass

    def __init__(self, channel):
      """Constructor.

      Args:
        channel: A grpc.Channel.
      """
      self.Echo = channel.unary_unary(
          '/com.appknox.bakerstreet.Moriarty/Echo',
          request_serializer=Message.SerializeToString,
          response_deserializer=Message.FromString,
          )
      self.LaunchApp = channel.unary_unary(
          '/com.appknox.bakerstreet.Moriarty/LaunchApp',
          request_serializer=App.SerializeToString,
          response_deserializer=Message.FromString,
          )
      self.ClearProxy = channel.unary_unary(
          '/com.appknox.bakerstreet.Moriarty/ClearProxy',
          request_serializer=Empty.SerializeToString,
          response_deserializer=Message.FromString,
          )
      self.HealthCheck = channel.unary_unary(
          '/com.appknox.bakerstreet.Moriarty/HealthCheck',
          request_serializer=Empty.SerializeToString,
          response_deserializer=Message.FromString,
          )
      self.RemovePackage = channel.unary_unary(
          '/com.appknox.bakerstreet.Moriarty/RemovePackage',
          request_serializer=App.SerializeToString,
          response_deserializer=Message.FromString,
          )
      self.InstallPackage = channel.unary_unary(
          '/com.appknox.bakerstreet.Moriarty/InstallPackage',
          request_serializer=InstallReq.SerializeToString,
          response_deserializer=Message.FromString,
          )
      self.ConfigureProxy = channel.unary_unary(
          '/com.appknox.bakerstreet.Moriarty/ConfigureProxy',
          request_serializer=ConfigProxyReq.SerializeToString,
          response_deserializer=Message.FromString,
          )
      self.ConfigureGadget = channel.unary_unary(
          '/com.appknox.bakerstreet.Moriarty/ConfigureGadget',
          request_serializer=App.SerializeToString,
          response_deserializer=Message.FromString,
          )
      self.Info = channel.unary_unary(
          '/com.appknox.bakerstreet.Moriarty/Info',
          request_serializer=Empty.SerializeToString,
          response_deserializer=Device.FromString,
          )
      self.ListPackages = channel.unary_unary(
          '/com.appknox.bakerstreet.Moriarty/ListPackages',
          request_serializer=Empty.SerializeToString,
          response_deserializer=Apps.FromString,
          )


  class MoriartyServicer(object):
    # missing associated documentation comment in .proto file
    pass

    def Echo(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.set_code(grpc.StatusCode.UNIMPLEMENTED)
      context.set_details('Method not implemented!')
      raise NotImplementedError('Method not implemented!')

    def LaunchApp(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.set_code(grpc.StatusCode.UNIMPLEMENTED)
      context.set_details('Method not implemented!')
      raise NotImplementedError('Method not implemented!')

    def ClearProxy(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.set_code(grpc.StatusCode.UNIMPLEMENTED)
      context.set_details('Method not implemented!')
      raise NotImplementedError('Method not implemented!')

    def HealthCheck(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.set_code(grpc.StatusCode.UNIMPLEMENTED)
      context.set_details('Method not implemented!')
      raise NotImplementedError('Method not implemented!')

    def RemovePackage(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.set_code(grpc.StatusCode.UNIMPLEMENTED)
      context.set_details('Method not implemented!')
      raise NotImplementedError('Method not implemented!')

    def InstallPackage(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.set_code(grpc.StatusCode.UNIMPLEMENTED)
      context.set_details('Method not implemented!')
      raise NotImplementedError('Method not implemented!')

    def ConfigureProxy(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.set_code(grpc.StatusCode.UNIMPLEMENTED)
      context.set_details('Method not implemented!')
      raise NotImplementedError('Method not implemented!')

    def ConfigureGadget(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.set_code(grpc.StatusCode.UNIMPLEMENTED)
      context.set_details('Method not implemented!')
      raise NotImplementedError('Method not implemented!')

    def Info(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.set_code(grpc.StatusCode.UNIMPLEMENTED)
      context.set_details('Method not implemented!')
      raise NotImplementedError('Method not implemented!')

    def ListPackages(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.set_code(grpc.StatusCode.UNIMPLEMENTED)
      context.set_details('Method not implemented!')
      raise NotImplementedError('Method not implemented!')


  def add_MoriartyServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'Echo': grpc.unary_unary_rpc_method_handler(
            servicer.Echo,
            request_deserializer=Message.FromString,
            response_serializer=Message.SerializeToString,
        ),
        'LaunchApp': grpc.unary_unary_rpc_method_handler(
            servicer.LaunchApp,
            request_deserializer=App.FromString,
            response_serializer=Message.SerializeToString,
        ),
        'ClearProxy': grpc.unary_unary_rpc_method_handler(
            servicer.ClearProxy,
            request_deserializer=Empty.FromString,
            response_serializer=Message.SerializeToString,
        ),
        'HealthCheck': grpc.unary_unary_rpc_method_handler(
            servicer.HealthCheck,
            request_deserializer=Empty.FromString,
            response_serializer=Message.SerializeToString,
        ),
        'RemovePackage': grpc.unary_unary_rpc_method_handler(
            servicer.RemovePackage,
            request_deserializer=App.FromString,
            response_serializer=Message.SerializeToString,
        ),
        'InstallPackage': grpc.unary_unary_rpc_method_handler(
            servicer.InstallPackage,
            request_deserializer=InstallReq.FromString,
            response_serializer=Message.SerializeToString,
        ),
        'ConfigureProxy': grpc.unary_unary_rpc_method_handler(
            servicer.ConfigureProxy,
            request_deserializer=ConfigProxyReq.FromString,
            response_serializer=Message.SerializeToString,
        ),
        'ConfigureGadget': grpc.unary_unary_rpc_method_handler(
            servicer.ConfigureGadget,
            request_deserializer=App.FromString,
            response_serializer=Message.SerializeToString,
        ),
        'Info': grpc.unary_unary_rpc_method_handler(
            servicer.Info,
            request_deserializer=Empty.FromString,
            response_serializer=Device.SerializeToString,
        ),
        'ListPackages': grpc.unary_unary_rpc_method_handler(
            servicer.ListPackages,
            request_deserializer=Empty.FromString,
            response_serializer=Apps.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'com.appknox.bakerstreet.Moriarty', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


  class BetaMoriartyServicer(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    # missing associated documentation comment in .proto file
    pass
    def Echo(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def LaunchApp(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def ClearProxy(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def HealthCheck(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def RemovePackage(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def InstallPackage(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def ConfigureProxy(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def ConfigureGadget(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def Info(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def ListPackages(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)


  class BetaMoriartyStub(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    # missing associated documentation comment in .proto file
    pass
    def Echo(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      # missing associated documentation comment in .proto file
      pass
      raise NotImplementedError()
    Echo.future = None
    def LaunchApp(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      # missing associated documentation comment in .proto file
      pass
      raise NotImplementedError()
    LaunchApp.future = None
    def ClearProxy(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      # missing associated documentation comment in .proto file
      pass
      raise NotImplementedError()
    ClearProxy.future = None
    def HealthCheck(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      # missing associated documentation comment in .proto file
      pass
      raise NotImplementedError()
    HealthCheck.future = None
    def RemovePackage(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      # missing associated documentation comment in .proto file
      pass
      raise NotImplementedError()
    RemovePackage.future = None
    def InstallPackage(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      # missing associated documentation comment in .proto file
      pass
      raise NotImplementedError()
    InstallPackage.future = None
    def ConfigureProxy(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      # missing associated documentation comment in .proto file
      pass
      raise NotImplementedError()
    ConfigureProxy.future = None
    def ConfigureGadget(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      # missing associated documentation comment in .proto file
      pass
      raise NotImplementedError()
    ConfigureGadget.future = None
    def Info(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      # missing associated documentation comment in .proto file
      pass
      raise NotImplementedError()
    Info.future = None
    def ListPackages(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      # missing associated documentation comment in .proto file
      pass
      raise NotImplementedError()
    ListPackages.future = None


  def beta_create_Moriarty_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_deserializers = {
      ('com.appknox.bakerstreet.Moriarty', 'ClearProxy'): Empty.FromString,
      ('com.appknox.bakerstreet.Moriarty', 'ConfigureGadget'): App.FromString,
      ('com.appknox.bakerstreet.Moriarty', 'ConfigureProxy'): ConfigProxyReq.FromString,
      ('com.appknox.bakerstreet.Moriarty', 'Echo'): Message.FromString,
      ('com.appknox.bakerstreet.Moriarty', 'HealthCheck'): Empty.FromString,
      ('com.appknox.bakerstreet.Moriarty', 'Info'): Empty.FromString,
      ('com.appknox.bakerstreet.Moriarty', 'InstallPackage'): InstallReq.FromString,
      ('com.appknox.bakerstreet.Moriarty', 'LaunchApp'): App.FromString,
      ('com.appknox.bakerstreet.Moriarty', 'ListPackages'): Empty.FromString,
      ('com.appknox.bakerstreet.Moriarty', 'RemovePackage'): App.FromString,
    }
    response_serializers = {
      ('com.appknox.bakerstreet.Moriarty', 'ClearProxy'): Message.SerializeToString,
      ('com.appknox.bakerstreet.Moriarty', 'ConfigureGadget'): Message.SerializeToString,
      ('com.appknox.bakerstreet.Moriarty', 'ConfigureProxy'): Message.SerializeToString,
      ('com.appknox.bakerstreet.Moriarty', 'Echo'): Message.SerializeToString,
      ('com.appknox.bakerstreet.Moriarty', 'HealthCheck'): Message.SerializeToString,
      ('com.appknox.bakerstreet.Moriarty', 'Info'): Device.SerializeToString,
      ('com.appknox.bakerstreet.Moriarty', 'InstallPackage'): Message.SerializeToString,
      ('com.appknox.bakerstreet.Moriarty', 'LaunchApp'): Message.SerializeToString,
      ('com.appknox.bakerstreet.Moriarty', 'ListPackages'): Apps.SerializeToString,
      ('com.appknox.bakerstreet.Moriarty', 'RemovePackage'): Message.SerializeToString,
    }
    method_implementations = {
      ('com.appknox.bakerstreet.Moriarty', 'ClearProxy'): face_utilities.unary_unary_inline(servicer.ClearProxy),
      ('com.appknox.bakerstreet.Moriarty', 'ConfigureGadget'): face_utilities.unary_unary_inline(servicer.ConfigureGadget),
      ('com.appknox.bakerstreet.Moriarty', 'ConfigureProxy'): face_utilities.unary_unary_inline(servicer.ConfigureProxy),
      ('com.appknox.bakerstreet.Moriarty', 'Echo'): face_utilities.unary_unary_inline(servicer.Echo),
      ('com.appknox.bakerstreet.Moriarty', 'HealthCheck'): face_utilities.unary_unary_inline(servicer.HealthCheck),
      ('com.appknox.bakerstreet.Moriarty', 'Info'): face_utilities.unary_unary_inline(servicer.Info),
      ('com.appknox.bakerstreet.Moriarty', 'InstallPackage'): face_utilities.unary_unary_inline(servicer.InstallPackage),
      ('com.appknox.bakerstreet.Moriarty', 'LaunchApp'): face_utilities.unary_unary_inline(servicer.LaunchApp),
      ('com.appknox.bakerstreet.Moriarty', 'ListPackages'): face_utilities.unary_unary_inline(servicer.ListPackages),
      ('com.appknox.bakerstreet.Moriarty', 'RemovePackage'): face_utilities.unary_unary_inline(servicer.RemovePackage),
    }
    server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
    return beta_implementations.server(method_implementations, options=server_options)


  def beta_create_Moriarty_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_serializers = {
      ('com.appknox.bakerstreet.Moriarty', 'ClearProxy'): Empty.SerializeToString,
      ('com.appknox.bakerstreet.Moriarty', 'ConfigureGadget'): App.SerializeToString,
      ('com.appknox.bakerstreet.Moriarty', 'ConfigureProxy'): ConfigProxyReq.SerializeToString,
      ('com.appknox.bakerstreet.Moriarty', 'Echo'): Message.SerializeToString,
      ('com.appknox.bakerstreet.Moriarty', 'HealthCheck'): Empty.SerializeToString,
      ('com.appknox.bakerstreet.Moriarty', 'Info'): Empty.SerializeToString,
      ('com.appknox.bakerstreet.Moriarty', 'InstallPackage'): InstallReq.SerializeToString,
      ('com.appknox.bakerstreet.Moriarty', 'LaunchApp'): App.SerializeToString,
      ('com.appknox.bakerstreet.Moriarty', 'ListPackages'): Empty.SerializeToString,
      ('com.appknox.bakerstreet.Moriarty', 'RemovePackage'): App.SerializeToString,
    }
    response_deserializers = {
      ('com.appknox.bakerstreet.Moriarty', 'ClearProxy'): Message.FromString,
      ('com.appknox.bakerstreet.Moriarty', 'ConfigureGadget'): Message.FromString,
      ('com.appknox.bakerstreet.Moriarty', 'ConfigureProxy'): Message.FromString,
      ('com.appknox.bakerstreet.Moriarty', 'Echo'): Message.FromString,
      ('com.appknox.bakerstreet.Moriarty', 'HealthCheck'): Message.FromString,
      ('com.appknox.bakerstreet.Moriarty', 'Info'): Device.FromString,
      ('com.appknox.bakerstreet.Moriarty', 'InstallPackage'): Message.FromString,
      ('com.appknox.bakerstreet.Moriarty', 'LaunchApp'): Message.FromString,
      ('com.appknox.bakerstreet.Moriarty', 'ListPackages'): Apps.FromString,
      ('com.appknox.bakerstreet.Moriarty', 'RemovePackage'): Message.FromString,
    }
    cardinalities = {
      'ClearProxy': cardinality.Cardinality.UNARY_UNARY,
      'ConfigureGadget': cardinality.Cardinality.UNARY_UNARY,
      'ConfigureProxy': cardinality.Cardinality.UNARY_UNARY,
      'Echo': cardinality.Cardinality.UNARY_UNARY,
      'HealthCheck': cardinality.Cardinality.UNARY_UNARY,
      'Info': cardinality.Cardinality.UNARY_UNARY,
      'InstallPackage': cardinality.Cardinality.UNARY_UNARY,
      'LaunchApp': cardinality.Cardinality.UNARY_UNARY,
      'ListPackages': cardinality.Cardinality.UNARY_UNARY,
      'RemovePackage': cardinality.Cardinality.UNARY_UNARY,
    }
    stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
    return beta_implementations.dynamic_stub(channel, 'com.appknox.bakerstreet.Moriarty', cardinalities, options=stub_options)
except ImportError:
  pass
# @@protoc_insertion_point(module_scope)
