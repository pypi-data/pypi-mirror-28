"""NuMat's Powder X-ray Diffraction Module.

This module is used to convert .dat files into human readable formats (csv file
s, plots, etc.)
"""

import os


class NuPXRD(object):
    """
    Attributes:
        path - Path of PXRD DAT file, as a string.
        data - empty list
    """

    def __init__(self, path, mofname='', data=[]):
        """Returns a NuPXRD object.

        Args:
            path - Path of PXRD DAT file, as a string.
            mofname - Name of the MOF, as a string.
            data - Empty list.
        """
        self.path = path
        self.mofname = os.path.basename(path).split(".")[0]
        self.data = data

    def read_pxrd(self):
        """Parses a PXRD DAT file.

        Args:
            self.
        Returns:
            A nested list of the form [[x1, y1], [x2, y2], ...].
        """
        data = []
        with open(self.path) as in_file:
            for row in in_file:
                # Assignment - fill in the `data` variable
                if ";" not in row:
                    tmplist = [row.split()[0], row.split()[1]]
                    data.append(list(map(float, tmplist)))
                elif ";" in row:
                    tmplist = [row.split()[0].replace(";", ""),
                               " ".join(row.split()[2::])]
                    data.append(list(map(str, tmplist)))
        self.data = data

    def write_csv(self):
        """Writes a csv file.

        Args:
            self.
        Returns:
            A csv file.
        """
        with open('output_'+str(self.mofname)+'.csv', 'w') as output_file:
            output_file.write("\n".join(",".join(list(map(str, datum)))
                              for datum in self.data))


if __name__ == '__main__':
    NuPXRD()
