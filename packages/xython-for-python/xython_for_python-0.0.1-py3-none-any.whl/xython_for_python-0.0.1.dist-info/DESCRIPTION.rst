Xython
-------------------------


.. code :: python

    import xython as xy
    _ = xy._

    xy.and_then(
            sum | xy.partial([]),
            sum,
            print
            )([[1, 2, 3], [2, 3, 4]])
    # => print(sum(sum([[1, 2, 3], [2, 3, 4]], [])))

    _*2    | xy.before_with(_ + 10) | xy.call(2)  # => (2 + 10) * 2

    _ + 10 | xy.next_by(_ * 5)     | xy.call(2)   # => (2 + 10) * 5

    (lambda x, y: x+y) | xy.to_curry | xy.call(1, 2)  # => 1 + 2

    (lambda x, y: x+y) | xy.to_curry | xy.call(1) | xy.call(2)  # => 1 + 2


Not only the syntax sugar, `JIT` and `AOT` could be expected.

