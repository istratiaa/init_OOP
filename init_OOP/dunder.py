class Derivate:
    """В общем случае – это оператор вызова, например, так можно вызывать функции. Но, как видите, так можно
     вызывать и классы. В действительности, когда происходит вызов класса, то автоматически запускается
     магический метод __call__ и в данном случае он создает новый экземпляр этого класса
     c=Counter()
               |
               --> __call__(self, *args, **kwargs):
                        obj = self.__new__(self, *args, **kwargs)
                        self.__init__(obj, *args, **kwargs)
                        return obj
     Это очень упрощенная схема реализации метода __call__, в действительности, она несколько сложнее, но принцип
     тот же: сначала вызывается магический метод __new__ для создания самого объекта в памяти устройства, а затем,
     метод __init__ - для его инициализации. То есть, класс можно вызывать подобно функции благодаря встроенной
     для него реализации магического метода __call__.
     """

    def __init__(self, func):
        self.__fn = func

    def __call__(self, x, dx=0.0001, *args, **kwargs):
        return (self.__fn(x + dx) - self.__fn(x)) / dx


@Derivate
def df_sin(x):
    return math.sin(x)


# print(df_sin(math.pi / 4))


class Counter:
    """Благодаря добавлению этого магического метода в наш класс, теперь можно вызывать его экземпляры подобно функциям
    через оператор круглые скобки. Классы, экземпляры которых можно вызывать подобно функциям, получили название
    функторы"""

    def __init__(self):
        self.__counter = 0

    def __call__(self, *args, **kwargs):
        self.__counter += 1
        return self.__counter


c = Counter()
c2 = Counter()
c()
c()
res = c()
res2 = c2()


class Person:

    def __init__(self, name, last_name, age):
        self.__name = name
        self.age = age
        self.last_name = last_name

    def __setattr__(self, key, value):
        ''' через этот магический метод запретим создание локального свойства с именем vast_name.'''
        if isinstance(value, str):
            if value.lower() == "sasha":  # недопустимое значение value
                raise AttributeError("недопустимое значение атрибута")
        if key == 'vast_name':  # недопустимое имя key
            raise AttributeError("недопустимое имя атрибута")
        else:
            object.__setattr__(self, key, value)  # или self.__dict__[key] = value

    def __getattribute__(self, item):
        """Если идет обращение к приватному атрибуту по внешнему имени _Person__name, то генерируем исключение ValueError.
         И, действительно, после запуска программы видим отображение этой ошибки в консоли. Вот так, через магический
         метод __getattribute__ можно реализовывать определенную логику при обращении к атрибутам через экземпляр
         класса."""
        if item == '_Person__name':
            raise ValueError("Private attribute")
        return object.__getattribute__(self, item)

    def __getattr__(self, item):
        '''Следующий магический метод __getattr__ автоматически вызывается, если идет обращение к
        несуществующему атрибуту'''
        return False  # Например, нам необходимо определить класс, в котором при обращении к несуществующим
        # атрибутам возвращается значение False, а не генерируется исключение

    def __delattr__(self, item):
        '''Можно контролировать удаление тех или иных атрибутов из экземпляров класса'''
        if item in ("last_name", "age"):
            object.__delattr__(self, item)
        else:
            raise ValueError("Невозможно удалить данный атрибут")

    def __repr__(self):
        """  магический метод для отображения информации об объекте класса в режиме отладки (для разработчиков)"""
        return f"{self.__class__}: {self.last_name}"

    def __str__(self):
        """магический метод для отображения информации об объекте класса для пользователей
        (например, для функций print, str)"""
        return f"{self.last_name}"


class Point:
    def __init__(self, *args):
        self.__coords = args


    def __len__(self):
        """ позволяет применять функцию len() к экземплярам класса"""
        return len(self.__coords)

    def __abs__(self):
        """ позволяет применять функцию abs() к экземплярам класса"""
        return list(map(abs, self.__coords))



if __name__ == '__main__':
    per_vasya = Person('vasya', 'pupkov', 30)
    per_pasha = Person('pasha', 'pupkov', 30)
    print(per_vasya.__dict__)
    p = Point(1, -2)
    print(len(p))
    print(abs(p))