import sys
import subprocess
import utils


def main():
    # eventually may parameterize more
    template_fname = sys.argv[1]
    max_tok = 100
    split_fname = template_fname.split(".")
    assert split_fname[-1] == "py"

    # may abstract sentinel later

    # swap for different kinds of file extensions
    gen_driver_cmd = ["uv", "run", "gen_driver.py", template_fname]
    # gen_driver_cmd = ["ls"]
    gen_driver = subprocess.Popen(
        gen_driver_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # ai_driver_cmd = ["uv", "run", "ai_driver.py", max_tok, ">>>"]
    # ai_driver = subprocess.Popen(
    #     ai_driver_cmd,
    #     stdin=subprocess.PIPE,
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.PIPE,
    #     text=True
    # )

    ai_output = " "
    gen_err = ""
    while True:
        return_code = gen_driver.poll()
        if return_code is not None:
            print(return_code)
            print(gen_err)
            break

        gen_output, gen_err = gen_driver.communicate(input=ai_output)
        print(f"{utils.bcolors.OKBLUE}{gen_output}{utils.bcolors.ENDC}")
        # ai_output, ai_err = ai_driver.communicate(input=gen_output)
        # print(f"{utils.bcolors.OKGREEN}{ai_output}{utils.bcolors.ENDC}")

    # ai_driver.kill()
    print("Done")


if __name__ == "__main__":
    main()
