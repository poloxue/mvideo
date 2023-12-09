import click


@click.command("publish")
@click.option(
    "--platform", type=click.STRING, help="Platform where you want to publish"
)
@click.option("--title", type=click.STRING, help="Title of video")
@click.option("--source-url", type=click.STRING, help="Origin url of this video")
@click.option("--keywords", type=click.STRING, help="Keywords of this video")
def publish(platform, title, source_url, keywords):
    print("publish")
    pass
