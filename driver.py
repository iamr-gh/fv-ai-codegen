from string import Template
import os
import subprocess

if __name__ == '__main__':
    fname = "templates/square.py"

    file = open(fname)
    content = file.read()
    print(content)

    # using the real template might make things easier long term
    template = Template(content)
    replace_data = input("write the body of the function:")

    new_content = template.substitute(body=replace_data)
    print("modified content:", new_content)

    # eventually can use pathlib to modify fnames differently
    new_fname = fname + "_test"
    file_new = open(new_fname, "w")
    file_new.write(new_content)

    prover_result = subprocess.run(['uv', 'run', 'python', '-m', 'deal', 'prove', new_fname],
                                   capture_output=True)

    # test with the prover initially
    print("Prover output")
    print(prover_result.stdout)
    print(prover_result.stderr)

    # remove a file
    # os.remove(new_fname)

    # test with fuzzer
    # going to need some additional tooling to
    # read every func and fuzz it then run output


