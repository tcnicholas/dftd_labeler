# DFT Dispersion Correction Labeler

This Python-based project is designed to process a database of structures and 
label them with DFT dispersion corrections. It reads an existing database, 
applies the desired DFT dispersion scheme ontop of the present energy and force
labels, and writes the corrected structures to a new database.

## Installation

We recommend working in a conda environment:

```bash
conda create -n dftd-env python=3.9 -y
conda activate dftd-env
```

Then install conda-specific dependencies:

```bash
conda install -c conda-forge ase simple-dftd3 dftd3-python dftd4 dftd4-python -y
```

## Usage

After installation, you can use the tool as a command-line program:

```css
dftd_labeler -i INPUT_DATABASE_PATH -o OUTPUT_DATABASE_PATH -d DISPERSION_SCHEME
```

## Options

 - -m or --dft_method: Specifies the DFT Method to be used. Default is 'SCAN'.
 - -i or --input_database: Specifies the path to the database to be read. This is a required argument.
 - -o or --output_database: Specifies the path to write the labeled database. This is a required argument.
 - -d or --dispersion: Specifies which dispersion scheme to use. Only values 3 or 4 are allowed, indicating DFT-D3 and DFT-D4 respectively. This is a required argument.

## Example

To process a database using the default DFT method (SCAN) and the DFT-D4 dispersion scheme:

```css
dftd_labeler -i my_database.extxyz -o output_database.extxyz -d 4
```

## Dependencies

This project depends on several Python libraries, including ase, dftd4.ase, 
dftd3.ase. Ensure you have all required dependencies installed.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to 
discuss what you would like to change.