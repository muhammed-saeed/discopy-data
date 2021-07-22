import json
import re

import click

from discopy_data.data.loaders.raw import load_texts


@click.command()
@click.option('-i', '--src', default='-', type=click.File('r'))
@click.option('-o', '--tgt', default='-', type=click.File('w'))
@click.option('--tokenize-only', is_flag=True)
def main(src, tgt, tokenize_only):
    for doc in load_texts(re.split(r'\n\n\n+', src.read()), tokenize_only=tokenize_only):
        tgt.write(json.dumps(doc.to_json()) + '\n')


if __name__ == '__main__':
    main()
