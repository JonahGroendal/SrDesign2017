__author__ = "Jonah Groendal"

import db

# Create database
db_object = db.PeptideDB(db_name="peptide")

# Import CSV files
db_object.import_dataset("../data/clean/allergenonline.csv", {
    "url": "http://www.allergenonline.org/celiacbrowse.shtml",
    "institution": "University of Nebraska-Lincoln",
    "authors": ["Richard Goodman", "John Wise", "Sreedevi Lalithambika"]
})
db_object.import_dataset("../data/clean/amper.csv", {
    "url": "http://www.cnbi2.com/cgi-bin/amp.pl",
    "institution": ("Division of Infectious Diseases, Department of Medicine, Faculty"
        " of Medicine, University of British Columbia, Vancouver, BC, Canada"),
    "authors": ["Fjell CD", "Hancock RE", "Cherkasov A"]
})
db_object.import_dataset("../data/clean/lamp.csv", {
    "url": "http://biotechlab.fudan.edu.cn/database/lamp/",
    "institution": "SLS, Fudan University",
    "authors": ["Dr. Qingshan Huang","Mrs. Xiaowei Zhao","Mr. Jinjiang Huang",
                "Mr. Hongyu Wu", "Dr. Hairong Lu", "Mr. Guodong Li"]
})
db_object.import_dataset("../data/clean/satpdb.csv",{
    "url": "http://crdd.osdd.net/raghava/satpdb/index.html",
    "institution": ("Raghava's Group, Bioinformatics Centre, Institute of"
        " Microbial Technology, Chandigarh, India."),
    "authors": ["Sandeep Singh", "Kumardeep Chaudhary", "Sandeep Kumar Dhanda",
                "Sherry Bhalla", "Salman Usmani", "Dr. Ankur Gautam", "Abhishek Tuknait",
                "Piyush Agrawal", "Deepika Mathur", "Dr. G.P.S. Raghava"]
})
db_object.import_dataset("../data/clean/kaliumdb.csv",{
    "url": "httpL//kaliumdb.org/",
    "institution": "Laboratory of Molecular Instruments for Neurobiology",
    "authors": ["Prof. Eugene V. Grishin","Prof. Jan Tytgat","Prof. Lourival D. Possani",
                "Prof. Ricardo C. Rodríguez de la Vega", "Prof. Yong-Hua Ji", "Dr. Florence Jungo"]
})
