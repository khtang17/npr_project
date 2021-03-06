# npr_project
calculate npr values of a chemical library and plot their distribution

## Calculate NPR
Setup Python environment
- Download Anaconda3 installer and install follow the instruction (https://www.anaconda.com/products/individual) 
- Create anaconda env and install packages

<pre>(base)$ conda create -c rdkit --name npr-py3 rdkit</pre>

<pre>(base)$ conda activate npr-py3</pre>


<pre>(npr-py3)$ conda install -c conda-forge vaex // vaex is dataframe library for huge libraries</pre>

<pre>(npr-py3)$ pip install ipython==7.9.0</pre>

## Run NPR calculation
Your smiles file should be in this format with no header: <smiles> <cid>

<pre>(npr-py3)$ python extra_newprops.py {smiles_file}</pre>
Notes:

- Failed and success molecules are output from this script.

- The calculation maybe slow. It is recommend that you chunk the file and run it on parallel.

## Make Heatmap
Generate h5py binary file

<pre>(npr-py3)$ python py_csv2hdf5.py {output_smiles_file}</pre>

This script without output h5py that is then can be read by vaex library (it is useful for read huge library into dataframe)

## Plot
Run Jupyter-Notebook

<pre>(npr-py3)$ jupyter-notebook</pre>

From jupyter-notebook interface

- Select 'single_plot.ipynb'

- Change the path to h5py file and run the kernel
