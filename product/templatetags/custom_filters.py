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

