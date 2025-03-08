# create an llm script that responds after sentinel character at the end of a line
import ai
import sys
import utils

if __name__ == "__main__":
    # might say something about writing code
    ai_thread = ai.OllamaThread(
        initial_prompt="You are interacting with a terminal program, only output the exact inputs asked for.")
    max_tok = int(sys.argv[1])
    sentinel = sys.argv[2]

    while True:

        input_stream = utils.input_to_sentinel(sentinel)
        ai_output = ai_thread.query(input_stream, max_tok)
        print(ai_output)
        print(sentinel)
