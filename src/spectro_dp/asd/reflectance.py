import click

from .measurement_composite import MeasurementComposite
from .plotter import Plotter


@click.command(
    help='Calculate reflectance from surface and white reference measurements.'
)
@click.option(
    '-in', '--input-dir',
    prompt=True, type=click.Path(exists=True),
    help='Path to input directory containing surface and white reference '
         'measurements',
)
@click.option(
    '-fp', '--file-prefix',
    prompt=True,
    help='Prefix of the filename for all measurements.'
)
@click.option(
    '--reflectance-start', '-rs', 'r_index',
    prompt=True, type=int,
    help='Start index of the file containing the surface measurement.'
)
@click.option(
    '--reflectance-count', '-rc', 'r_count',
    default=1, type=int,
    help='Total count of surface measurements. (Default: 1)'
)
@click.option(
    '--white-reference-start', '-wrs', 'wr_index',
    prompt=True, type=int,
    help='Start index of the file containing the first white reference '
         'measurement.',
)
@click.option(
    '--white-reference-count', '-wrc', 'wr_count',
    default=10, type=int,
    help='Total count of white reference measurements. (Default: 10)'
)
@click.option(
    '--debug',
    is_flag=True, default=False,
    help='Print information of processed files while processing',
)
def cli(
        input_dir, file_prefix,
        r_index, r_count,
        wr_index, wr_count,
        debug
):
    try:
        composite = MeasurementComposite(
            input_dir, file_prefix, r_index, wr_index,
            set_1_count=r_count, set_2_count=wr_count,
            debug=debug
        )
        composite.calculate()

        print(f"Results saved to:\n  {composite.save('reflectance')}")

        Plotter.show(
            composite,
            composite_title='Reflectance',
            set_1_label='Surface',
            set_2_label='White reference'
        )

    except FileNotFoundError as fnfe:
        print(f"ERROR: {fnfe}")
