"""Build static HTML site from directory of HTML templates and plain files."""
import os
import sys
import json
import shutil
import click
import jinja2


@click.command()
@click.argument("INPUT_DIR")
@click.option("-o", "--output",
              type=click.Path(exists=False),
              default="html",
              help="Output directory.")
@click.option("-v", "--verbose", is_flag=True, help="Print more output.")
def main(input_dir, verbose, output):
    """Templated static website generator."""
    if not os.path.exists(input_dir):
        sys.exit(f"\'{input_dir}\' is not a directory.")

    if output == "html":
        generated_dest = f"{input_dir}/{output}"
    else:
        generated_dest = f"{output}"

    if os.path.exists(f"{input_dir}/static"):
        static_files = os.listdir(f"{input_dir}/static")
        for static_file in static_files:
            full_file_name = os.path.join(f"{input_dir}/static", static_file)
            shutil.copytree(full_file_name,
                            f"{generated_dest}/{static_file}")
    else:
        os.makedirs(generated_dest)

    if verbose:
        print(f"Rendered index.html -> {generated_dest}/index.html")

    with open(f"{input_dir}/config.json",
              "r",
              encoding="utf-8") as in_file:
        data = json.load(in_file)

        for info in data:
            url = info["url"]

            env = jinja2.Environment(loader=jinja2.FileSystemLoader(
                f"{input_dir}/templates/"),
                autoescape=jinja2.
                select_autoescape(["html", "xml"]))

            template = env.get_template(info["template"])
            generated = template.render(info["context"])

            if not os.path.exists(f"{generated_dest}{url}"):
                os.makedirs(f"{generated_dest}{url}")

            with open(f"{generated_dest}{url}/index.html",
                      "w",
                      encoding="utf-8") as out_file:
                out_file.write(generated)


if __name__ == '__main__':
    main()
