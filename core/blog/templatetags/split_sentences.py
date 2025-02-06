from django import template

register = template.Library()


@register.filter
def split_sentences(value, num_sentences):
    sentences = value.split(". ")
    first_part = ". ".join(sentences[:num_sentences]) + "."
    second_part = ". ".join(sentences[num_sentences:])
    return first_part, second_part
