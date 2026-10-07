"""Create static font instances used to generate the glyphs.

Usage: python3 scripts/instance_fonts.py <Archivo-VF.ttf> <SourceSans3-VF.ttf> <outdir>
Archivo and Source Sans 3 are SIL Open Font License 1.1 fonts (Google Fonts).
MIT licence, The Lisbon Council 2026.
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

archivo, source, out = sys.argv[1:4]
jobs = [(archivo, {'wght': 700, 'wdth': 100}, 'Archivo Bold'),
        (archivo, {'wght': 800, 'wdth': 100}, 'Archivo ExtraBold'),
        (source, {'wght': 400}, 'Source Sans 3 Regular'),
        (source, {'wght': 600}, 'Source Sans 3 SemiBold')]
for src, loc, name in jobs:
    inst = instantiateVariableFont(TTFont(src), loc)
    fam, sty = name.rsplit(' ', 1)
    for rec in inst['name'].names:
        if rec.nameID in (1, 16):
            rec.string = fam
        elif rec.nameID in (2, 17):
            rec.string = sty
        elif rec.nameID == 4:
            rec.string = name
        elif rec.nameID == 6:
            rec.string = name.replace(' ', '-')
    inst.save(f"{out}/{name.replace(' ', '_')}.ttf")
    print('saved', name)
