from wraptitude import Wrapper


def test_args():
    @Wrapper(dict, a=3, b=4)
    def f(**kwargs):
        return kwargs

    assert f(c=1, d=2) == {
        'a': 3,
        'b': 4,
        'c': 1,
        'd': 2
    }


def test_dict():
    @Wrapper(dict)
    def f(x):
        for i in range(x):
            yield str(i), float(i)

    assert f(12) == {str(x): float(x) for x in range(12)}


def test_identity():
    @Wrapper(lambda x: x)
    def f(x):
        return x + 1

    assert (f(-2), f(-1), f(0), f(1)) == (-1, 0, 1, 2)


def test_list():
    @Wrapper(list)
    def f(x):
        for i in range(x):
            yield i ** 2

    assert f(3) == [x ** 2 for x in range(3)]
