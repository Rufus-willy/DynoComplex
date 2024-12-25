#!/usr/bin/env python3
import argparse

def merge_gro_files(protein_gro, ligand_gros, output_gro):
    try:
        
        with open(protein_gro, 'r') as f:
            protein_lines = f.readlines()
        
        
        total_atoms = int(protein_lines[1].strip())
    
        
        output_lines = []
        output_lines.append(protein_lines[0])  
        output_lines.extend(protein_lines[2:-1])  
        
        
        for ligand_gro in ligand_gros:
            with open(ligand_gro, 'r') as f:
                ligand_lines = f.readlines()
            
            
            total_atoms += int(ligand_lines[1].strip())
            
            output_lines.extend(ligand_lines[2:-1])
        
        
        output_lines.insert(1, f"{total_atoms}\n")
        
        output_lines.append(protein_lines[-1])
        
        
        with open(output_gro, 'w') as f:
            f.writelines(output_lines)
            
        print(f"Successfully merged GRO files to {output_gro}")
        print(f"Total atoms: {total_atoms}")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find input file - {str(e)}")
    except ValueError as e:
        print(f"Error: Invalid atom count in input files - {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Merge protein and ligand GRO files')
    parser.add_argument('-p', '--protein', required=True, help='Input protein GRO file')
    parser.add_argument('-l', '--ligand', required=True, nargs='+', help='Input ligand GRO file(s)')
    parser.add_argument('-o', '--output', required=True, help='Output merged GRO file')
    
    args = parser.parse_args()
    merge_gro_files(args.protein, args.ligand, args.output)

if __name__ == "__main__":
    main() 