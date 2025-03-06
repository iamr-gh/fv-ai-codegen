from string import Template
import os
import sys
import subprocess

if __name__ == '__main__':
    fname = sys.argv[1]

    file = open(fname)
    content = file.read()
    file.close()
    print(content)

    # using the real template might make things easier long term
    template = Template(content)
    replace_data = input("write the body of the function:")

    new_content = template.substitute(body=replace_data)
    print("modified content:", new_content)

    path, old_n = os.path.split(fname)
    old_name, ext = old_n.split(".")
    new_fname = os.path.join(path, old_name + "_test" + "." + ext)
    print(new_fname)
    file_new = open(new_fname, "w")
    file_new.write(new_content)
    file_new.close()

    file_new_r = open(new_fname, "r")
    # verify that file writes occur in time
    print("rewritten file:", file_new_r.read())
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
        print("Correct!")

    os.remove(new_fname)
