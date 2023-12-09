import click


@click.command("transcribe")
@click.option(
    "--whisper-mode",
    type=click.STRING,
    help="whisper model, options: tiny, base, small, medium, large",
)
@click.option("--translator", type=click.STRING, help="Translator")
@click.option("--translator-from-lang", type=click.STRING, help="Translator from lang")
@click.option("--translator-to-lang", type=click.STRING, help="Translator to lang")
def transcribe(whisper_mode, translator, translator_from_lang, translator_to_lang):
    print("transcribe")
