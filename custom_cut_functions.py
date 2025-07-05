import awkward as ak
import math
from pocket_coffea.lib.cut_definition import Cut

def cut_function(events, params, year, sample, **kwargs):
    masks = []
    for i, c in enumerate(params["coll"]):
        objs = getattr(events, c)
        ptmin = params["minpt"][i]
        nmin = params["nMin"][i]

        if ptmin is not None:
            objs = objs[objs.pt > ptmin]

        mask = ak.num(objs) >= nmin
        masks.append(mask)

    # Return mask where at least one condition is satisfied
    combined_mask = masks[0]
    for m in masks[1:]:
        combined_mask = combined_mask | m

    return ak.where(ak.is_none(combined_mask), False, combined_mask)
def get_nObj_min_or(nMin, minpt,coll, name=None):
    if not (len(coll) == len(nMin) and (minpt is None or len(minpt) == len(coll))):
        raise ValueError("coll, nMin, and minpt (if provided) must have same length")

    if name is None:
        name = "cut_" + "_or_".join([
            f"{c}_min{nMin[i]}" + (f"_pt{minpt[i]}" if minpt else "")
            for i, c in enumerate(coll)
        ])
    return Cut(
        name=name,
        params={
            "coll": coll,
            "nMin": nMin,
            "minpt": minpt if minpt else [None] * len(coll),
        },
        function=cut_function,
    )

def VBS_jets(events, params, year, sample, **kwargs):
    mask = (
        (events.VBS_dijet_system.pt > params["mass"] )
        & 
        (events.VBS_dijet_system.deltaEta > params["deltaEta"])
    )
    return ak.where(ak.is_none(mask), False, mask)

def single_good_electron(events, params, year, sample, **kwargs):
    mask = (
        ak.num(events.ElectronGood) >= 2
        )
    return ak.where(ak.is_none(mask), False, mask)  

def single_good_muon(events, params, year, sample, **kwargs):
    mask = (
        ak.num(events.MuonGood) >= 2
    )  
    return ak.where(ak.is_none(mask), False, mask)

def single_good_lepton(events, params, year, sample, **kwargs):
    ele_mask = single_good_electron(events, params, year, sample, **kwargs)
    muon_mask = single_good_muon(events, params, year, sample, **kwargs)
    combined_mask = ele_mask & muon_mask
    return ak.where(ak.is_none(combined_mask), False, combined_mask)    


# 1 lepton + 4 jets OR 1 lepton + 1 FatJet + 2 Jets
def semileptonic(events, params, year, sample, **kwargs):
 #   single_electron = events.nElectronGood == 1
    single_muon = events.nMuonGood == 1
    print(events.MET.pt)
    print(events.Muon.pt)
    print(events.MuonGood.pt)
    mask = (
        (events.nLeptonsGood == 1)
        & (single_muon)
        & ak.firsts(events.MuonGood.pt > params["pt_leading_muon"])
        & (
            (events.nCleanJets >= params["nJet"])
            | (
                (events.nCleanFatJets >= params["nFatJets"])
                & (events.nCleanJets >= params["nJet_with_FatJet"])
            )
        )
        & (events.MET.pt > params["met"])
    )

    print(mask)

    return ak.where(ak.is_none(mask), False, mask)


semileptonic_presel = Cut(
    name="semileptonic_presel", 
    params = {
        "pt_leading_electron" : 20,
        "pt_leading_muon" : 20,
        "nJet" : 1, 
        "nFatJets" : 1,
        "nJet_with_FatJet" : 1,
        "met" : 20,
    },
    function = semileptonic,
) 
    
VBS_jets_presel = Cut(
    name="VBS_jets_presel",
    params = {
        "mass" : 400,
        "deltaEta" : 2.5,
    },
    function=VBS_jets,
)
SingleEle = Cut(
    name="SingleGoodEle",
    params = {},
    function=single_good_electron,
)
SingleMuon = Cut(
    name="SingleGoodMuon", 
    params = {},
    function=single_good_muon,
)
SingleLepton = Cut(
    name="SingleGoodLeptons",
    params={},
    function=single_good_lepton,
)