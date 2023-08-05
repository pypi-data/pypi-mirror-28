import os

class Biofile():
    def check_existence(self):
        """Check if file given by user exists
        """
        if not os.path.exists(self.filepath):
            raise Exception(f"File {self.filepath} does not exists")
