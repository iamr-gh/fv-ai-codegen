import deal
import fuzz
import ollama
import ai_integration


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
        for i in range(len(x) - 2):
            if x[i] > x[i + 1]:
                x[i], x[i + 1] = x[i + 1], x[i]
                change = True
    return x


def queryModel(msg: str) -> str:
    return ollama.chat(model="llama3.1", messages=[{'role': 'user', 'content': msg}])


def main():
    # print(sort_func([1, 3, 2]))
    # print(square(2))
    # print("Hello from fv-ai-codegen!")
    # fuzz.fuzz(sort_func)
    # _ = deal.cases(sort_func) can't figure out how to do this
    # resp = queryModel("Why is the sky blue?")
    # print(resp)
    # resp = queryModel("What was the previous message?")
    # print(resp)

    ai = ai_integration.OllamaThread()
    while (True):
        txt = input(">>> ")
        print(ai.query(txt, 100))


if __name__ == "__main__":
    main()
