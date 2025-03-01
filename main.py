import deal
import fuzz


@deal.post(lambda x: x >= 0)
@deal.pure
def square(x: int) -> int:
    return x * x


@deal.post(lambda result: all(result[i] <= result[i + 1] for i in range(len(result) - 1)))
@deal.ensure(lambda x, result: result == sorted(x))
def sort_func(x: list[int]) -> list[int]:
    # bubble sort
    change = True
    while (change):
        change = False
        for i in range(len(x) - 1):
            if x[i] > x[i + 1]:
                x[i], x[i + 1] = x[i + 1], x[i]
                change = True
    return x

# ok to use this library, probably want to fuzz test inputs in their type range


def main():
    # print(sort_func([1, 3, 2]))
    # print(square(2))
    # print("Hello from fv-ai-codegen!")
    fuzz.fuzz(sort_func)


if __name__ == "__main__":
    main()
