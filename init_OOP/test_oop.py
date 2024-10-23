# _(protected) знак того что это внутренний атрибут и не предназначен для использования
# наследуется и видим дочерними классами
# __(private) приватные атрибуты, не наследуется, можно обращаться через сеттеры, геттеры и делитеры,
# а еще через (object._Class__attribute ---> Name Mangling)

class Ineger:
    '''дескриптор'''
    def __set_name__(self, owner, name):
        self.name = "_" + name
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
class Person:
    '''данные для хранения персоны'''

    def __init__(self, name, age):
        self.__name = name
        self.age = age

    def conclusion(self):
        print(f"I am {self.__name} and to me {self.__age}")

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        if 1 > age or age > 120:
            raise ValueError('Age must be in range')
        self.__age = age

    @age.deleter
    def age(self):
        del self.__age


if __name__ == '__main__':
    per = Person("Igor", 30)
    per.age = 100
    print(per.age, per.__dict__)
    per.conclusion()
    print(dir(per))
