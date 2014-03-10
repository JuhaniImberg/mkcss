"""Contains misc functions that generate CSS."""


def grid(css, slices=16, each=60, gutter=16):
    """Function to generate a grid"""

    css.selector(".container-{0}".format(slices), values={
        "margin": (0, "auto"),
        "width": slices * each
    })
    for index in range(1, slices + 1):
        css.selector(".grid-{0}".format(index), values={
            "width": index * each - gutter,
            "display": "inline-block",
            "margin": (0, gutter / 2),
            "padding": 0
        })
