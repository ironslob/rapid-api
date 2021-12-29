#!/usr/bin/env python3

import click
import os
import yaml
import sys
from jinja2 import \
    Environment, \
    FileSystemLoader, \
    StrictUndefined
from config import Config

@click.command()
@click.option('--config')
@click.option('--template')
@click.option('--output')
@click.option('--option', multiple=True)
def main(config, template, output, option):
    assert config
    assert template
    assert output

    with open(config) as fd:
        content = fd.read()

    data = yaml.load(content, Loader=yaml.SafeLoader)

    config_obj = Config(**data)
    template_data = dict(
        config=config_obj,
        options=option,
    )

    template_paths = [
        template,
    ]

    loader = FileSystemLoader(template_paths)
    jinja_env = Environment(
        loader=loader,
        undefined=StrictUndefined,
    )

    # iterate through directory
    walker = os.walk(template)

    for path, directories, files in walker:
        relative_path = path[len(template)+1:]
        output_path = os.path.join(output, relative_path)

        for directory in directories:
            directory_path = os.path.join(output_path, directory)
            directory_path = jinja_env.from_string(directory_path).render(**template_data)
            os.makedirs(directory_path, exist_ok=True)

        for filename in files:
            if filename.endswith(".swp"):
                continue

            template_path = os.path.join(relative_path, filename)
            file_path = os.path.join(output_path, filename)
            file_path = jinja_env.from_string(file_path).render(**template_data)

            print('Generating %s' % file_path)

            content = jinja_env.get_template(template_path).render(**template_data)

            with open(file_path, 'w') as fd:
                fd.write(content)

if __name__ == '__main__':
    main()
