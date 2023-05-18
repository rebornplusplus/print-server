import hashlib
import os.path

import weasyprint

from django.conf import settings
from django.template.loader import get_template


def generate_html_for_print(content, template_path):
    content = content.replace("\t", "    ").split("\n")
    template = get_template(template_path)
    html = template.render(context={
        "PROJECT_TITLE": settings.PROJECT_TITLE,
        "print_contents": content,
    })
    return html


def generate_weasyprint_doc(content, template_path, css_path="", top_left_header=""):
    html = generate_html_for_print(content, template_path)
    html_obj = weasyprint.HTML(string=html)
    #
    if css_path == "":
        css_obj = None
    else:
        css_obj = weasyprint.CSS(os.path.join("static/", css_path))
    team_name_css = weasyprint.CSS(string="@page { @top-left { content: \"" + top_left_header + "\" } }")
    #
    pdf = html_obj.render(stylesheets=[css_obj, team_name_css])
    file_name = ""
    if settings.KEEP_PDF:
        file_name = hashlib.sha256(content.encode()).hexdigest() + ".pdf"
        pdf.write_pdf(target=settings.MEDIA_ROOT + "/" + file_name)
    #
    return len(pdf.pages), file_name


def generate_pdf(content, user):
    return generate_weasyprint_doc(
        content=content,
        template_path="prints/print-details.html",
        css_path="css/magic.css",
        top_left_header=user.get_full_name()
    )
