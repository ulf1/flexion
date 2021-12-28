from typing import List
import os
import sfst_transduce
import pathlib
from .map_smor_conllu import (match_smor_and_conllu, get_best_smortag)
import re
import copy


# load FST
FSTPATH = os.environ.get("FLEXION_FSTPATH")
if FSTPATH is None:
    FSTPATH = f"{str(pathlib.Path.home())}/flexion_data/smor/SMOR/lib/smor.a"
fst = sfst_transduce.Transducer(FSTPATH)


def replace(lemma: str, substitute: str, tokenlist: List[dict]) -> List[str]:
    # run SMOR analysis if token is the given lemma
    tokens2 = []
    indicies = []
    for i, t in enumerate(copy.deepcopy(tokenlist)):
        if t.get("lemma") == lemma:
            smortags = match_smor_and_conllu(t, fst.analyse(t.get("form")))
            t['smortags'] = smortags
            indicies.append(i)
        tokens2.append(t)

    # abort
    if len(indicies) == 0:
        return []

    # enumerate all SMOR tags for substitute lemma
    subsitute_smortags = fst.analyse(substitute)
    pattern = re.compile(r'<Fem>|<Masc>|<Neut>')
    count = {'<Fem>': 0, '<Masc>': 0, '<Neut>': 0}
    for sm in subsitute_smortags:
        matches = pattern.findall(sm)
        if len(matches) > 0:
            count[matches[-1]] += 1
    genus = '<Neut>' if count['<Neut>'] >= count['<Fem>'] else '<Fem>'
    genus = '<Masc>' if count['<Masc>'] > count[genus] else genus

    # generate form with SMOR for substitute lemma and overwrite `'form'` field
    for tid in indicies:
        tokens2[tid]["form"] = []
        for smortag in tokens2[tid].get('smortags'):
            pos = smortag.find('<+')
            adjusted = re.sub(pattern, genus, smortag[pos:])
            newforms = fst.generate(f"{substitute}{adjusted}")
            if len(newforms) > 0:
                tokens2[tid]["form"].extend(newforms)

    # check genus for articles before the lemma (PronType: Art)
    for tid in indicies:
        if tid > 0:
            t = tokens2[tid - 1]
            if t.get("feats", {}).get("PronType") == "Art":
                smortags = match_smor_and_conllu(t, fst.analyse(t.get("form")))
                if len(smortags) > 0:
                    adjusted = re.sub(pattern, genus, smortags[0])
                    newforms = fst.generate(f"{adjusted}")
                    if len(newforms) > 0:
                        t['form'] = newforms[0]

    # if the lemma is root of clause sentence (PronType: Rel) the change genus

    # done
    return generate_strings(tokens2)


def generate_strings(tokens) -> List[str]:
    """ generate sentence strings """
    sent = [""]
    nextws = True
    for t in tokens:
        # check id
        if not isinstance(t.get('id'), (int, str)):
            continue
        # whitespace
        ws = True
        if not nextws:
            ws = False
        if t.get("form") in [",", ".", "!", "?", ":", ";", '“', '‘',
                             "(", "[", "{"]:
            ws = False
        if ws:
            for i in range(len(sent)):
                sent[i] += " "
        # add words
        if isinstance(t.get("form"), (list, tuple)):
            newsent = []
            for word in t.get("form"):
                tmp = copy.copy(sent)
                for i in range(len(sent)):
                    tmp[i] += word
                newsent.extend(tmp)
            sent = newsent
        else:
            for i in range(len(sent)):
                sent[i] += t.get("form")
        # skip next whitspace
        nextws = True
        if t.get("form") in ['„', '‚', ")", "]", "}"]:
            nextws = False
    # strip
    sent = [s.strip() for s in sent]

    # done
    return sent
