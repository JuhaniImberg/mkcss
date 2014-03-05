#!/usr/bin/env python2
# coding: utf-8

from mkcss import CSS, px
c = CSS()


def randomfunction():
    c("font-family", "monospace")


@c.selector(".header")
def header():
    c.comment(("This is a really important message!\n"
               "With several lines"))
    c("font-size", px(32))
    randomfunction()
    c("color", "#f8f8f8")


@c.selector("#mui", "#hei")
def muihei():
    randomfunction()
    c("box-shadow", px(3), px(2), px(1), "#333")

if __name__ == "__main__":
    c.comment("Mui maailma!\nmoi")
    c.make("mui.css")
