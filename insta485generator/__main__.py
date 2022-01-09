"""Build static HTML site from directory of HTML templates and plain files."""
import click

@click.command()
@click.option("--count", default=1, help="Number of strings")

def main():
    """Top level command line interface."""
    print("Hellp world!")
    
if __name__ == '__main__':
    main()