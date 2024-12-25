#config
configfile: "config.yaml"

rule all:
    input:
        "md/md.gro",
        "md/md.xtc"

rule prep_protein:
    input:
        config["protein_file"]
    output:
        gro="md/protein.gro",
        top="md/topol.top",
    shell:
        """
        mkdir -p md
        cd md
        echo 15 | gmx pdb2gmx -f {input} -o protein.gro -p topol.top -i posre.itp -ignh -water spc
        sed -i 's|"posre.itp"|"posre.itp"|g' topol.top
        mv topol.top protein.itp
        python ../extract.py -i protein.itp -o topol.top
        cd ..
        touch {output.top}
        touch {output.gro} 
        """

rule prep_ligand:
    input:
        pdb=config["ligand_file"]
    output:
        gro="md/ligand.gro",
        itp="md/ligand.itp"
    shell:
        """
        cp {input.pdb} md/ligand.pdb
        cd md
        obabel -ipdb ligand.pdb -omol2 -O ligand.mol2
        cp ligand.mol2 ../sobtop
        cd ../sobtop
        ./sobtop ligand.mol2<gen_top.txt
        cd ..
        mv sobtop/ligand.gro {output.gro}
        mv sobtop/ligand.itp {output.itp}
        rm -rf sobtop/ligand.mol2
        rm -rf sobtop/ligand.top
        cd md
        sed -i 's/MOL/LIG/' ligand.itp
        sed -i 's/MOL/LIG/' ligand.gro
        """

rule prep_cofactor:
    input:
        pdb=config["cofactor_file"]
    output:
        gro="md/cofactor.gro",
        itp="md/cofactor.itp"
    shell:
        """
        cp {input.pdb} md/cofactor.pdb
        cd md
        obabel cofactor.pdb -O cofactor.mol2 -xu
        cp cofactor.mol2 ../sobtop
        cd ../sobtop
        ./sobtop cofactor.mol2<gen_top.txt
        cd ..
        mv sobtop/cofactor.gro {output.gro}
        mv sobtop/cofactor.itp {output.itp}
        rm -rf sobtop/cofactor.mol2
        rm -rf sobtop/cofactor.top
        cd md
        sed -i 's/MOL/COF/' cofactor.itp
        sed -i 's/MOL/COF/' cofactor.gro
        """

rule merge:
    input:
        protein_gro="md/protein.gro",
        cofactor_gro="md/cofactor.gro",
        ligand_gro="md/ligand.gro",
        ligand_itp="md/ligand.itp",
        cofactor_itp="md/cofactor.itp"
    output:
        "md/complex.gro"
    shell:
        """
        python merge_itp.py -lp {input.cofactor_itp} {input.ligand_itp} -p md/topol.top
        python add_itp.py -l protein.itp {input.cofactor_itp} {input.ligand_itp} -p md/topol.top
        sed -i 's/md\/cofactor.itp/cofactor.itp/g' md/topol.top
        sed -i 's/md\/ligand.itp/ligand.itp/g' md/topol.top
        python merge_gro.py -p {input.protein_gro} -l {input.cofactor_gro} {input.ligand_gro} -o {output}
        """

rule prep_md:
    input:
        "md/complex.gro"
    output:
        "md/em.gro",
    shell:
        """
        export OMP_NUM_THREADS=32
        gmx editconf -f {input} -o md/box.gro -c -d 1.0 -bt cubic
        gmx solvate -cp md/box.gro -o md/water.gro -p md/topol.top
        gmx grompp -f mdp/ions.mdp -c md/water.gro -p md/topol.top -o md/ions.tpr
        echo 16 | gmx genion -s md/ions.tpr -o md/ions.gro -p md/topol.top -pname NA -nname CL -neutral
        gmx grompp -f mdp/em.mdp -c md/ions.gro -p md/topol.top -o md/em.tpr -maxwarn 2
        gmx mdrun -v -ntmpi 1 -ntomp 32 -deffnm md/em
        cd md
        echo 0 | gmx genrestr -f cofactor.gro -o posres_cofactor.itp -fc 1000 1000 1000
        echo 0 | gmx genrestr -f ligand.gro -o posres_ligand.itp -fc 1000 1000 1000
        python ../add_posre.py -l posres_cofactor.itp posres_ligand.itp -p topol.top        
        echo -e "1|13|14\\nq" | gmx make_ndx -f em.gro -o index.ndx
        cd ..
        touch {output}
        """
rule md:
    input:
        "md/em.gro"
    output:
        gro="md/md.gro",
        xtc="md/md.xtc"
    shell:
        """
        export OMP_NUM_THREADS=32
        gmx grompp -f mdp/nvt.mdp -c {input} -r {input} -p md/topol.top -o md/nvt.tpr -maxwarn 4
        gmx mdrun -v -ntmpi 1 -ntomp 32 -gpu_id 0 -deffnm md/nvt
        gmx grompp -f mdp/nvt2.mdp -c md/nvt.gro -r md/nvt.gro -n md/index.ndx -p md/topol.top -o md/nvt2.tpr -maxwarn 5
        gmx mdrun -v -ntmpi 1 -ntomp 32 -gpu_id 0 -deffnm md/nvt2
        gmx grompp -f mdp/npt.mdp -c md/nvt2.gro -r md/nvt2.gro -n md/index.ndx -p md/topol.top -o md/npt.tpr -maxwarn 4
        gmx mdrun -v -ntmpi 1 -ntomp 32 -gpu_id 0 -deffnm md/npt
        gmx grompp -f mdp/md.mdp -c md/npt.gro -r md/npt.gro -n md/index.ndx -p md/topol.top -o md/md.tpr -maxwarn 4
        gmx mdrun -v -ntmpi 1 -ntomp 32 -gpu_id 0 -deffnm md/md
        touch {output.gro}
        touch {output.xtc}
        """