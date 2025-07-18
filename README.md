```
> voms-proxy-init -voms cms -rfc --valid 168:0
> apptainer shell -B /afs -B /cvmfs/cms.cern.ch \
                -B /tmp  -B /eos/cms/  -B /etc/sysconfig/ngbauth-submit \
                -B ${XDG_RUNTIME_DIR}  --env KRB5CCNAME="FILE:${XDG_RUNTIME_DIR}/krb5cc" \
    /cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/cms-analysis/general/pocketcoffea:lxplus-el9-stable
> runner --cfg configuration_VBS.py -o [outputDir]


------------------------------------------------------------------------------------------
workflowVBS.py
primo script ad essere eseguito. Definizione di nuove collezioni da usare successivamente nella selezione. I parametri che definiscono se un muone/elettrone/jet sono da considerarsi buoni o no sono nel file /parameters/object_presel.yaml
------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------
configuration_X.py
script principale. All'interno sono definiti tutti gli step che devono essere eseguiti.
-SKIM:
    selezione molto generale sugli eventi contenuti nel NanoAOD, ad esempio numero minimo di leptoni o di jet e loro pt. I parametri sono in skim_dictionary.py
-PRESELECTION:
    qui sono implementati i tagli sugli oggetti che superano il passo precedente, le funzioni che vengono usate sono definite in custom_cut_functions.py e dichiarate secondo la classe "Cut" definita qui :     
    https://github.com/PocketCoffea/PocketCoffea/blob/main/pocket_coffea/lib/cut_definition.py
-CATEGORIES
    definizione delle categorie sugli eventi che superano anche la preselection. 
------------------------------------------------------------------------------------------

