""" Ninkasi template tag lib """

from datetime import date
import calendar
from django.template import Library
from django.template.loader import render_to_string
from django.template.exceptions import TemplateDoesNotExist
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.forms import models as model_forms
from markdown import markdown
from ninkasi.utils import get_model_name
from ninkasi.models.task import ScheduledTask
from ninkasi.models.step import StepLog
from ninkasi.views.base import InlineCreateView


register = Library()


@register.filter
def ctname(obj):

    return get_model_name(obj)


@register.filter
def fslabel(formset):

    """ Get the label from the verbose name plural option """

    return formset.model._meta.verbose_name_plural


@register.inclusion_tag('snippets/listing.html', takes_context=True)
def listing(context, title, items, create_url=None):

    """ Show object listing """

    context.update({'title': title,
                    'items': items,
                    'create_url': create_url})

    return context


@register.inclusion_tag('snippets/sublisting.html', takes_context=True)
def sublisting(context, title, items, submodel, fk_field=None):

    """ Show listing of items within object """

    context.update({'title': title,
                    'items': items,
                    'submodel': submodel})

    if fk_field:
        context.update({'extra_args': '?fk_field=%s' % fk_field})

    return context


@register.inclusion_tag('snippets/edit_action.html')
def edit_action(obj):

    model_name = get_model_name(obj)

    try:
        _url = reverse("edit_%s" % model_name, kwargs={'pk': obj.id})
    except NoReverseMatch:
        try:
            _url = reverse("edit", kwargs={'model': model_name, 'pk': obj.id})
        except NoReverseMatch:
            _url = obj.get_url('edit')

    return {'edit_url': _url}


@register.inclusion_tag('snippets/edit_action.html')
def inline_edit_action(obj, parent, extra_args=""):

    return {'edit_url': "%s%s" % (reverse("inline_edit", kwargs={
        'parent_pk': parent.id,
        'parent_model': get_model_name(parent),
        'pk': obj.id,
        'model': get_model_name(obj)}), extra_args)}


@register.inclusion_tag('snippets/add_action.html')
def add_action(model):

    model_name = model.__class__.__name__.lower()

    try:
        create_url = reverse("create_%s" % model_name)
    except NoReverseMatch:
        create_url = reverse("create", kwargs={'model': model_name})
    return {'create_url': create_url}


@register.inclusion_tag('snippets/add_action.html')
def inline_add_action(model_name, parent, extra_args=""):

    return {'create_url': "%s%s" % (reverse("inline_create", kwargs={
        'parent_pk': parent.id,
        'parent_model': get_model_name(parent),
        'model': model_name}), extra_args)
    }


@register.inclusion_tag('snippets/delete_action.html')
def delete_action(obj, extra_args=""):

    try:
        return {'delete_url': "%s%s" % (reverse("delete", kwargs={
            'model': get_model_name(obj),
            'pk': obj.id}), extra_args)}
    except NoReverseMatch:
        return {'delete_url': obj.get_url('delete')}


@register.inclusion_tag('snippets/delete_action.html')
def inline_delete_action(obj, parent, extra_args=""):

    """ Render delete link as inline action """

    return {'delete_url': "%s%s" % (
        reverse("inline_delete", kwargs={
            'pk': obj.id,
            'model': get_model_name(obj),
            'parent_pk': parent.id,
            'parent_model': get_model_name(parent)}),
        extra_args)}


@register.inclusion_tag('snippets/view_action.html')
def view_action(obj, extra_args=""):

    """ render link to detail view as action button """

    return {'url': f"{ detail_url(obj) }{ extra_args }"}


@register.inclusion_tag('snippets/path_detail.html')
def path_detail(path):

    """ Render the path as template """

    return {'path': path}


@register.filter
def detail_url(obj):

    """ The object may not have a view. Ask it's url in that case """

    try:
        return reverse('view',
                       kwargs={'model': get_model_name(obj), 'pk': obj.id})
    except NoReverseMatch:
        return obj.get_url('view')


@register.filter
def doc(model):

    """ Return object class docstring """

    return mark_safe(markdown(model.__class__.__doc__))


@register.filter
def get(iterable, idx):

    return iterable.get(idx, None)


@register.filter
def status_label(obj):

    if obj.status == 1:
        return ""

    try:
        return obj._meta.model.get_status_display(obj)
    except AttributeError:
        return None


@register.filter
def status_class(status):

    """ If status is not an int, always return info """

    try:
        if status == 1:
            return ""
        elif status == 6:
            return "success"
        elif status > 4 or status == -1:
            return "danger"
        else:
            return "warning"
    except TypeError:
        return "info"


@register.simple_tag
def byline(obj):

    try:
        return render_to_string("snippets/%s_byline.html" %
                                get_model_name(obj),
                                {'obj': obj})
    except BaseException:
        return ""


@register.filter
def push(obj1, obj2):

    """ Push second object to the stack and return """

    return obj1, obj2


@register.filter
def has_obj_perm(user_obj, perm):

    user, obj = user_obj

    if getattr(obj, "mode", None) == 'ro':
        return False

    # return user.has_perm("unicorn.%s_%s" % (perm, get_model_name(obj)))

    return True


@register.filter
def has_model_perm(user_model, perm):

    user, model = user_model

    # return user.has_perm("unicorn.%s_%s" % (perm, model))

    return True


@register.simple_tag
def icon(obj_or_model):

    """ Render the icom for the given model """

    if not isinstance(obj_or_model, str):
        model = get_model_name(obj_or_model)
    else:
        model = obj_or_model

    try:
        return render_to_string(f"snippets/icon/{ model }.html", {})
    except TemplateDoesNotExist:
        return ""


@register.simple_tag
def status(obj):

    try:
        return render_to_string("snippets/status/%s.html" %
                                get_model_name(obj),
                                {'obj': obj})
    except TemplateDoesNotExist:
        return ""


@register.filter
def txt2html(txt):

    return mark_safe(markdown(txt))


@register.simple_tag
def tasks(day, month, year):

    """ Get tasks for the given day """

    day = date(year, month, day)

    return ScheduledTask.objects.filter(date=day)


@register.filter
def month_name(month_number):

    """ Return the local month name from the given number """

    month_number = int(month_number)
    return calendar.month_name[month_number]


@register.inclusion_tag("snippets/logform.html", takes_context=True)
def step_logform(context, step):

    form = model_forms.modelform_factory(StepLog, fields=['start_time',
                                                          'step',
                                                          'end_time'])

    form = form(initial={'step': step.id})

    form.fields['step'].widget = form.fields['step'].hidden_widget()

    context.update({'step': step, 'form': form})

    return context


@register.filter
def url_is_remote(url):

    """ Poor man's implementation of the remote check """

    return url.startswith("http")


@register.inclusion_tag("snippets/priority.html", takes_context=False)
def priority(_task):

    """ Render snippet for task priority """

    return {'task': _task}


@register.inclusion_tag("snippets/task.html", takes_context=False)
def task(_task):

    """ Render snippet for task """

    return {'task': _task}
