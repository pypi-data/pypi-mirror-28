import traceback

from whatap.trace import UdpSession, PacketTypeEnum
from whatap.trace.mod.application_wsgi import transfer
from whatap.util.date_util import DateUtil
from whatap.trace.trace_context_manager import TraceContextManager


def instrument_requests(module):
    def wrapper(fn):
        def trace(*args, **kwargs):
            ctx = TraceContextManager.getLocalContext()
            if not ctx or ctx.active_httpc_hash:
                return fn(*args, **kwargs)
    
            req = args[1]
            start_time = DateUtil.nowSystem()
            ctx.start_time = start_time
            ctx.httpc_url = req.url
            ctx.active_httpc_hash = ctx.httpc_url
            
            req.headers = transfer(ctx, req.headers)
            
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
    
    module.Session.send = wrapper(module.Session.send)

