##

import subprocess


def cli_run(cmd: str, *args: str, input_file: str = None):
    command_output = ""
    run_cmd = [
        cmd,
        *args
    ]

    p = subprocess.Popen(run_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    if input_file:
        with open(input_file, 'rb') as input_data:
            while True:
                line = input_data.readline()
                if not line:
                    break
                p.stdin.write(line)
            p.stdin.close()

    while True:
        line = p.stdout.readline()
        if not line:
            break
        line_string = line.decode("utf-8")
        command_output += line_string

    p.wait()

    return p.returncode, command_output
