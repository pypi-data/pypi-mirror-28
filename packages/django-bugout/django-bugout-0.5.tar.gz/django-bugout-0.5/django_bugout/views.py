from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.test import Client
# from utils.client import Client
from django.core.urlresolvers import reverse
from django.views import debug
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext
import json

@login_required
def bugout(request):
    if request.method=='POST':
        uri=request.POST.get('parse_uri')
        method=request.POST.get('parse_method', 'GET')
        data=request.POST.get('parse_data', '{}')
        post_contenttype=request.POST.get('post_contenttype', '')
        render_method=request.POST.get('render_method', 'orinal')


        c = Client()
        user=request.user
        # c.login(username='cjssupport_evn', password='o3Yw4gJxAUXC')
        # c.login(username='cjs_genco3@cjs.vn', password='VBSaj9YVsP5v')
        # https://docs.djangoproject.com/en/2.0/topics/testing/tools/#django.test.Client.force_login
        c.force_login(request.user)
        # response = c.get(reverse('KPIWorkSheetDetail', kwargs={
        #     'kpi_id': 1410023}) + '?target_org=1333&follow_page=0&load_child=1&reload=1&level=1&has_child_loaded=0')
        from django.conf import settings
        settings.DEBUG = True
        settings.TEMPLATES_OPTION_DEBUG = True
        settings.TEMPLATES[0]["OPTIONS"]["debug"] = True
        # response = c.get(reverse('kpi_dashboard', kwargs={}))
        # 188987/?target_org=1&follow_page=1&load_child=1&reload=1&level=1&has_child_loaded=0
        # response = c.get(reverse('KPIWorkSheetDetail', kwargs={'kpi_id': 188987}) \
        #                  + '?target_org=1&follow_page=1&load_child=1&reload=1&level=1&has_child_loaded=0')
        # api_v2.profile
        # parse_html = True
        if render_method == 'text':
            def technical_500_response(request, exc_type, exc_value, tb, status_code=500):
                """
                Create a technical server error response. The last three arguments are
                the values returned from sys.exc_info() and friends.
                """
                reporter = debug.ExceptionReporter(request, exc_type, exc_value, tb)
                text = reporter.get_traceback_text()
                return HttpResponse(text, status=status_code, content_type='text/plain')

            debug.technical_500_response = technical_500_response

        elif render_method == 'html':
            def technical_500_response(request, exc_type, exc_value, tb, status_code=500):
                """
                Create a technical server error response. The last three arguments are
                the values returned from sys.exc_info() and friends.
                """
                reporter = debug.ExceptionReporter(request, exc_type, exc_value, tb)
                # duan add
                # if True or request.is_ajax():
                if False and request.is_ajax():
                    text = reporter.get_traceback_text()
                    return HttpResponse(text, status=status_code, content_type='text/plain')
                else:
                    html = reporter.get_traceback_html()
                    return HttpResponse(html, status=status_code, content_type='text/html')

            debug.technical_500_response = technical_500_response


        # if uri:
        #     response = c.get(uri)
        # else:
        #     response = c.get(reverse('api_v2.profile', kwargs={'user_id': 18}))
        # # response = c.get(reverse('api_v2.profile', kwargs={'user_id':18}), HTTP_X_REQUESTED_WITH='')

        if not uri:
            uri='/'

        if method == 'post':
            print data
            post_data = json.loads(data)
            if post_contenttype=='application/json':
                response=c.post(uri, json.dumps(post_data), content_type='application/json')
            else:
                response=c.post(uri, post_data)

        print response.status_code
        print response.content

        # return render(request, 'debug_wizard.html', {
        #     # 'user_organizations': user_organizations,
        #
        # })
        return response

    # else for any other request methods
    response = render_to_response('bugout.html', {}, context_instance=RequestContext(request))
    response.status_code = 200
    return response
