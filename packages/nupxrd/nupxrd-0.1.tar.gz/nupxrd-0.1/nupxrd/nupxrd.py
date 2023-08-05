"""NuMat's Powder X-ray Diffraction Module.

This module is used to convert .dat files into human readable formats (csv files, plots, etc.)
"""

class NuPXRD(object):
    """

    Attributes:
        Width:
    """

    def __init__(self, name, width, twotheta=[], intensity=[])
        """ """"
        self.width = width
        self.twotheta = twotheta
        self.intensity = intensity

    def read_pxrd(path):
        """Parses a PXRD DAT file.

        Args:
            path - Path of PXRD DAT file, as a string.
        Returns:
            A nested list of the form [[x1, y1], [x2, y2], ...]
        """
        data = []

        with open(path) as in_file:
            for row in in_file:
                # Assignment - fill in the `data` variable
                data=""
        return data

    def write_csv():
        with open('output.csv', 'w') as output_file:
            output_file.write(your_csv_string)



if __name__ == '__main__':
    print "NuXRD"
