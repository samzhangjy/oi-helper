import json
import os
import click
from .common import CONFIG_FILE, CONFIG_DIR

from oihelper.parser import LuoguParser

DEFAULT_TEMPLATE = """\
#include <iostream>
#include <cstdio>
#include <algorithm>
#include <string>
#include <stack>
#include <queue>
using namespace std;

int main() {
    return 0;
}
"""

@click.command()
@click.argument("pid", required=True)
def parse(pid: str):
    """Parse the given problem's test samples and generate a blank code template."""
    pid = pid.upper()
    click.echo(click.style(f"Parsing problem {pid} ...", bold=True))
    try:
        config = json.load(open(CONFIG_FILE, "r"))
    except FileNotFoundError:
        if not os.path.exists(CONFIG_DIR):
            os.mkdir(CONFIG_DIR)
        config = {}
    parser = LuoguParser()
    results = parser.parse_problem(pid)
    testcase_dir = f"{CONFIG_DIR}/{pid}"
    if not os.path.exists(testcase_dir):
        os.mkdir(testcase_dir)
    for idx, testcase in enumerate(results["testcases"], 1):
        with open(f"{testcase_dir}/test{idx}.in", "w") as f:
            f.write(testcase[0])
        with open(f"{testcase_dir}/test{idx}.out", "w") as f:
            f.write(testcase[1])
    current_solution = os.path.abspath(f"./{pid}.cpp")
    config[current_solution] = results
    json.dump(config, open(CONFIG_FILE, "w"), indent=2)
    if not os.path.exists(current_solution):
        click.echo(click.style(f"Generating a default template at {current_solution} ...", bold=True))
        with open(current_solution, "w") as f:
            f.write(DEFAULT_TEMPLATE)
    else:
        click.echo(click.style(f"Warning: Source file {current_solution} already exists, skipping template generation.", bold=True, fg="yellow"))
    click.echo(click.style(f"Problem {pid} parsed successfully.", bold=True))
