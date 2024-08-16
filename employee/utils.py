from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.conf import settings


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')

    # Set up a link_callback function for xhtml2pdf to handle static files
    def link_callback(uri, rel):
        path = None
        if uri.startswith('/static/'):
            path = os.path.join(settings.BASE_DIR, 'static', uri.replace('/static/', ''))
        elif uri.startswith('/media/'):
            path = os.path.join(settings.MEDIA_ROOT, uri.replace('/media/', ''))
        if path and os.path.exists(path):
            return path
        return None


    pdf_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    if pdf_status.err:
        return HttpResponse('Some errors were encountered <pre>' + html + '</pre>')

    return response

