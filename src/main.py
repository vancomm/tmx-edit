"""
This script requires patching tmx/structural.py, line 180
(PR: https://github.com/ChonkyYoshi/python-tmx/pull/1)
"""

from copy import deepcopy

from tmx import inline, load_tmx

source_file = "./data/digital-ling.tmx"
patched_file = "./data/tagless-digital-ling.tmx"


def main():
    src_tmx = load_tmx(source_file)
    new_tmx = deepcopy(src_tmx)

    assert src_tmx.tus and new_tmx.tus

    for itu, tu in enumerate(src_tmx.tus or ()):
        for ituv, tuv in enumerate(tu.tuvs):
            if len(tuv.runs) > 1:
                clean_text = "".join(
                    run.text for run in tuv.runs if type(run) == inline.run and run.text
                )
                # orig_text = "".join(run.text for run in tuv.runs if run.text)
                # print(f"orig_text:\n{orig_text}\n\nclean_text:\n{clean_text}")
                # return
                new_tmx.tus[itu].tuvs[ituv].runs = [inline.run(text=clean_text)]

    new_tmx.export(patched_file)


def check():
    src_tmx = load_tmx(source_file)
    new_tmx = load_tmx(patched_file)

    assert src_tmx.tus and new_tmx.tus

    print(f"src tus: {len(src_tmx.tus)}, new tus: {len(new_tmx.tus)}")
    print(
        f"src tuvs: {sum(len(tu.tuvs) for tu in src_tmx.tus)}, "
        f"new tuvs: {sum(len(tu.tuvs) for tu in new_tmx.tus)}"
    )


if __name__ == "__main__":
    main()
    # check()
