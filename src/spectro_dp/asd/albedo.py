import click

from .measurement_composite import MeasurementComposite
from .plotter import Plotter


@click.command(
    help='Calculate snow albedo from a sequence of up and down looking '
         'measurements with the ASD field spectrometer.'
)
@click.option(
    '-in', '--input-dir',
    prompt=True, type=click.Path(exists=True),
    help='Path to input directory containing both up and down looking '
         'measurements',
)
@click.option(
    '-fp', '--file-prefix',
    prompt=True,
    help='Prefix of the filename for an individual measurement.'
)
@click.option(
    '-ofs', '--output-file-suffix',
    default='albedo',
    help='Suffix to use for the saved file. Default: albedo'
)
@click.option(
    '--up-looking-file-start', '-up', 'up_index',
    prompt=True, type=int,
    help='Start index of the file containing the first up looking measurement.'
)
@click.option(
    '--up-looking-count', '-ulc', 'up_count',
    default=10, type=int,
    help='Total count of up looking measurements. (Default: 10)'
)
@click.option(
    '--down-looking-file-start', '-down', 'down_index',
    prompt=True, type=int,
    help='Start index of the file containing the first down looking '
         'measurement.',
)
@click.option(
    '--down-looking-count', '-dlc', 'down_count',
    default=10, type=int,
    help='Total count of up looking measurements. (Default: 10)'
)
@click.option(
    '--debug',
    is_flag=True, default=False,
    help='Print information of processed files while processing',
)
def cli(
        input_dir,
        file_prefix, output_file_suffix,
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

        print(f"Results saved to:\n  {composite.save(output_file_suffix)}")

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
