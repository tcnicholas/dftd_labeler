import os
import hashlib
import argparse
import logging
from typing import List
from ase import Atoms
from ase.io import read, extxyz
from dftd4.ase import DFTD4
from dftd3.ase import DFTD3


# Setup basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_environment() -> None:
    """
    Setup environment variables using defaults or user-defined values.
    """
    ENV_VARS = {
        "OMP_NUM_THREADS": os.getenv("OMP_NUM_THREADS", "1"),
        "OPENBLAS_NUM_THREADS": os.getenv("OPENBLAS_NUM_THREADS", "1"),
        "MKL_NUM_THREADS": os.getenv("MKL_NUM_THREADS", "1"),
        "VECLIB_MAXIMUM_THREADS": os.getenv("VECLIB_MAXIMUM_THREADS", "1"),
        "NUMEXPR_NUM_THREADS": os.getenv("NUMEXPR_NUM_THREADS", "1"),
    }
    for key, val in ENV_VARS.items():
        os.environ[key] = val


def append_to_extxyz(filename: str, atom_obj: Atoms, dispersion: int) -> None:
    """
    Append an Atoms object to an extxyz file.

    :param filename: name of file to write.
    :param atom_obj: ASE Atoms object to be appended.
    :param dispersion: Dispersion scheme to use.
    """
    extxyz_columns = [
        'symbols', 'numbers', 'positions', 'forces_SCAN', f'forces_SCAN_d{dispersion}'
    ]
    with open(filename, 'a') as f:
        extxyz.write_extxyz(
            f, [atom_obj], 
            write_results=False, 
            columns=extxyz_columns, 
            write_info=True
        )


def generate_index_filename(input_path: str, output_path: str) -> str:
    """
    Generate an index filename based on the input and output paths.

    :param input_path: Path to the input file.
    :param output_path: Path to the output file.
    :return: Name of the index file.
    """
    combined = input_path + output_path
    name_hash = hashlib.md5(combined.encode()).hexdigest()
    return f'last_processed_index_{name_hash}.txt'


def retrieve_start_index(index_file: str) -> int:
    """
    Retrieve the starting index from the given file, if it exists.

    :param index_file: Path to the index file.
    :return: Starting index.
    """
    start_idx = 0
    if os.path.exists(index_file):
        with open(index_file, 'r') as f:
            lines = f.readlines()
            if len(lines) > 2:
                start_idx = int(lines[2].strip()) + 1
    return start_idx


def process_structure(atoms: Atoms, dft_method: str, dispersion: int) -> Atoms:
    """
    Process a given Atoms object with the specified method and dispersion.

    :param atoms: The Atoms object.
    :param dft_method: DFT method to use.
    :param dispersion: Dispersion scheme to use.
    :return: Processed Atoms object.
    """

    # make copy of atoms object to prevent manipulating the original object.
    atoms_dispersion = atoms.copy()

    # check which dispersion correction we are using. note the D3 correction 
    # defaults to with BJ-damping.
    if dispersion == 4:
        atoms_dispersion.calc = DFTD4(method=dft_method)
    elif dispersion == 3:
        atoms_dispersion.calc = DFTD3(method=dft_method, damping="d3bj")

    # prepare the new energy, forces, and stress labels.
    energy_label = f'energy_{dft_method}'
    force_label = f'forces_{dft_method}'
    stress_label = f'stress_{dft_method}'
    
    # compute the new energy.
    atoms.info[energy_label+f'_d{dispersion}'] = atoms.info[energy_label] + \
        atoms_dispersion.get_potential_energy(force_consistent=True)

    # compute the new forces.
    atoms.set_array(force_label+f'_d{dispersion}', atoms.arrays[force_label] + \
        atoms_dispersion.get_forces())

    # compute the new stress.
    atoms.info[stress_label+f'_d{dispersion}'] = atoms.info[stress_label] + \
        (-atoms_dispersion.get_stress(voigt=False) * atoms_dispersion.get_volume()).flatten()

    return atoms


def main():
    """
    Main function to label structures with DFT-D4 correction.
    """

    setup_environment()

    parser = argparse.ArgumentParser(
        description="Label structures with DFT-D4 correction."
    )
    parser.add_argument(
        "-m", "--dft_method", 
        type=str, 
        default='SCAN', 
        help="DFT Method to be used. Default is 'SCAN'."
    )
    parser.add_argument(
        "-i", "--input_database",
        type=str, 
        required=True, 
        help="Path to the database to be read."
    )
    parser.add_argument(
        "-o", "--output_database",
        type=str, 
        required=True, 
        help="Path to write the labeled database."
    )
    parser.add_argument(
        "-d", "--dispersion", 
        type=int, 
        required=True, 
        choices=[3, 4], 
        help="Which dispersion scheme to use."
    )
    args = parser.parse_args()

    index_file = generate_index_filename(
        args.input_database, 
        args.output_database
    )
    start_idx = retrieve_start_index(index_file)

    try:
        full_database = read(args.input_database, format='extxyz', index=':')
    except Exception as e:
        logger.error(f"Failed to read the database: {str(e)}")
        return

    if start_idx >= len(full_database):
        logger.info("All structures processed. Exiting...")
        return

    for idx, atom in enumerate(full_database[start_idx:], start=start_idx):
        
        logger.info(f"Processing structure: {idx}")
        processed_atom = process_structure(atom,args.dft_method,args.dispersion)
        append_to_extxyz(args.output_database,processed_atom,args.dispersion)

        with open(index_file, 'w') as f:
            f.write(f"Input: {args.input_database}\nOutput: {args.output_database}\n{idx}")

    logger.info("Finished!")


if __name__ == '__main__':
    main()
