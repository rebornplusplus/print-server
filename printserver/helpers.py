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
    return html_obj.render(stylesheets=[css_obj, team_name_css])
