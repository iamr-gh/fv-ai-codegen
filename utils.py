def input_to_sentinel(sentinel: str) -> str:
    input_lines = []
    while True:
        input_line = input()
        input_lines.append(input_line)
        if input_line[-len(sentinel):] == sentinel:
            input_lines[-1] = input_line[:-len(sentinel)]  # remove sentinel char from input:
            break

    return "\n".join(input_lines)


class bcolors:
    # for colored terminal printing
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
