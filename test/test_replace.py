import flexion
import io
import conllu
import copy

# read conllu file
iowrapper = io.open("tmp/de_hdt-ud-dev.conllu", "r", encoding="utf-8")
dat = []
i = 0
for s in conllu.parse_incr(iowrapper):
    dat.append(s)
    i += 1
    if i > 10:
        break

"""
dat[5]
'" Diesen Gerüchten liegt eine unseriöse Recherche zugrunde.'
"""


def test1():
    tokens = [{**t} for t in dat[5] if isinstance(t.get('id'), (int, str))]
    tokens[2]["form"] = ["Mutmaßungen", "Theorien", "Spekulationen"]
    sents = flexion.generate_strings(tokens)
    assert len(sents) == 3
    assert sents == [
        '" Diesen Mutmaßungen liegt eine unseriöse Recherche zugrunde.',
        '" Diesen Theorien liegt eine unseriöse Recherche zugrunde.',
        '" Diesen Spekulationen liegt eine unseriöse Recherche zugrunde.'
    ]


def test2():
    tokenlist = [{**t} for t in dat[5]]
    lemma = "Gerücht"
    substitute = "Spekulation"
    sents = flexion.replace(lemma, substitute, tokenlist)
    assert len(sents) == 1
    assert sents[0] in (
        '" Diesen Spekulationen liegt eine unseriöse Recherche zugrunde.')
