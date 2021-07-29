import click

from .measurement_composite import MeasurementComposite


@click.command()
@click.option('-in', '--input-dir', prompt=True, type=click.Path(exists=True))
@click.option('-fp', '--file-prefix', prompt=True)
@click.option(
    '--up-looking-file-start', '-up', 'set_1_index', prompt=True, type=int
)
@click.option(
    '--up-looking-count', '-ulc', 'set_1_count', default=10, type=int
)
@click.option(
    '--down-looking-file-start', '-down', 'set_2_index', prompt=True, type=int
)
@click.option(
    '--down-looking-count', '-dlc', 'set_2_count', default=10, type=int
)
@click.option('--debug', is_flag=True, default=False)
def cli(
        input_dir, file_prefix,
        set_1_index, set_1_count,
        set_2_index, set_2_count,
        debug
):
    try:
        result = MeasurementComposite(
            input_dir, file_prefix, set_1_index, set_2_index,
            set_1_count=set_1_count, set_2_count=set_2_count,
            debug=debug
        ).calculate()

        print(result.mean())
    except FileNotFoundError as fnfe:
        print(f"ERROR: {fnfe}")
