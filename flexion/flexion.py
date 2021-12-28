from typing import List
import os
import sfst_transduce
import pathlib
from .map_smor_conllu import match_smor_and_conllu
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
    for i, t in enumerate(tokenlist):
        if t.get("lemma") == lemma:
            smortags = match_smor_and_conllu(t, fst.analyse(t.get("form")))
            t['smortags'] = smortags
            indicies.append(i)
            # print(i, t['smortags'])
        tokens2.append(t)

    # abort
    if len(indicies) == 0:
        return []

    # enumerate all SMOR tags for substitute lemma
    subsitute_smortags = fst.analyse(substitute)
    pattern = re.compile(r'<Fem>|<Masc|<Neut>')
    count = {'<Fem>': 0, '<Masc>': 0, '<Neut>': 0}
    for sm in subsitute_smortags:
        matches = pattern.findall(sm)
        if len(matches) > 0:
            count[matches[-1]] += 1
    genus = '<Neut>' if count['<Neut>'] >= count['<Fem>'] else '<Fem>'
    genus = '<Masc>' if count['<Masc>'] > count[genus] else genus
    # print(substitute, genus)

    # generate form with SMOR for substitute lemma and overwrite `'form'` field
    for tid in indicies:
        tokens2[tid]["form"] = []
        # print(len(tokens2[tid]['smortags']))
        for smortag in tokens2[tid].get('smortags'):
            # print(smortag)
            pos = smortag.find('<+')
            adjusted = re.sub(pattern, genus, smortag[pos:])
            # print(adjusted)
            newforms = fst.generate(f"{substitute}{adjusted}")
            if len(newforms) > 0:
                tokens2[tid]["form"].extend(newforms)
    # done
    return generate_strings(tokens2)


def generate_strings(tokens) -> List[str]:
    """ generate sentence strings """
    sent = [""]
    for t in tokens:
        # check id
        if not isinstance(t.get('id'), (int, str)):
            continue
        # whitespace
        if t.get("upos") != "PUNCT":
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
    # strip
    sent = [s.strip() for s in sent]

    # done
    return sent
