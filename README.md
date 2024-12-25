## Requirements

- GROMACS
- Python
- Snakemake

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
