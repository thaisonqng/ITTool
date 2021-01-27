
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class Staff:
    def __init__(self,StaffID, FullName, Department, JobTitle):
        self.StaffID = StaffID
        self.FullName = FullName
        self.Department= Department
        self.JobTitle = JobTitle
    def __str__(self):
        return str(self.StaffID) +' ' +str(self.FullName)+' '+str(self.Department)+' '+ str(self.JobTitle)
    def toList(self):
        list=[]
        list.append(self.StaffID)
        list.append(self.FullName)
        list.append(self.Department)
        list.append(self.JobTitle)
        return list



