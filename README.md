## Requirements

- GROMACS
- Python
- Snakemake
- Sobtop (For generating small molecule topology files)
- s_mmpbsa (For calculating mmpbsa)

## Acknowledgements

Sobtop:
This workflow uses [Sobtop_1.0(dev5)](http://sobereva.com/soft/Sobtop/) developed by Dr. Tian Lu for generating small molecule topology files. If you use this workflow in your research, please cite Sobtop as:

Tian Lu, Sobtop, Version [sobtop_1.0(dev5)], http://sobereva.com/soft/Sobtop (accessed on 24-12-2024)
s_mmpbsa:
This workflow uses [s_mmpbsa-0.6.7](https://github.com/Supernova4869/s_mmpbsa) developed by jiaxing_zhang@outlook.com for calculating mmpbsa.

## Usage

1. Configure input files:
   Edit `config.yaml` to set input file paths:
   ```yaml
   protein_file: "input/protein.pdb"
   ligand_file: "input/ligand.pdb"
   cofactor_file: "input/cofactor.pdb"
   ```

2. Run simulation:
   ```bash
   snakemake 
   ```

## Scripts Description

### add_itp.py
- Purpose: Add ITP files to topology file
- Usage: `python add_itp.py -l <itp_files> -p <topology_file>`

### add_posre.py
- Purpose: Add position restraints to topology file
- Usage: `python add_posre.py -l <posre_files> -p <topology_file>`

### merge_gro.py
- Purpose: Merge multiple GRO files
- Usage: `python merge_gro.py -p <protein_gro> -l <ligand_gros> -o <output_gro>`

### merge_itp.py
- Purpose: Merge ligand ITPs with protein topology
- Usage: `python merge_itp.py -lp <ligand_itps> -p <protein_top>`

### extract.py
- Purpose: Extract topology sections
- Usage: `python extract.py -i <input_file> -o <output_file>`

### run_mmpbsa.py
- Purpose: Automate MM-PBSA calculations using s_mmpbsa
- Usage: `python run_mmpbsa.py -t <tpr_file> -x <xtc_file> -n <ndx_file> -p <protein_group> -l <ligand_group> -i <interval>`
- Parameters:
  - `-t, --tpr`: Input tpr file from MD simulation
  - `-x, --xtc`: Input trajectory file
  - `-n, --ndx`: Input index file
  - `-p, --protein`: Protein group number in index file
  - `-l, --ligand`: Ligand group number in index file
  - `-i, --interval`: Analysis interval in ns (default: 1)