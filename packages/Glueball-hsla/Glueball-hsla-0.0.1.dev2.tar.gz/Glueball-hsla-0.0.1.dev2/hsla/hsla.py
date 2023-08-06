"""A human-friendly system for HSLA colors in HTML"""


# The hues only shadow HTML color names, when they
# are identical in 100 saturation and 50 luminosity
HUES = {
    'red':          0,  # shadows HTML color name
    'scarlet':      10,
    'tangerine':    20,
    'carrot':       30,
    'amber':        40,
    'maize':        50,
    'yellow':       60,  # shadows HTML color name
    'apple':        70,
    'springbud':    80,
    'inchworm':     90,
    'pistacho':     100,
    'harlequin':    110,
    'lime':         120,  # shadows HTML color name
    'emerald':      130,
    'malachite':    140,
    'cadmium':      150,
    'jade':         160,
    'opal':         170,
    'cyan':         180,  # shadows HTML color name
    'cerulean':     190,
    'police':       200,
    'cobalt':       210,
    'sapphire':     220,
    'phthalo':      230,
    'blue':         240,  # shadows HTML color name
    'majorelle':    250,
    'lilac':        260,
    'mauve':        270,
    'wisteria':     280,
    'phlox':        290,
    'magenta':      300,  # shadows HTML color name
    'rose':         310,
    'candy':        320,
    'cerise':       330,
    'raspberry':    340,
    'amaranth':     350,
}


class Hsla:
    """Generates CSS hsl(a) color value as string representation.
    Depends on the HUES dictionary to produce human friendly names.

    Colors 'black', 'white' and 'gray' have a hue and saturation of 0.
    A luminisity of 0 defaults to 'black' and 100 to 'white';
    anything in between is treated as `gray`.

    suffix      The suffix attribute for use in selectors: yellow[sat]['-'lum]['-'alpha'a']
    _h          Hue - The value (0 to 360)
    _s          Saturation - The percentage as a value 0-100, defaults to 100
    _l          Luminosity - The percentage as a value 0-100, defaults to 50
    _a          Alpha - Value 0-100 translates to 0.0 to 1.0
    """
    def __init__(self, hue_name, sat=100, lum=50, alpha=100):
        if hue_name == 'black' or lum == 0:
            self._h = 0
            self._s = 0
            self._l = 0
            self.suffix = 'black'
        elif hue_name == 'white' or lum == 100:
            self._h = 0
            self._s = 0
            self._l = 100
            self.suffix = 'white'
        elif hue_name in ['grey', 'gray']:
            self._h = 0
            self._s = 0
            self._l = lum
            self.suffix = 'gray'
            if lum != 50:
                self.suffix = self.suffix + "-" + str(lum)
        else:
            self._h = HUES[hue_name]
            self._s = sat
            self._l = lum
            self.suffix = hue_name
            if sat != 100:
                self.suffix = self.suffix + str(sat)
            if lum != 50:
                self.suffix = self.suffix + "-" + str(lum)

        self._a = alpha
        if alpha != 100:
            self.suffix = self.suffix + "-" + str(alpha) + "a"

    def __str__(self):
        if self._a < 100:
            return 'hsla({:d}, {:d}%, {:d}%, {:.2f})'.format(self._h, self._s, self._l, self._a/100)
        return 'hsl({:d}, {:d}%, {:d}%)'.format(self._h, self._s, self._l)
