import sys
from .file_class import Biofile
import pysam


class Bed(Biofile):
    """BED file"""

    def __init__(self, filepath):
        self.filepath = filepath

        self.check_existence()

    def coverage_at_position(self):
        samfile = pysam.AlignmentFile(self.filepath, 'rb')
        data = samfile.pileup("1", 100, 120)
        print(data)
        samfile.close()
