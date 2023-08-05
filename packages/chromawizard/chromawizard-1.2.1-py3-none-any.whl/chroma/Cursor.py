from PyQt5 import QtGui

class CustomCursor:
    def __init__(self, type="CIRCLE"):
        pix_circle = [
"12 12 2 1",
"       c None",
".      c #FF0000",
"   ......   ",
"  .      .  ",
" .        . ",
".          .",
".          .",
".          .",
".          .",
".          .",
".          .",
" .        . ",
"  .      .  ",
"   ......   "]

        pix_new = [
"16 16 3 1",
"       c None",
".      c #000000",
"X      c #FFFFFF",
"                ",
"   ......       ",
"   .XXX.X.      ",
"   .XXX.XX.     ",
"   .XXX.XXX.    ",
"   .XXX.....    ",
"   .XXXXXXX.    ",
"   .XXXXXXX.    ",
"   .XXXXXXX.    ",
"   .XXXXXXX.    ",
"   .XXXXXXX.    ",
"   .XXXXXXX.    ",
"   .XXXXXXX.    ",
"   .........    ",
"                ",
"                "
]

        pix_plus1 = [
"11 9 3 1",
"       c None",
".      c #FFFFAA",
"a      c #FFFFFF",
"aaa        ",
"a   ...    ",
"a   ...    ",
"  .......  ",
"  .......  ",
"  .......  ",
"    ...    ",
"    ...    ",
"           "]

        pix_plus2 = [
"11 9 3 1",
"       c None",
".      c #AAFFFF",
"a      c #FFFFFF",
"aaa        ",
"a   ...    ",
"a   ...    ",
"  .......  ",
"  .......  ",
"  .......  ",
"    ...    ",
"    ...    ",
"           "]

        pix_minus1 = [
"11 9 3 1",
"       c None",
".      c #FFFFAA",
"a      c #FFFFFF",
"aaa        ",
"a          ",
"a          ",
"  .......  ",
"  .......  ",
"  .......  ",
"           ",
"           ",
"           "]

        pix_minus2 = [
"11 9 3 1",
"       c None",
".      c #AAFFFF",
"a      c #FFFFFF",
"aaa        ",
"a          ",
"a          ",
"  .......  ",
"  .......  ",
"  .......  ",
"           ",
"           ",
"           "]

        pix_draw1 = [
"11 9 2 1",
"       c None",
"a      c #FFFFFF",
"aaa        ",
"aa         ",
"a a        ",
"   a       ",
"    a      ",
"     a     ",
"      a    ",
"       a   ",
"        a  "]


        if type == "CIRCLE":
            pix = QtGui.QPixmap(pix_circle)
        elif type == "NEW":
            pix = QtGui.QPixmap(pix_new)
        elif type == "PLUS1":
            pix = QtGui.QPixmap(pix_plus1)
        elif type == "PLUS2":
            pix = QtGui.QPixmap(pix_plus2)
        elif type == "MINUS1":
            pix = QtGui.QPixmap(pix_minus1)
        elif type == "MINUS2":
            pix = QtGui.QPixmap(pix_minus2)
        elif type == "DRAW1":
            pix = QtGui.QPixmap(pix_draw1)

        self.cursor = QtGui.QCursor(pix, 0, 0)