#!/usr/bin/env python3
import argparse

def merge_itp_files(ligand_itps, protein_top):
    try:
        with open(protein_top, 'r') as f:
            protein_lines = f.readlines()

        atomtypes_dict = {}  
        ligand_names = []
        atomtypes_header = None

        for ligand_itp in ligand_itps:
            with open(ligand_itp, 'r') as f:
                ligand_lines = f.readlines()

            for line in ligand_lines:
                if "[ moleculetype ]" in line:
                    name_line = next(l for l in ligand_lines[ligand_lines.index(line)+1:] if l.strip() and not l.startswith(';'))
                    ligand_name = name_line.split()[0]
                    ligand_names.append(ligand_name)
                    break

            atomtypes_start = False
            atomtypes_end = False
            
            for i, line in enumerate(ligand_lines):
                if "[ atomtypes ]" in line:
                    atomtypes_start = True
                    if atomtypes_header is None and i+1 < len(ligand_lines):
                        atomtypes_header = [line]
                        next_line = ligand_lines[i+1]
                        if next_line.startswith(';'):
                            atomtypes_header.append(next_line)
                elif atomtypes_start and "[ moleculetype ]" in line:
                    atomtypes_end = True
                    break
                elif atomtypes_start and not atomtypes_end:
                    if line.strip() and not line.startswith(';'):
                        atom_type = line.split()[0]
                        atomtypes_dict[atom_type] = line

            output_lines = []
            skip = False
            for line in ligand_lines:
                if "[ atomtypes ]" in line:
                    skip = True
                elif "[ moleculetype ]" in line:
                    skip = False
                if not skip:
                    output_lines.append(line)

            with open(ligand_itp, 'w') as f:
                f.writelines(output_lines)

        output_lines = []
        molecules_section = False
        ff_section_found = False
        water_section_found = False

        last_non_empty = -1
        for i, line in enumerate(protein_lines):
            if line.strip():
                last_non_empty = i

        for i, line in enumerate(protein_lines):
            if "; Include forcefield parameters" in line:
                output_lines.append(line)
                ff_section_found = True
            elif "; Include water topology" in line:
                if ff_section_found:
                    if atomtypes_header:
                        output_lines.extend(atomtypes_header)
                    output_lines.extend(atomtypes_dict.values())
                output_lines.append(line)
                water_section_found = True
            elif "[ molecules ]" in line:
                molecules_section = True
                output_lines.append(line)
            elif i == last_non_empty:
                output_lines.append(line)
                for ligand_name in ligand_names:
                    output_lines.append(f"{ligand_name:<15} 1\n")
            else:
                output_lines.append(line)

        with open(protein_top, 'w') as f:
            f.writelines(output_lines)

        print(f"Successfully merged ITP files to {protein_top}")
        print(f"Added ligands: {', '.join(ligand_names)}")
        print(f"Total unique atomtypes: {len(atomtypes_dict)}")

    except FileNotFoundError as e:
        print(f"Error: Could not find input file - {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Merge ligand ITP files with protein topology')
    parser.add_argument('-lp', '--ligand', required=True, nargs='+', help='Input ligand ITP file(s)')
    parser.add_argument('-p', '--protein', required=True, help='Input protein topology file')
    
    args = parser.parse_args()
    merge_itp_files(args.ligand, args.protein)

if __name__ == "__main__":
    main() 