import logging
logger = logging.getLogger(__name__)

from ipware.ip import get_real_ip

from ct_useragents.forms import add_visit

	

def log_user_agent(request):
	user_agent = request.META.get('HTTP_USER_AGENT', '')
	ip = get_real_ip(request)
	if ip == None:
		ip = 'No IP Info'
	path = request.path
	content_type = request.content_type
	method = request.method
	encoding = request.encoding
	if hasattr(request, 'user'):
		user = request.user.pk
	else:
		user=None
	print('log_user_agent user: {}'.format(user))
	add_visit(user_agent,path,ip,method,content_type,encoding,user=user)
	
		
		
class UserAgentsMiddleware(object):

    def __init__(self, get_response=None):
        if get_response is not None:
            self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        log_user_agent(request)
