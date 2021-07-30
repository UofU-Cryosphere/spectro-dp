import click

from .measurement_composite import MeasurementComposite
from .plotter import Plotter


@click.command()
@click.option('-in', '--input-dir', prompt=True, type=click.Path(exists=True))
@click.option('-fp', '--file-prefix', prompt=True)
@click.option(
    '--up-looking-file-start', '-up', 'up_index', prompt=True, type=int
)
@click.option(
    '--up-looking-count', '-ulc', 'up_count', default=10, type=int
)
@click.option(
    '--down-looking-file-start', '-down', 'down_index', prompt=True, type=int
)
@click.option(
    '--down-looking-count', '-dlc', 'down_count', default=10, type=int
)
@click.option('--debug', is_flag=True, default=False)
def cli(
        input_dir, file_prefix,
        up_index, up_count,
        down_index, down_count,
        debug
):
    try:
        composite = MeasurementComposite(
            input_dir, file_prefix, down_index, up_index,
            set_1_count=down_count, set_2_count=up_count,
            debug=debug
        )
        composite.calculate()

        print(f"Results saved to:\n  {composite.save('albedo')}")

        if composite.set_2.mean() < composite.set_1.mean():
            set_1_label = 'Incoming'
            set_2_label = 'Outgoing'
        else:
            set_1_label = 'Outgoing'
            set_2_label = 'Incoming'

        Plotter.show(
            composite,
            composite_title='Albedo',
            set_1_label=set_1_label,
            set_2_label=set_2_label
        )

    except FileNotFoundError as fnfe:
        print(f"ERROR: {fnfe}")
