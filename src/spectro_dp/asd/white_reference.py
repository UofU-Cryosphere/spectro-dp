from pathlib import PurePath

import click
import matplotlib.pyplot as plt

from .measurement_composite import MeasurementFile


@click.command(
    help='Check white reference measurements with the ASD field spectrometer.'
)
@click.option(
    '-in', '--input-dir',
    prompt=True, type=click.Path(exists=True),
    help='Path to input directory containing the white reference measurements',
)
@click.option(
    '-fp', '--file-prefix',
    prompt=True,
    help='Prefix of the filename for all measurements.'
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
        wr_index, wr_count,
        debug
):
    try:
        input_dir = PurePath(input_dir)
        file_suffix = '{file_index:03d}'
        file_base = file_prefix + '.' + file_suffix

        if debug:
            print("Processing:")

        plt.figure(dpi=300)
        for file_index in range(wr_index, wr_index + wr_count):
            file = input_dir.joinpath(file_base.format(file_index=file_index))

            if debug:
                print(f' - {file.as_posix()}')

            plt.plot(
                MeasurementFile.BAND_RANGE, MeasurementFile(file).data,
                label=file_suffix.format(file_index=file_index), lw=1
            )

        plt.xlabel(MeasurementFile.X_LABEL)
        plt.xlim(left=MeasurementFile.MIN_WAVELENGTH)
        plt.ylabel(MeasurementFile.Y_LABEL)
        plt.ylim(bottom=0)
        plt.title('White References: 210410r')
        plt.legend()
        plt.show()

    except FileNotFoundError as fnfe:
        print(f"ERROR: {fnfe}")
