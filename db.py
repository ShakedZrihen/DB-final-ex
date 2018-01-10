import mysql.connector
from mysql.connector import errorcode
from collections import OrderedDict
import datetime
from dateutil.relativedelta import relativedelta

DB_NAME = 'test'

config = {
    'user': 'root',
    'password': 'Shaked1234',
    'host': '127.0.0.1',
    'database': 'test',
    'raise_on_warnings': True,
}

TABLES = OrderedDict()

TABLES['SoftwareField'] = (
    "CREATE TABLE IF NOT EXISTS  `SoftwareField` ("
    "  `expertise` TEXT NOT NULL,"
    "  `fieldId` int NOT NULL AUTO_INCREMENT,"
    "  PRIMARY KEY (`fieldId`)"
    ") ENGINE=InnoDB DEFAULT CHARACTER SET utf8")

TABLES['Engineers'] = (
    "CREATE TABLE IF NOT EXISTS `Engineers` ("
    "  `firstName` TEXT NOT NULL,"
    "  `lastName` TEXT NOT NULL,"
    "  `engineerId` double NOT NULL,"
    "  `fieldId` int NOT NULL,"
    "  `adress` TEXT NOT NULL,"
    "  `birthDate` Date NOT NULL,"
    "  PRIMARY KEY (`engineerId`),"
    "  CONSTRAINT `engField_ibfk_1` FOREIGN KEY (`fieldId`) "
    "  REFERENCES `SoftwareField` (`fieldId`) ON DELETE RESTRICT ON UPDATE CASCADE"
    ") ENGINE=InnoDB DEFAULT CHARACTER SET utf8")

TABLES['projects'] = (
    "CREATE TABLE IF NOT EXISTS `projects` ("
    " `costumerName` TEXT NOT NULL," 
    " `name` TEXT NOT NULL," 
    " `startDate` Date NOT NULL," 
    " `description` TEXT," 
    " `projectId` int NOT NULL AUTO_INCREMENT," 
    " PRIMARY KEY (`projectId`)"
    ") ENGINE=INNODB DEFAULT CHARACTER SET utf8")


TABLES['phones'] = (
        " CREATE TABLE IF NOT EXISTS `phones` ("
        " `engineerId` double NOT NULL," 
        " `phoneNumber` char(10)," 
        " PRIMARY KEY (`phoneNumber`)," 
        "  CONSTRAINT `eng_phones_ibfk_1` FOREIGN KEY (`engineerId`) "
        " REFERENCES `Engineers`(`engineerId`) ON DELETE CASCADE ON UPDATE CASCADE"
        ") ENGINE=INNODB DEFAULT CHARACTER SET utf8")


TABLES['worksAt'] = (
    "CREATE TABLE IF NOT EXISTS `worksAt` ("
    "`engineerId` double," 
    "`projectId` int," 
    " PRIMARY KEY (`engineerId`, `projectId`), " 
    " CONSTRAINT `eng_project_ibfk_1` FOREIGN KEY (`engineerId`) "
    " REFERENCES Engineers (`engineerId`) ON DELETE CASCADE ON UPDATE CASCADE, " 
    " CONSTRAINT `eng_project_ibfk_2` FOREIGN KEY (`projectId`) "
    " REFERENCES `projects`(`projectId`) ON DELETE CASCADE ON UPDATE CASCADE"
    ") ENGINE=INNODB DEFAULT CHARACTER SET utf8")

TABLES["grades"] = (
    "CREATE TABLE IF NOT EXISTS  `grades` ("
    "`engineerId` double," 
    "`projectId` int," 
    "`month` Date," 
    "`grade` int," 
    "PRIMARY KEY (`month`, `projectId`, `engineerId`), " 
    " CONSTRAINT `grade_project_ibfk_1` FOREIGN KEY (`projectId`) "
    "REFERENCES `worksAt` (`projectId`) ON DELETE CASCADE ON UPDATE CASCADE, " 
    " CONSTRAINT `eng_project_grade_ibfk_2` FOREIGN KEY (`engineerId`) "
    "REFERENCES `worksAt`(`engineerId`) ON DELETE CASCADE ON UPDATE CASCADE"
    ") ENGINE=INNODB DEFAULT CHARACTER SET utf8")

TABLES["milestones"] = (
    "CREATE TABLE IF NOT EXISTS `milestones` ("
    "`date` Date," 
    "`amount` double,"
    "`description` TEXT," 
    "`projectId` int," 
    "PRIMARY KEY (`date`, `projectId`)," 
    " CONSTRAINT `miles_project_ibfk_1` FOREIGN KEY (`projectId`) "
    "REFERENCES `projects`(`projectId`) ON DELETE CASCADE ON UPDATE CASCADE"
    ") ENGINE=INNODB DEFAULT CHARACTER SET utf8")

