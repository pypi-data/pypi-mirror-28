#!/usr/bin/env bash
# Used to make a conda environment with deepchem

# Change commented out line For gpu tensorflow-gpu
#export tensorflow=tensorflow-gpu
export tensorflow=tensorflow-gpu


if [ -z "$1" ]
then
    echo "Must Specify Conda Environment Name"
fi

if [ -z "$python_version" ]
then
    echo "Using python 3.5 by default"
    export python_version=3.5
fi

unamestr=`uname`
if [[ "$unamestr" == 'Darwin' ]]; then
   source activate root
   conda install -y -q conda=4.3.25
fi

export envname=$1
conda create -y --name $envname python=$python_version
source activate $envname
conda install -y -q -c omnia pdbfixer=1.4
conda install -y -q -c conda-forge joblib=0.11
conda install -y -q -c conda-forge six=1.10.0
conda install -y -q -c deepchem mdtraj=1.9.1
conda install -y -q -c conda-forge scikit-learn=0.19.1
conda install -y -q -c conda-forge setuptools=36.2.2
conda install -y -q -c conda-forge keras=1.2.2
conda install -y -q -c conda-forge networkx=1.11
conda install -y -q -c conda-forge pillow=4.3.0
conda install -y -q -c conda-forge pandas=0.22.0
yes | pip install $tensorflow==1.4.0
conda install -y -q -c conda-forge nose=1.3.7
conda install -y -q -c conda-forge nose-timer=0.7.0
conda install -y -q -c conda-forge flaky=3.3.0
conda install -y -q -c conda-forge zlib=1.2.11
conda install -y -q -c conda-forge requests=2.18.4
conda install -y -q -c conda-forge xgboost=0.6a2
conda install -y -q -c conda-forge simdna=0.4.2
conda install -y -q -c conda-forge jupyter=1.0.0
conda install -y -q -c rdkit rdkit=2017.09.1
