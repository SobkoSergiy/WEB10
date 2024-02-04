from django import template
from .. models import Author, Tag, Quote


register = template.Library()


def tags(quote_tags):
    return ', '.join([str(name) for name in quote_tags.all()])


def get_tags(quote):
    qtags = []
    for name in quote.all():
        qtags.append(str(name))
    return qtags


register.filter('qtags', get_tags)
register.filter('tags', tags)
# register.filter('search_tag', search_tag)