TABLES["stages"] = (
    "CREATE TABLE IF NOT EXISTS `Stages` ("
    "`stageName` char(20)," 
    "`stageId` int NOT NULL AUTO_INCREMENT," 
    "`description` TEXT," 
    " PRIMARY KEY (`stageId`)" 
    ") ENGINE=INNODB DEFAULT CHARACTER SET utf8")

TABLES["tools"] = (
    "CREATE TABLE IF NOT EXISTS `tools` ("
    "`toolName` char(20)," 
    "`toolId` int NOT NULL AUTO_INCREMENT," 
    "`description` TEXT," 
    "PRIMARY KEY(`toolId`)" 
    ") ENGINE=INNODB DEFAULT CHARACTER SET utf8")

TABLES["tools-stages-project"] = (
    "CREATE TABLE IF NOT EXISTS `tools-stages-proj` ("
    "`toolId` int," 
    "`stageId` int,"
    "`projectId` int,"
    " PRIMARY KEY (`toolId`, `stageId`, `projectId`)," 
    " CONSTRAINT `tool_sp_ibfk_1` FOREIGN KEY (`toolId`) "
    "REFERENCES `tools`(`toolId`) ON DELETE CASCADE ON UPDATE CASCADE,"
    " CONSTRAINT `stage_tp_ibfk_1` FOREIGN KEY (`stageId`) "
    "REFERENCES `stages`(`stageId`) ON DELETE CASCADE ON UPDATE CASCADE,"
    " CONSTRAINT `proj_ts_ibfk_1` FOREIGN KEY (`projectId`) "
    "REFERENCES `projects`(`projectId`) ON DELETE CASCADE ON UPDATE CASCADE"
    ") ENGINE=INNODB DEFAULT CHARACTER SET utf8")


