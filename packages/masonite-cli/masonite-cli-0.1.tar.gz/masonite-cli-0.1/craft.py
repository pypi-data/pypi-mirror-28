import click

@click.command()
@click.argument('command')
def cli(command):
    globals()[command]()

def auth():
	click.echo('auth system')
