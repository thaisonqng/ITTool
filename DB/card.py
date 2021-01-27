

class Card:
    def __init__(self):
        pass
    def __init__(self, staffID, cardID, fullName, position, department, date, picture):
        self.staffID = staffID
        self.cardID = cardID
        self.fullName = fullName
        self.position = position
        self.department = department
        self.date = date
        self.picture = picture

    def toList(self):
        list = []
        list.append(self.staffID)
        list.append(self.cardID)
        list.append(self.fullName)
        list.append(self.position)
        list.append(self.department)
        list.append(self.date)
        list.append(self.picture)
        return list


