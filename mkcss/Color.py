"""Contains the Color class."""

import colorsys
import struct
import base64


class Color(object):

    """Represents a CSS color. Internally HLS is used."""

    namedColors = {
        "white":    "FFFFFF",
        "silver":   "C0C0C0",
        "gray":     "808080",
        "black":    "000000",
        "red":      "FF0000",
        "maroon":   "800000",
        "yellow":   "FFFF00",
        "olive":    "808000",
        "lime":     "00FF00",
        "green":    "008000",
        "aqua":     "00FFFF",
        "teal":     "008080",
        "blue":     "0000FF",
        "navy":     "000080",
        "fuchsia":  "FF00FF",
        "purple":   "800080",
        "orange":   "FFA500"
    }

    def __init__(self, val):
        self.alpha = 1
        self.hls = (0, 0, 0)

        if len(val) > 0:
            if val.lower() in Color.namedColors:
                self.from_name(val.lower())
            elif '#' in val:
                self.from_hex(val)
            elif 'rgb' in val:
                val = val.lstrip('rgba(').rstrip(');').split(',')
                val = [int(x) for x in val]
                if len(val) == 3:
                    self.from_rgb(val[0], val[1], val[2])
                elif len(val) == 4:
                    self.from_rgb(val[0], val[1], val[2], val[3])
                else:
                    raise Exception("This seems really invalid!")
            elif 'hsl' in val:
                val = val.lstrip('hsla(').rstrip(');').split(',')
                hue = int(val[0])
                sat = int(val[1].rstrip("%"))
                lig = int(val[2].rstrip("%"))
                if len(val) == 3:
                    self.from_hsl(hue, sat, lig)
                elif len(val) == 4:
                    self.from_rgb(hue, sat, lig, int(val[3]))
                else:
                    raise Exception("This seems really invalid!")

    def from_name(self, name):
        """Get a color from a name"""
        name = name.lower()
        if name in Color.namedColors:
            hexrgb = Color.namedColors[name]
            try:
                what = hexrgb.decode('hex')
            except AttributeError:
                what = bytes.fromhex(hexrgb)
            rgb = struct.unpack('BBB', what)
            self.hls = colorsys.rgb_to_hls(
                rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
        else:
            raise Exception("I don't know such color.")

    def from_hex(self, hexstr):
        """Get a color from a hex string"""
        if '#' in hexstr:
            hexstr = hexstr.lstrip('#')
        what = None
        try:
            what = hexstr.decode('hex')
        except AttributeError:
            what = bytes.fromhex(hexstr)
        rgb = struct.unpack('BBB', what)
        rgb = [x / 255 for x in rgb]
        self.hls = colorsys.rgb_to_hls(rgb[0], rgb[1], rgb[2])

    def from_rgb(self, red, green, blue, alpha=1):
        """Get a color from r, g, b values"""
        if max(red, green, blue) > 1:
            red /= 255
            green /= 255
            blue /= 255
        self.hls = colorsys.rgb_to_hls(red, green, blue)
        self.alpha = alpha

    def from_hsl(self, hue, saturation, lightness, alpha=1):
        """Get a color from h, s, l values"""
        if max(hue, saturation, lightness) > 1:
            hue /= 360
            saturation /= 100
            lightness /= 100
        self.hls = (hue, lightness, saturation)
        self.alpha = alpha

    def rgb(self):
        """Returns a rgb() or rgba() string from this color."""
        rgb = colorsys.hls_to_rgb(self.hls[0], self.hls[1], self.hls[2])
        red = int(rgb[0] * 255)
        green = int(rgb[1] * 255)
        blue = int(rgb[2] * 255)

        if self.alpha == 1:
            return "rgb({0},{1},{2})".format(red, green, blue)
        else:
            return "rgba({0},{1},{2},{3})".format(red, green, blue, self.alpha)

    def hsl(self):
        """Returns a hsl() or hsla() string from this color."""
        hue = int(self.hls[0] * 360)
        saturation = str(int(self.hls[2] * 100)) + "%"
        lightness = str(int(self.hls[1] * 100)) + "%"
        if self.alpha == 1:
            return "hsl({0},{1},{2})".format(hue, saturation, lightness)
        else:
            return "hsla({0},{1},{2},{3})".format(
                hue, saturation, lightness, self.alpha)

    def hexrgb(self):
        """Returns a hex string from this color."""
        rgb = colorsys.hls_to_rgb(self.hls[0], self.hls[1], self.hls[2])
        rgb = [int(round(x * 255)) for x in rgb]
        try:
            return "#" + "".join([chr(x) for x in rgb]).encode('hex')
        except LookupError:
            return (b'#' + base64.b16encode(bytes(rgb))).decode()

    def light(self):
        """Is this color light?"""
        return self.hls[1] > 0.5

    def dark(self):
        """Is this color dark?"""
        return not self.light()

    def lighten(self, amount=0.1):
        """Returns a new color that has been lightened by amount"""
        tmpcol = Color("")
        tmpcol.from_hsl(self.hls[0],
                        self.hls[2],
                        self.hls[1] * (1 + amount) if self.hls[
                        1] != 0 else amount,
                        self.alpha)
        return tmpcol

    def darken(self, amount=0.1):
        """Returns a new color that has been darkened by amount"""
        return self.lighten(-amount)
