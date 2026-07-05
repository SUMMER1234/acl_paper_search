import time
import bibtexparser

class Load_Bib_file():
    def __init__(self):
        self.database_path = "anthology+abstracts.bib"
        with open(self.database) as acl_file:
            self.database = bibtexparser.load(acl_file)



if __name__ == '__main__':
    star_time = time.time()
    LBF = Load_Bib_file()
    end_time = time.time()
    print("Bib Database loaded")
    print("Time: "+str(end_time-star_time))