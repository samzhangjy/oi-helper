import click

from oihelper.cli.run_program import run
from oihelper.cli.parse_problem import parse
from oihelper.cli.login import login
from oihelper.cli.submit_program import submit, record


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli():
    pass


cli.add_command(run)
cli.add_command(parse)
cli.add_command(login)
cli.add_command(submit)
cli.add_command(record)

if __name__ == "__main__":
    cli()
