import click


@click.command("make")
@click.option("--cover-text", type=click.STRING, help="Covert text")
@click.option("--declaim-text", type=click.STRING, help="Declaim text")
@click.option("--end-text", type=click.STRING, help="End text")
@click.option("--without-chapter", is_flag=True, help="Without chapter")
@click.option("--smart", is_flag=True, help="If final video exists, dont override")
@click.option(
    "--subtitle-mode",
    type=click.STRING,
    help="Subtitle, options: all, origin, translate, none",
)
def make(cover_text, declaim_text, end_text, without_chapter, smart, subtitle_mode):
    print("make")
