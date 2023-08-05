import click

from uptodate.core import UpToDate


DEFAULT_FILE_PATH = 'requirements.txt'


@click.command()
@click.argument('file_paths', nargs=-1, type=click.Path(exists=True))
def up_to_date(file_paths):
    """Scan requirements.txt file for dependences which are not up to date"""

    if len(file_paths) == 0:
        file_paths = (DEFAULT_FILE_PATH, )

    for file_path in file_paths:
        click.secho(file_path, fg='blue')
        uptodate = UpToDate()
        uptodate.check(file_path)


if __name__ == '__main__':
    up_to_date()
