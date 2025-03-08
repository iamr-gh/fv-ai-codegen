import deal


@deal.post(lambda x: x >= 0)
@deal.pure
def square(x: int) -> int:
    return x
