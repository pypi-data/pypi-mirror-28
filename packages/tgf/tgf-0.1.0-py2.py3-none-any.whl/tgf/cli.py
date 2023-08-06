# -*- coding: utf-8 -*-

import click


@click.command()
@click.option('--debug/--no-debug', default=False, help='Enables debug mode. Will print errors.')
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def main(debug, input, output):
    """Console script for tgf"""
    click.echo("Replace this message by putting your code into "
               "tgf.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")


if __name__ == "__main__":
    main()