class MyDB:

    def __init__(self):
        self.db = None
        self.cur = None
        self.insert_into = {
            'engineers': self.insert_to_engineers,
            'projects': self.insert_to_projects,
            'SoftwareFields': self.insert_to_software_field,
            'stages': self.insert_to_stages,
            'tools': self.insert_to_tools,
            'milestones': self.insert_to_milestones,
            'worksAt': self.insert_to_worksat,
            'phones': self.insert_to_phones,
            'grade': self.insert_to_grades,
            'tools-stage-proj': self.insert_to_tools_stage_proj,
        }

    def insert_to_projects(self,
                           costumer_name=None,
                           name=None,
                           start_day=None,
                           description=None):
        add_to = ("INSERT INTO projects "
                  "(costumerName, name, startDate, description) "
                  "VALUES (%s,  %s, %s, %s)")
        data = (costumer_name, name, start_day, description)
        self.cur.execute(add_to, data)
        self.db.commit()

    def insert_to_grades(self,
                         engineer_id=None,
                         project_id=None,
                         grade=0,
                         month=None):
        add_to = ("INSERT INTO grades "
                  "(engineerId, projectId, month, grade) "
                  "VALUES (%s,  %s, %s, %s)")
        data = (engineer_id, project_id, grade, month)
        self.cur.execute(add_to, data)
        self.db.commit()

    def insert_to_milestones(self,
                             project_id=None,
                             date=None,
                             amount=0,
                             description=None):
        add_to = ("INSERT INTO milestones "
                  "(date, amount, description, projectId) "
                  "VALUES (%s,  %s, %s, %s)")
        data = (date, amount, description, project_id)
        self.cur.execute(add_to, data)
        self.db.commit()

    def insert_to_software_field(self,
                                 expertise=None):
        add_to = ("INSERT INTO SoftwareField "
                  "(expertise) "
                  "VALUES (%s)")
        data = (expertise,)
        self.cur.execute(add_to, data)
        self.db.commit()

    def insert_to_stages(self,
                         name=None,
                         description=None):
        add_to = ("INSERT INTO Stages "
                  "(stageName, description) "
                  "VALUES (%s, %s)")
        data = (name, description)
        self.cur.execute(add_to, data)
        self.db.commit()

    def insert_to_tools(self,
                        tool_name=None,
                        description=None):
        add_to = ("INSERT INTO tools"
                  "(toolName, description) "
                  "VALUES (%s,  %s)")
        data = (tool_name, description)
        self.cur.execute(add_to, data)
        self.db.commit()

    def insert_to_worksat(self,
                          engineer_id=None,
                          project_id=None):
        add_to = ("INSERT INTO worksAt"
                  "(engineerId, projectId)"
                  "VALUES (%s,  %s)")
        data = (engineer_id, project_id)
        self.cur.execute(add_to, data)
        self.db.commit()

    def insert_to_phones(self,
                         engineer_id=None,
                         phone_number='0521234567'):
        add_to = ("INSERT INTO phones"
                  "(engineerId, phoneNumber) "
                  "VALUES (%s,  %s)")
        data = (engineer_id, phone_number)
        self.cur.execute(add_to, data)
        self.db.commit()

    def insert_to_tools_stage_proj(self,
                                   tool_id=None,
                                   stage_id=None,
                                   project_id=None):
        add_to = ("INSERT INTO tools-stages-project "
                  "(toolId, stageId, projectId) "
                  "VALUES (%s,  %s, %s)")
        data_employee = (tool_id, stage_id, project_id)
        self.cur.execute(add_to, data_employee)
        self.db.commit()

    def insert_to_engineers(self,
                            first_name=None,
                            last_name=None,
                            engineer_id=None,
                            field_id=None,
                            address=None,
                            birthday=None):
        add_to = ("INSERT INTO Engineers "
                  "(firstName, lastName, engineerId, fieldId, adress, birthDate) "
                  "VALUES (%s,  %s, %s, %s, %s, %s)")
        data = (first_name, last_name, engineer_id, field_id, address, birthday)
        self.cur.execute(add_to, data)
        self.db.commit()

    def delete_from_engineer(self,
                             engineer_id):
        delete_from = "DELETE FROM Engineers WHERE engineerId=%s"
        self.cur.execute(delete_from, (engineer_id,))
        self.db.commit()

    def connect(self):
        try:
            self.db = mysql.connector.connect(**config)
            self.cur = self.db.cursor()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print "Bad username or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print "Database does not exist"
            else:
                print err
        else:
            print "db connected!"

    def close_connection(self):
        self.db.close()

    def init_db(self):
        global TABLES

        for name, ddl in TABLES.iteritems():
            try:
                print "Creating table {}: ".format(name),
                self.cur.execute(ddl)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print "already exists."
                else:
                    print(err.msg)
            else:
                print "OK"

    def init_data(self):
        # initialize Software fields
        self.insert_into["SoftwareFields"]("iOS")
        self.insert_into["SoftwareFields"]("Android")
        self.insert_into["SoftwareFields"]("C++")
        self.insert_into["SoftwareFields"]("C")
        self.insert_into["SoftwareFields"]("C#")
        self.insert_into["SoftwareFields"]("Python")
        self.insert_into["SoftwareFields"]("Scala")

        # initialize engineers
        self.insert_into["engineers"]("Shaked", "Zrihen", "312533011", 2, "Ramat Gan", '1994-2-05')
        self.insert_into["phones"]("312533011", "0532777866")
        self.insert_into["phones"]("312533011", "0532777867")

        self.insert_into["engineers"]("Noga", "Zohar", "311275929", 3, "Ramat Gan", '1994-1-11')
        self.insert_into["phones"]("311275929", "0546578900")

        self.insert_into["engineers"]("Lior", "Liora", "312533891", 4, "Raanana", '1990-2-05')
        self.insert_into["phones"]("312533891", "0532757866")

        self.insert_into["engineers"]("Noa", "Tamir", "312536011", 6, "Mattan", '1966-7-27')
        self.insert_into["phones"]("312536011", "0524509458")

        self.insert_into["engineers"]("moty", "Zrihen", "312533091", 2, "Yarhiv", '1965-5-31')
        self.insert_into["phones"]("312533091", "0522938601")

        self.insert_into["engineers"]("Rony", "Zrihen", "555533011", 2, "Mattan", '1999-1-30')
        self.insert_into["phones"]("555533011", "0524509453")

        # initialize projects table
        self.insert_into['projects'](costumer_name="Avichi", name="firstAssignment", start_day="2017-11-1", description="create table")
        self.insert_into['projects'](costumer_name="Avichi", name="finalProj", start_day="2018-1-10", description="final ex project")
        self.insert_into['worksAt'](engineer_id="312533011", project_id="1")

    def get_phones(self, engineer_id):
        if engineer_id:
            query = ("SELECT * FROM phones WHERE engineerId={};".format(engineer_id))
            print "query: {}".format(query)
            self.cur.execute(query)
            rows = {}
            for index, i in enumerate(self.cur.fetchall()):
                row = list(i)
                rows[str(index)] = str(row[1])
            return rows
        return None

    def show_table(self, table_name):
        query = ("SELECT * FROM " + table_name)
        self.cur.execute(query)
        if table_name == "Engineers":
            rows = []
            for i in self.cur.fetchall():
                engineer_row = list(i)
                now = datetime.date.today()
                age = relativedelta(now, engineer_row[5])
                engineer_row.append(age.years)
                engineer_row[5] = engineer_row[5].strftime("%d/%m/%Y")
                rows.append(engineer_row)
        elif table_name == "projects":
            rows = []
            for i in self.cur.fetchall():
                project_row = list(i)
                project_row[2] = project_row[2].strftime("%d/%m/%Y")
                rows.append(project_row)
        else:
            rows = [list(i) for i in self.cur.fetchall()]
        return rows

    def create_table(self, name, fields):
        pass



