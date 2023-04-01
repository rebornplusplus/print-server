from django.template import Library

register = Library()


@register.inclusion_tag("tags/basic_form.html")
def basic_form(form, **kwargs):
    return {
        'button_text': kwargs.get('button_text', 'Submit'),
        'force_save': kwargs.get('force_save', None),
        'form': form,
        'action': kwargs.get('action', '.'),
        'method': kwargs.get('method', 'POST'),
        'cancel_url': kwargs.get('cancel_url', None),
        'id': kwargs.get('id', '')
    }


@register.inclusion_tag("tags/basic_form_headless.html")
def basic_form_headless(form, **kwargs):
    return {
        'form': form,
        'action': kwargs.get('action', '.'),
        'method': kwargs.get('method', 'POST'),
        'cancel_url': kwargs.get('cancel_url', None),
        'id': kwargs.get('id', '')
    }


@register.inclusion_tag("tags/form_error.html")
def form_error(form, **kwargs):
    return {
        'form': form,
    }
