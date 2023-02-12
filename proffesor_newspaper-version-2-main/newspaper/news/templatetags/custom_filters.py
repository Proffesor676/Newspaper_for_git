from django import template

register = template.Library()

@register.filter()
def censor(value):
    bad_words = ('попа', 'свекла', 'автомобиле', 'свеклу')
    if not isinstance(value, str):
        raise TypeError(f'Непонятный тип данных {type(value)}, ожидаемый тип str')

    for bad_word in value.split():
        if bad_word.lower() in bad_words:
            value = value.replace(bad_word, f'{bad_word[0]}{"*" *(len(bad_word)-1)}')
    return value
