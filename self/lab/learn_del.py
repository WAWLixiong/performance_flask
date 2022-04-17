"""
    B del
    C execute
    C del
    end
    A del
"""


class A:
    def __del__(self):
        print('A del')

    def conn(self):
        return B()


class B:
    def __del__(self):
        print('B del')

    def cursor(self):
        return C()


class C:
    def __del__(self):
        print('C del')

    def execute(self):
        print('C execute')


if __name__ == '__main__':
    import time

    a = A()
    a.conn().cursor().execute()

    time.sleep(3)
    print('end')
