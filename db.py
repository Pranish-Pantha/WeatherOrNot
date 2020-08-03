import sqlite3
from sqlite3 import Error

class dbAccess:
    def __init__(self, db_file):
        self.connection = self.create_connection(db_file)

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn

    def make_db(self):

        makeInfoDB = """ CREATE TABLE IF NOT EXISTS userdata (
                            email text PRIMARY KEY,
                            zipcode integer NOT NULL,
                            name text NOT NULL,
                            asthma integer NOT NULL,
                            melanoma integer NOT NULL,
                            photoaging integer NOT NULL,
                            basal_cell_carcinoma integer NOT NULL,
                            dysautonomia integer NOT NULL,
                            lung_cancer integer NOT NULL,
                            pneumonia integer NOT NULL,
                            chronic_bronchitis integer NOT NULL,
                            cystic_fibrosis integer NOT NULL,
                            diabetes integer NOT NULL,
                            arthritis integer NOT NULL,
                            epilepsy integer NOT NULL,
                            migranes integer NOT NULL,
                            seasonal_allergic_rhinitis integer NOT NULL,
                            pollen_allergy integer NOT NULL,
                            dust_allergy integer NOT NULL,
                            albinism integer NOT NULL,
                            photodermatitis integer NOT NULL,
                            hyperhidrosis integer NOT NULL
                        ); """
        self.executeSQL(makeInfoDB)

    def executeSQL(self, command):
        try:
            c = self.connection.cursor()
            c.execute(command)
        except Error as e:
            print(e)

    def readColumn(self, email):
        readEntry = """ SELECT * FROM userdata WHERE email = '{}'; """.format(email)
        cur = self.connection.cursor()
        cur.execute(readEntry)
        rows = cur.fetchall()
        for row in rows:
            return row

    def printTable(self):
        readEntry = """ SELECT * FROM userdata;"""
        cur = self.connection.cursor()
        cur.execute(readEntry)
        rows = cur.fetchall()
        for row in rows:
            print(row)

    def updateEntry(self, email, data):
        formatList = data + [email]
        update = """ UPDATE userdata SET email='{}', zipcode={}, name='{}', asthma={}, melanoma={}, photoaging={}, basal_cell_carcinoma={}, dysautonomia={}, lung_cancer={}, pneumonia={},
                chronic_bronchitis={}, cystic_fibrosis={}, diabetes={}, arthritis={}, epilepsy={}, migranes={},
                seasonal_allergic_rhinitis={}, pollen_allergy={}, dust_allergy={}, albinism={}, photodermatitis={},
                hyperhidrosis={} WHERE email = '{}';
        """.format(*formatList)
        #print(update)
        self.executeSQL(update)

    def addEntry(self, data):
        addEntry = """ INSERT INTO userdata(email, zipcode, name, asthma, melanoma, photoaging, basal_cell_carcinoma, dysautonomia, lung_cancer, pneumonia,
                chronic_bronchitis, cystic_fibrosis, diabetes, arthritis, epilepsy, migranes,
                seasonal_allergic_rhinitis, pollen_allergy, dust_allergy, albinism, photodermatitis,
                hyperhidrosis)
                        VALUES('{}', {}, '{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});
        """.format(*data)
        self.executeSQL(addEntry)

    def closeConnection(self):
        self.connection.commit()
        self.connection.close()
