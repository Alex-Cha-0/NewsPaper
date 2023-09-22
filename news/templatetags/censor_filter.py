from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    censor_list = [
        'дурак',
        'сука',
        'мразь',
        'Какашка',
    ]
    # value_list = value.split()
    # for censor_word in censor_list:
    #     for index, value_word in enumerate(value_list):
    #         if censor_word == value_word:
    #             value_word = censor_word[0] + (len(censor_word) - 2) * '*' + censor_word[-1]
    #             value_list[index] = value_word
    # return ' '.join(value_list)
    words = value.split()
    result = []
    for word in words:
        if word in censor_list:
            result.append(word[0] + "*" * (len(word) - 2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)
