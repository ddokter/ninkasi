from datetime import datetime
from django.template import Library
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.safestring import mark_safe
from django.utils import timezone
from markdown import markdown
from ninkasi.utils import get_model_name


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
        _url = reverse("edit", kwargs={'model': model_name, 'pk': obj.id})
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

    return {'delete_url': "%s%s" % (reverse("delete", kwargs={
        'model': get_model_name(obj),
        'pk': obj.id}), extra_args)}


@register.inclusion_tag('snippets/delete_action.html')
def inline_delete_action(obj, parent, extra_args=""):

    return {'delete_url': "%s%s" % (
        reverse("inline_delete", kwargs={
            'pk': obj.id,
            'model': get_model_name(obj),
            'parent_pk': parent.id,
            'parent_model': get_model_name(parent)}),
        extra_args)}


@register.inclusion_tag('snippets/path_detail.html')
def path_detail(path):

    return {'path': path}


@register.filter
def detail_url(obj):

    return reverse('view', kwargs={'model': get_model_name(obj), 'pk': obj.id})


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
    except:
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
    except:
        return "info"


@register.simple_tag
def byline(obj):

    try:
        return render_to_string("snippets/%s_byline.html" %
                                get_model_name(obj),
                                {'obj': obj})
    except:
        return ""


@register.filter
def push(obj1, obj2):

    """ Push second object to the stack and return """

    return obj1, obj2


@register.filter
def has_obj_perm(user_obj, perm):

    user, obj = user_obj

    # return user.has_perm("unicorn.%s_%s" % (perm, get_model_name(obj)))

    return True


@register.filter
def has_model_perm(user_model, perm):

    user, model = user_model

    # return user.has_perm("unicorn.%s_%s" % (perm, model))

    return True


@register.simple_tag
def icon(obj_or_model):

    if hasattr(obj_or_model, "_meta"):
        model = get_model_name(obj_or_model)
    else:
        model = obj_or_model
    
    try:
        return render_to_string(f"snippets/icon/{ model }.html", {})
    except:
        return ""


@register.simple_tag
def status(obj):

    try:
        return render_to_string("snippets/status/%s.html" %
                                get_model_name(obj),
                                {'obj': obj})
    except:
        return ""


@register.filter
def txt2html(txt):

    return mark_safe(markdown(txt))


@register.simple_tag
def tankcontent(tank, day, month, year):

    """ Provide tank availability """

    batch = tank.content(datetime(year, month, day,
                                  tzinfo=timezone.get_current_timezone()))

    if batch:
        return batch.get_color()

    return ""


@register.simple_tag
def brewhousecontent(brewhouse, day, month, year):

    """ Provide tank availability """

    brew = brewhouse.content(datetime(year, month, day,
                                      tzinfo=timezone.get_current_timezone()))

    if brew:

        return brew.batch.color

    return ""
