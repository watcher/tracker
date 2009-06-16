from tracker.lib import response

def index(request):
	if request.method == "POST":
		pass
	else:
		pass
		
	return response(request, 'tracker/public/index.html')