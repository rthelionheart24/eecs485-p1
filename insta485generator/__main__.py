"""Build static HTML site from directory of HTML templates and plain files."""
import os
import sys
import json
import shutil
import click
import jinja2

# ! Generator needs to render all files inside /templates


@click.command()
@click.argument("INPUT_DIR")
@click.option("-o", "--output", type=click.Path(exists=False), default="html", help="Output directory.")
@click.option("-v", "--verbose", is_flag=True, help="Print more output.")
def main(input_dir, verbose, output):
    """Templated static website generator."""

    in_exist = os.path.exists(input_dir)

    if not in_exist:
        sys.exit("\'{in_dir}\' is not a directory.".format(in_dir=input_dir))

    if output == "html":
        generated_dest = "{dir}/html".format(dir=input_dir)
    else:
        generated_dest = "{dir}".format(dir=output)

    static_exist = os.path.exists("{dir}/static".format(dir=input_dir))
    if static_exist:
        static_files = os.listdir("{dir}/static".format(dir=input_dir))
        for static_file in static_files:
            full_file_name = os.path.join(
                "{dir}/static".format(dir=input_dir), static_file)
            shutil.copytree(
                full_file_name, "{dir}/{folder}".format(dir=generated_dest, folder=static_file))
    else:
        os.makedirs(generated_dest)

    if (verbose):
        print("Rendered index.html -> {}/index.html".format(generated_dest))

    with open("{dir}/config.json".format(dir=input_dir)) as js:
        data = json.load(js)

        for d in data:
            context = d["context"]
            file = d["template"]

        file_loader = jinja2.FileSystemLoader(
            "{in_dir}/templates/".format(in_dir=input_dir))
        env = jinja2.Environment(
            loader=file_loader, autoescape=jinja2.select_autoescape(["html", "xml"]))

        template = env.get_template(file)
        generated = template.render(context)

        with open("./{dir}/{target}".format(dir=generated_dest, target=file), "w") as f:
            f.write(generated)


if __name__ == '__main__':
    main()
