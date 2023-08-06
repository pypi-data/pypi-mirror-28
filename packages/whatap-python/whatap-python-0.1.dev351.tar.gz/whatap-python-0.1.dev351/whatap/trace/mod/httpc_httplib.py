import traceback

from whatap.trace import UdpSession, PacketTypeEnum
from whatap.trace.mod.application_wsgi import transfer
from whatap.util.date_util import DateUtil
from whatap.trace.trace_context_manager import TraceContextManager


def instrument_httplib(module):
    def wrapper(fn):
        def trace(*args, **kwargs):
            ctx = TraceContextManager.getLocalContext()
            if not ctx or ctx.active_httpc_hash:
                return fn(*args, **kwargs)
    
            start_time = DateUtil.nowSystem()
            ctx.start_time = start_time
            ctx.httpc_url = args[1]
            ctx.active_httpc_hash = ctx.httpc_url

            kwargs['headers'] = transfer(ctx, kwargs.get('headers', {}))
            
            try:
                callback = fn(*args, **kwargs)
                return callback
            except Exception as e:
                errors = []
                errors.append(e.__class__.__name__)
                errors.append(str(e.args[0]))
                try:
                    errors.append(traceback.format_exc())
                except:
                    errors.append('')
                UdpSession.send_packet(PacketTypeEnum.PACKET_ERROR, ctx, errors)
                
                if not ctx.error:
                    ctx.error = 1
            finally:
                datas = [ctx.httpc_url, ctx.mcallee]
                ctx.elapsed = DateUtil.nowSystem() - start_time
                UdpSession.send_packet(PacketTypeEnum.PACKET_HTTPC, ctx, datas)
                
                ctx.active_httpc_hash = 0
                ctx.httpc_url = None
        
        return trace
    
    module.HTTPConnection.request = wrapper(module.HTTPConnection.request)



def instrument_httplib2(module):
    def wrapper(fn):
        def trace(*args, **kwargs):
            ctx = TraceContextManager.getLocalContext()
            if not ctx or ctx.active_httpc_hash:
                return fn(*args, **kwargs)
            
            start_time = DateUtil.nowSystem()
            ctx.start_time = start_time
            ctx.httpc_url = args[1]
            ctx.active_httpc_hash = ctx.httpc_url
            
            kwargs['headers'] = transfer(ctx, kwargs.get('headers', {}))
            
            try:
                callback = fn(*args, **kwargs)
                return callback
            except Exception as e:
                ctx.error_step = e
                if not ctx.error:
                    ctx.error = 1
                    
                errors = []
                errors.append(e.__class__.__name__)
                errors.append(str(e.args[0]))
                try:
                    errors.append(traceback.format_exc())
                except:
                    errors.append('')
                UdpSession.send_packet(PacketTypeEnum.PACKET_ERROR, ctx, errors)
                
            finally:
                datas = [ctx.httpc_url, ctx.mcallee]
                ctx.elapsed = DateUtil.nowSystem() - start_time
                UdpSession.send_packet(PacketTypeEnum.PACKET_HTTPC, ctx, datas)
                
                ctx.active_httpc_hash = 0
                ctx.httpc_url = None
        
        return trace
    
    module.Http.request = wrapper(module.Http.request)
