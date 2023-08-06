# -*- coding: utf-8 -*-

import os
from jinja2 import Environment, FileSystemLoader, meta
import yaml


def main():
    # define dirs
    app_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    templates_dir = os.path.join(app_dir, 'templates')
    target_dir = os.path.join(app_dir, 'rendered')
    config_dir = os.path.join(app_dir, 'config')

    # load all configs
    f = open(os.path.join(config_dir, 'main.yml'), 'r')
    configs = yaml.load(f)
    f.close()
    print(yaml.dump(configs))

    # prepare template env
    env = Environment(
        loader=FileSystemLoader([templates_dir])
    )

    # list all templates
    templates = env.list_templates('ini')
    print(templates)

    # process one template file
    template_filename = 'test.ini'

    # check variables
    template_source = env.loader.get_source(env, template_filename)
    parsed_content = env.parse(template_source)
    variables = meta.find_undeclared_variables(parsed_content)

    for v in variables:
        if v not in configs:
            raise Exception("\"{}\" is not defined".format(v))

    template = env.get_template(template_filename)
    rendered = template.render(configs)
    print(rendered)

    # with open(os.path.join(target_dir, template_filename), "wb") as f:
    #     f.write(rendered.encode("utf-8"))


main()
