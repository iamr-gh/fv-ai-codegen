from string import Template
import os
import sys
import subprocess
import utils


def codegen_loop(fname: str, max_iterations=10):
    sentinel = ">>>"

    file = open(fname)
    content = file.read()
    file.close()

    path, old_n = os.path.split(fname)
    old_name, ext = old_n.split(".")
    new_fname = os.path.join(path, old_name + "_test" + "." + ext)
    print(new_fname)

    correct = True
    ctr = 0
    while ctr < max_iterations:
        ctr += 1
        # using the real template might make things easier long term
        template = Template(content)
        print(content)

        print("write the body of the function:\n" + sentinel)

        # allow multiline input
        replace_data = utils.input_to_sentinel(sentinel)

        new_content = template.substitute(body=replace_data)
        # print("modified content:", new_content)

        file_new = open(new_fname, "w")
        file_new.write(new_content)
        file_new.close()

        file_new_r = open(new_fname, "r")
        # could be faster to use the new_content in mem, but this verifies the actual file has been changed
        print("rewritten function:\n", file_new_r.read())
        file_new_r.close()

        prover_command = ['uv', 'run', 'python', '-m', 'deal', 'prove', new_fname]
        prover_result = subprocess.run(
            prover_command, capture_output=True, text=True
        )

        # print(prover_result)
        # test with the prover initially, it probably can't figure out validity
        print("Prover output:")
        if (prover_result.returncode == 0):
            print(prover_result.stdout)
            print(prover_result.stderr)
            # this assumes one property to prove
            if "proved!" in prover_result.stdout:
                print("Correct via proof!")
                correct = True
                break

        # now test with fuzzer
        # ok I can now run prover in and out -- need to generalize for dafny and others
        fuzz_command = ['uv', 'run', 'fuzz_driver.py', new_fname]
        fuzz_result = subprocess.run(
            fuzz_command, capture_output=True, text=True
        )

        # in this case, no output is the correct output of the fuzzer
        print("Fuzz output:")
        if fuzz_result.returncode != 0:
            print(fuzz_result.stdout)
            print(fuzz_result.stderr)
        else:
            print("Correct via fuzz!")
            correct = True
            break

        print("Code is incorrect due to above statements, rewrite the following body again:")

    if not correct:
        print("Code is incorrect, failed after too many attempts removing file")
        os.remove(new_fname)
    else:
        valid_fname = os.path.join(path, old_name + "_gen_correct" + "." + ext)
        os.rename(new_fname, valid_fname)
    return correct


if __name__ == '__main__':
    fname = sys.argv[1]
    codegen_loop(fname)
