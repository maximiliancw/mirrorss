from datetime import datetime
import json
import os
from pprint import pprint
import click
from diskcache import Cache

from mirrorss.app import app


@click.group()
def cli():
    pass

@cli.command()
@click.option('--debug/--no-debug', default=False)
def run(debug: bool):
    if debug:
        app.run(debug=debug)
    else:
        os.system("gunicorn --workers=2 mirrorss.app:app")

@cli.group()
@click.pass_context
def cache(ctx):
    ctx.ensure_object(dict)
    ctx.obj['cache'] = Cache("cache")

@cache.command()
@click.pass_context
def clear(ctx):
    cache: Cache = ctx.obj["cache"]
    byte_size = cache.volume()
    cache.clear()
    click.echo(f"Cache cleared ({byte_size} bytes)")

@cache.command()
@click.option('--export/--no-export', default=False, help='Dump to filesystem')
@click.pass_context
def dump(ctx, export: bool):
    cache: Cache = ctx.obj["cache"]
    if not export:
        pprint(cache.__dict__)
    else:
        folder = os.path.join(os.getcwd(), "exports")
        filename = f"{datetime.today().isoformat()}.json"
        path = os.path.join(folder, filename)
        with open(path, "w") as f:
            json.dump(cache, f, indent=4)
