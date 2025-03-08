import deal

@deal.post(lambda result: all(result[i] <= result[i + 1] for i in range(len(result) - 1)))
@deal.ensure(lambda x, result: result == sorted(x))
def sort_func(x: list[int]) -> list[int]:
    a
