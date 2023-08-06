import os
import click

@click.group()
@click.pass_context
def pipz(ctx):
    pass

@pipz.command()
@click.argument('package')
@click.option('--secret', default=None)
@click.pass_context
def install(ctx, package, secret):
    if secret is None:
        os.system("pip install {lib} --no-cache-dir --upgrade --index-url http://s3.amazonaws.com/whl/{lib}/index.html --find-links http://s3.amazonaws.com/whl/{lib}/index.html --trusted-host s3.amazonaws.com".format(lib=package))
    else:

        os.system("pip install {lib} --no-cache-dir --upgrade --index-url http://s3.amazonaws.com/whl/{secret}/{lib}/index.html --find-links http://s3.amazonaws.com/whl/{secret}/{lib}/index.html --trusted-host s3.amazonaws.com".format(lib=package, secret=secret))


@pipz.command()
@click.argument('package')
@click.pass_context
def uninstall(ctx, package):
    os.system('pip uninstall {}'.format(package))

@pipz.command()
@click.argument('package')
@click.option('--secret', default=None)
@click.pass_context
def download(ctx, package, secret):
    if secret is None:
        os.system("pip download {lib} --no-cache-dir --no-deps --index-url http://s3.amazonaws.com/whl/{lib}/index.html --find-links http://s3.amazonaws.com/whl/{lib}/index.html --trusted-host s3.amazonaws.com".format(lib=package))
    else:

        os.system("pip download {lib} --no-cache-dir --no-deps  --index-url http://s3.amazonaws.com/whl/{secret}/{lib}/index.html --find-links http://s3.amazonaws.com/whl/{secret}/{lib}/index.html --trusted-host s3.amazonaws.com".format(lib=package, secret=secret))



if __name__ == '__main__':
    pipz(obj={})
