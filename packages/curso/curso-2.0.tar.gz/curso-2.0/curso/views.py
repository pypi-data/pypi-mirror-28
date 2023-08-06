from djangoApiDec.djangoApiDec import queryString_required
from django.http import JsonResponse
from .apps import SearchOb

sob = SearchOb()
# Create your views here.
@queryString_required(['keyword', 'school'])
def search(request):
	keyword = request.GET['keyword']
	school = request.GET['school']
				
	return JsonResponse(sob.search(), safe=False)