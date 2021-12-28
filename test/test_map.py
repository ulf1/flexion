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
    for sm in smortags:
        assert sm == [
            "<+ADJ><Pos>",
            "<+ADJ><Pos><Adv>",
            "<+ADJ><Pos><Invar>",
            "<+ADJ><Pos><Pred>"]
