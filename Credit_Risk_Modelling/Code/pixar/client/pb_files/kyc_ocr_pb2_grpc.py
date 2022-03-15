# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import pd_files.kyc_ocr_pb2 as kyc__ocr__pb2


class ocr_serviceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetOcrDetails = channel.unary_unary(
        '/ocr_service/GetOcrDetails',
        request_serializer=kyc__ocr__pb2.kyc_ocr_request.SerializeToString,
        response_deserializer=kyc__ocr__pb2.kyc_ocr_response.FromString,
        )


class ocr_serviceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GetOcrDetails(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ocr_serviceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetOcrDetails': grpc.unary_unary_rpc_method_handler(
          servicer.GetOcrDetails,
          request_deserializer=kyc__ocr__pb2.kyc_ocr_request.FromString,
          response_serializer=kyc__ocr__pb2.kyc_ocr_response.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ocr_service', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
