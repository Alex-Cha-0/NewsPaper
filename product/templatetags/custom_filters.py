from django import template

register = template.Library()  # если мы не зарегестрируем наши фильтры, то django никогда не узнает где именно их искать и фильтры потеряются :(


@register.filter(name='multiply')
def multiply(value, arg):
    if isinstance(value, str) and isinstance(arg,
                                             int):  # проверяем, что value -- это точно строка, а arg -- точно число, чтобы не возникло курьёзов
        return str(value) * arg
    else:
        raise ValueError(
            f'Нельзя умножить {type(value)} на {type(arg)}')  # в случае, если кто-то неправильно воспользовался нашим тегом, выводим ошибку


@register.filter(name='censor')
def censor(value):
    censor_list = [
        'дурак',
        'сука',
        'мразь',
        'Какашка',
    ]
    value_list = value.split()
    for censor_word in censor_list:
        for index, value_word in enumerate(value_list):
            if censor_word == value_word:
                value_word = censor_word[0] + (len(censor_word) - 2) * '*' + censor_word[-1]
                value_list[index] = value_word

                print(censor_word, value_word)
    return ' '.join(value_list)
