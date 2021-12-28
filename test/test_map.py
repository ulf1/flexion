import flexion


def test1():
    smortags = "<+ADJ><Comp><Adv>"
    posfeats = flexion.smor_to_conllu(smortags)
    target = {"upos": "ADJ", "Degree": "Cmp"}
    assert len(posfeats) == len(target)
    for k, v in posfeats.items():
        assert target.get(k) == v


def test2():
    posfeats = {"upos": "ADJ", "Degree": "Pos"}
    smortags = flexion.conllu_to_smor(posfeats)
    assert len(smortags) == 4
    for sm, _ in smortags.items():
        assert sm in [
            "<+ADJ><Pos>",
            "<+ADJ><Pos><Adv>",
            "<+ADJ><Pos><Invar>",
            "<+ADJ><Pos><Pred>"]


def test3():
    posfeats = {'upos': 'NOUN', 'Case': 'Dat', 'Gender': 'Neut',
                'Number': 'Plur', 'Person': '3'}
    smortags = flexion.conllu_to_smor(posfeats)
    assert len(smortags) == 2
    assert smortags['<+NN><Neut><Dat><Pl>'] == 0.8
    assert smortags['<+NN><NoGend><Dat><Pl>'] == 0.6
