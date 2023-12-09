import click

import cmds


@click.group()
def cli():
    pass


def main():
    cli.add_command(cmds.init)
    cli.add_command(cmds.transcribe)
    cli.add_command(cmds.make)
    cli.add_command(cmds.publish)
    cli()


if __name__ == "__main__":
    main()
