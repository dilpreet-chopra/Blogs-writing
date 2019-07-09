from django.shortcuts import redirect
from django.contrib.auth import logout

class StackOverflowMiddleware(object):
	def __init__(self, get_response):
		self.get_response = get_response

		
	def __call__(self, request):
		if request.get_full_path() == '/admin/logout/':	
			logout(request)

		return self.get_response(request)  
		  
	
