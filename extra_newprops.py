from __future__ import print_function, absolute_import

import sys, os
from rdkit import Chem as C
from rdkit import rdBase
from rdkit.Chem import Descriptors as D
from rdkit.Chem import rdMolDescriptors as CD
from rdkit.Chem import AllChem




def record_error(error_file, smiles, cid):
    fail_file = "failed_" + error_file
    with open(fail_file, 'a') as err_f:
         mol = [smiles, cid]
         err_f.write(' '.join(mol) + '\n')
         err_f.close()

def main(args):
    print(rdBase.rdkitVersion)
    input_filename = os.path.basename(args[1]).split('.')[0]
    result_file = "output_" + input_filename

    print(result_file)
    try:
         with open(result_file, 'a') as output:
             header = ['smiles', 'cid', 'npr1', 'npr2']
             output.write((' '.join(header)) +'\n')
             with open (args[1]) as f:
                 for line in f:
                     try:
                         smiles,cid=line.strip().split(None,1)
                         mol = C.MolFromSmiles(smiles)
                         mol = C.AddHs(mol)
                         AllChem.EmbedMolecule(mol, useExpTorsionAnglePrefs=True, useBasicKnowledge=True)
                     except Exception as e:
                         continue
                     try:
                         npr1 = round(CD.CalcNPR1(mol), 4)
                         npr2 = round(CD.CalcNPR2(mol), 4)
                     except Exception as e:
                         print("Failed molecules:" + cid)
                         record_error(input_filename, smiles, cid)
                         continue                 
                     a = [ smiles, cid, npr1,npr2  ]
                     a=map(str,a)
                     #print (' '.join(a))
                     output.write((' '.join(a)) +'\n')
                     #print (' '.join(a))
                 f.close()
             output.close()
    except IOError as err:
        print(err) 
             

if __name__ == '__main__':
    sys.exit(main(sys.argv))
