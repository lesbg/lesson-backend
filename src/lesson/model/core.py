# lesson/model/core.py
# 
# Core database configuration
# 
# This file is part of LESSON.  LESSON is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2 or later.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# 
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# 
# Copyright (C) 2012 Jonathan Dieter <jdieter@lesbg.com>

uuid = u'7bb2302a-a003-11e1-9b06-00163e9a5f9b'
version = 4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from sqlalchemy import Column, Integer, Unicode, Date, String, DateTime, UnicodeText, Float, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime, date

from controller import password

from model import TableTop

Base = declarative_base()

class Config(Base, TableTop):
    __tablename__ = 'config'

    ConfigIndex = Column(Integer, nullable=False, primary_key=True)
    UUID = Column(Unicode(36), nullable=False, index=True)
    Key = Column(Unicode(50), nullable=False, index=True)
    Value = Column(Unicode(1024), default=None)

    Link = "config"

    def __repr__(self):
        return u"<Config('%s: %s')>" % (self.Key, self.Value)

    def __init__(self, UUID, Key, Value):
        super(Config, self).__init__()
        type_check = {("UUID", unicode, False),
                      ("Key", unicode, False),
                      ("Value", unicode)}
        self.check_type(locals(), type_check)

        self.UUID = UUID
        self.Key = Key
        self.Value = Value


class Version(Base, TableTop):
    """
    This class contains a textual type, a UUID and the version of the item
    """

    __tablename__ = 'version'

    UUID = Column(Unicode(36), nullable=False, primary_key=True)
    Type = Column(Unicode(50), nullable=False)
    VersionNumber = Column(Integer, nullable=False)

    Link = "versions"

    def __repr__(self):
        return u"<Version('%s - %i')>" % (self.Type, self.Version)

    def __init__(self, UUID, Type, VersionNumber):
        super(Version, self).__init__()
        type_check = {("UUID", unicode, False),
                      ("Key", unicode, False),
                      ("VersionNumber", int, False)}
        self.check_type(locals(), type_check)

        self.UUID = UUID
        self.Type = Type
        self.VersionNumber = VersionNumber


class Year(Base, TableTop):
    """
    This class contains an auto-incrementing primary key, a number used for
    ordering the years, and a textual representation of the year
    """

    __tablename__ = 'year'

    YearIndex = Column(Integer, nullable=False, primary_key=True)
    YearNumber = Column(Integer, nullable=False)
    YearName = Column('Year', Unicode(50), nullable=False)

    Link = "years"

    def __repr__(self):
        return u"<Year('%s')>" % (self.YearName)

    def __init__(self, YearName, YearNumber):
        super(Year, self).__init__()
        type_check = {("YearName", unicode, False),
                      ("YearNumber", int, False)}
        self.check_type(locals(), type_check)

        self.YearName = YearName
        self.YearNumber = YearNumber


class Department(Base, TableTop):
    """
    This class contains an auto-incrementing primary key and a text
    representation of the department
    """

    __tablename__ = 'department'

    DepartmentIndex = Column(Integer, nullable=False, primary_key=True)
    DepartmentName = Column('Department', Unicode(50), nullable=False)

    Link = "departments"

    def __repr__(self):
        return u"<Department('%s')>" % (self.DepartmentName)

    def __init__(self, DepartmentName):
        super(Department, self).__init__()
        type_check = {("DepartmentName", unicode, False)}
        self.check_type(locals(), type_check)

        self.DepartmentName = DepartmentName


class SubjectType(Base, TableTop):
    """
    This class contains an auto-incrementing primary key, the title of the
    subject type, and miscellaneous other information about the subject type
    """
    __tablename__ = 'subjecttype'

    SubjectTypeIndex = Column(Integer, nullable=False, primary_key=True)
    Title = Column(Unicode(50), nullable=False)
    ShortTitle = Column(Unicode(50))
    ID = Column(Unicode(50))
    Description = Column(UnicodeText)
    Weight = Column(Integer)
    HighPriority = Column(Integer, nullable=False, default=0)  # boolean

    Link = "SubjectTypes"

    def __repr__(self):
        return u"<SubjectType('%s')>" % (self.Title)

    def __init__(self, Title, ShortTitle=None, ID=None, Description=None, Weight=None, HighPriority=False):
        super(SubjectType, self).__init__()
        type_check = {("Title", unicode, False),
                      ("ShortTitle", unicode),
                      ("ID", unicode),
                      ("Description", unicode),
                      ("Weight", int),
                      ("HighPriority", bool, False)}
        self.check_type(locals(), type_check)

        self.Title = Title
        self.ShortTitle = ShortTitle
        self.ID = ID
        self.Description = Description
        self.Weight = Weight
        if HighPriority:
            self.HighPriority = 1
        else:
            self.HighPriority = 0


class Grade(Base, TableTop):
    """
    This class contains a unique ordered grade number, the department that
    the grade is in, and a text description of the grade
    """

    __tablename__ = 'grade'

    GradeIndex = Column('Grade', Integer(11), nullable=False, autoincrement=False, primary_key=True)  # Rename ASAP
    DepartmentIndex = Column(Integer(11), ForeignKey('department.DepartmentIndex'), nullable=False)
    GradeName = Column(Unicode(50), nullable=False)

    DepartmentObject = relationship(Department, primaryjoin=DepartmentIndex == Department.DepartmentIndex, foreign_keys=[Department.DepartmentIndex], uselist=False)

    def __repr__(self):
        return u"<Grade('%s')>" % (self.GradeName)

    def __init__(self, GradeIndex, DepartmentObject, GradeName):
        super(Grade, self).__init__()
        type_check = {("GradeIndex", int, False),
                      ("DepartmentObject", Department, False),
                      ("GradeName", unicode, False)}
        self.check_type(locals(), type_check)

        self.GradeIndex = GradeIndex
        self.DepartmentIndex = DepartmentObject.DepartmentIndex
        self.GradeName = GradeName


class Term(Base, TableTop):
    """
    This class contains an auto-incrementing primary key, a number used for
    ordering the years, and a textual representation of the year
    """

    __tablename__ = 'term'

    TermIndex = Column(Integer(11), nullable=False, primary_key=True)
    TermNumber = Column(Integer(11), nullable=False)
    TermName = Column(Unicode(50), nullable=False)
    DepartmentIndex = Column(Integer(11), ForeignKey('department.DepartmentIndex'), nullable=False)
    HasConduct = Column(Integer(1), nullable=False, default=1)

    DepartmentObject = relationship(Department, primaryjoin=DepartmentIndex == Department.DepartmentIndex, foreign_keys=[Department.DepartmentIndex], uselist=False)

    def __repr__(self):
        return u"<Term('%s')>" % (self.TermName)

    def __init__(self, TermName, TermNumber, DepartmentObject, HasConduct=True):
        super(Term, self).__init__()
        type_check = {("TermName", unicode, False),
                      ("TermNumber", int, False),
                      ("DepartmentObject", Department, False),
                      ("HasConduct", bool, False)}
        self.check_type(locals(), type_check)

        self.TermName = TermName
        self.TermNumber = TermNumber
        self.DepartmentIndex = DepartmentObject.DepartmentIndex
        if HasConduct:
            self.HasConduct = 1
        else:
            self.HasConduct = 0


class NonmarkType(Base, TableTop):
    """
    This class contains an auto-incrementing primary key, a mandatory
    description, and an optional applicable department
    """
    __tablename__ = 'nonmark_type'

    NonmarkTypeIndex = Column(Integer, nullable=False, primary_key=True)
    NonmarkTypeName = Column('NonmarkType', Unicode(50), nullable=False)
    DepartmentIndex = Column(Integer, ForeignKey('department.DepartmentIndex'))

    DepartmentObject = relationship(Department, primaryjoin=DepartmentIndex == Department.DepartmentIndex, foreign_keys=[Department.DepartmentIndex], uselist=False)

    Link = 'nonmark_types'

    def __repr__(self):
        return u"<NonmarkType('%s')>" % (self.NonmarkTypeName)

    def __init__(self, NonmarkTypeName, DepartmentObject):
        super(NonmarkType, self).__init__()
        type_check = {("NonmarkTypeName", unicode, False),
                      ("DepartmentOjbect", Department)}
        self.check_type(locals(), type_check)

        self.NonmarkType = NonmarkType
        if DepartmentObject is not None:
            self.DepartmentIndex = DepartmentObject.DepartmentIndex
        else:
            self.DepartmentIndex = None


class Nonmark(Base, TableTop):
    """
    This class contains an auto-incrementing primary key, the applicable
    NonmarkTypeIndex, an optional input value for the nonmark, the display
    value, an optional minimum score for the nonmark and an optional value
    """

    __tablename__ = 'nonmark_index'

    NonmarkIndex = Column(Integer, nullable=False, primary_key=True)
    NonmarkTypeIndex = Column(Integer, ForeignKey('nonmark_type.NonmarkTypeIndex'), nullable=False)
    Input = Column(Unicode(8))
    Display = Column(Unicode(8), nullable=False)
    MinScore = Column(Float)
    Value = Column(Float)

    NonmarkTypeObject = relationship(NonmarkType, primaryjoin=NonmarkTypeIndex == NonmarkType.NonmarkTypeIndex, foreign_keys=[NonmarkType.NonmarkTypeIndex], backref=backref('Nonmarks', uselist=True), uselist=False)

    Link = 'nonmark_indexes'

    def __repr__(self):
        return u"<NonmarkIndex('%s: %s')>" % (self.NonmarkType.NonmarkType, self.Display)

    def __init__(self, NonmarkTypeObject, Display, Input=None, MinScore=None, Value=None):
        super(Nonmark, self).__init__()
        type_check = {("NonmarkTypeObject", NonmarkType, False),
                      ("Display", unicode, False),
                      ("Input", unicode),
                      ("MinScore", (int, long)),
                      ("Value", (int, long))}
        self.check_type(locals(), type_check)

        self.NonmarkTypeIndex = NonmarkTypeObject.NonmarkTypeIndex
        self.Display = Display
        self.Input = Input
        self.MinScore = MinScore
        self.Value = Value


class User(Base, TableTop):
    """
    This class contains most user information.  The primary key is the
    username, and mandatory fields include FirstName and Surname
    """

    __tablename__ = 'user'

    Username = Column(Unicode(50), nullable=False, primary_key=True)
    FirstName = Column(Unicode(50), nullable=False)
    Surname = Column(Unicode(50), nullable=False)
    Gender = Column(Unicode(1))
    PhoneNumber = Column(Unicode(20))
    CellNumber = Column(Unicode(20))
    DOB = Column(Date)
    Password = Column(String(255))
    Password2 = Column(String(255))
    Permissions = Column(Integer, default=0, nullable=False)
    Title = Column(Unicode(10))
    House = Column(Unicode(1))
    Email = Column(Unicode(256))
    DateType = Column(Integer)
    DateSeparator = Column(Unicode(1))
    ActiveStudent = Column(Integer, default=0, nullable=False)  # boolean
    ActiveTeacher = Column(Integer, default=0, nullable=False)  # boolean
    SupportTeacher = Column(Integer, default=0, nullable=False)  # boolean
    DepartmentIndex = Column(Integer, ForeignKey('department.DepartmentIndex'))
    User1 = Column(Integer)  # boolean
    User2 = Column(Integer)  # boolean
    User3 = Column(Integer)  # boolean
    User4 = Column(Integer)  # boolean
    User5 = Column(Integer)  # boolean

    DepartmentObject = relationship(Department, primaryjoin=DepartmentIndex == Department.DepartmentIndex, foreign_keys=[Department.DepartmentIndex], backref=backref('Users', uselist=True), uselist=False)

    Link = "users"

    def __repr__(self):
        return u"<User('%s %s (%s)')>" % (self.FirstName, self.Surname, self.Username)

    def __init__(self, Username, FirstName, Surname, Gender=None,
                 PhoneNumber=None, CellNumber=None, DOB=None, Password=None,
                 Password2=None, Permissions=0, Title=None, House=None,
                 Email=None, DateType=None, DateSeparator=None,
                 ActiveStudent=False, ActiveTeacher=False, SupportTeacher=False,
                 DepartmentObject=None, User1=None, User2=None, User3=None,
                 User4=None, User5=None):
        super(User, self).__init__()
        type_check = {("Username", unicode, False),
                      ("FirstName", unicode, False),
                      ("Surname", unicode, False),
                      ("Gender", unicode),
                      ("PhoneNumber", unicode),
                      ("CellNumber", unicode),
                      ("DOB", date),
                      ("Password", unicode),
                      ("Password2", unicode),
                      ("Permissions", int, False),
                      ("Title", unicode),
                      ("House", unicode),
                      ("Email", unicode),
                      ("DateType", int),
                      ("DateSeparator", unicode),
                      ("ActiveStudent", bool, False),
                      ("ActiveTeacher", bool, False),
                      ("SupportTeacher", bool, False),
                      ("DepartmentObject", Department),
                      ("User1", bool),
                      ("User2", bool),
                      ("User3", bool),
                      ("User4", bool),
                      ("User5", bool)}
        self.check_type(locals(), type_check)

        self.Username = Username
        self.FirstName = FirstName
        self.Surname = Surname
        self.Gender = Gender
        self.PhoneNumber = PhoneNumber
        self.CellNumber = CellNumber
        self.DOB = DOB
        if Password is not None:
            self.Password = password.encrypt(Password)
        else:
            self.Password = None
        if Password2 is not None:
            self.Password2 = password.encrypt(Password2)
        else:
            self.Password2 = None
        self.Permissions = Permissions
        self.Title = Title
        self.House = House
        self.Email = Email
        self.DateType = DateType
        self.DateSeparator = DateSeparator
        if ActiveStudent:
            self.ActiveStudent = 1
        else:
            self.ActiveStudent = 0
        if ActiveTeacher:
            self.ActiveTeacher = 1
        else:
            self.ActiveTeacher = 0
        if SupportTeacher:
            self.SupportTeacher = 1
        else:
            self.SupportTeacher = 0
        if DepartmentObject is not None:
            self.DepartmentIndex = DepartmentObject.DepartmentIndex
        else:
            self.DepartmentIndex = None
        if User1 is not None:
            if User1:
                self.User1 = 1
            else:
                self.User1 = 0
        else:
            self.User1 = None
        if User2 is not None:
            if User2:
                self.User2 = 1
            else:
                self.User2 = 0
        else:
            self.User2 = None
        if User3 is not None:
            if User3:
                self.User3 = 1
            else:
                self.User3 = 0
        else:
            self.User3 = None
        if User4 is not None:
            if User4:
                self.User4 = 1
            else:
                self.User4 = 0
        else:
            self.User4 = None
        if User5 is not None:
            if User5:
                self.User5 = 1
            else:
                self.User5 = 0
        else:
            self.User5 = None


class Class(Base, TableTop):
    """
    This class contains information about each class.  The primary key is
    auto-incrementing, and mandatory fields include Class, YearIndex and
    DepartmentIndex
    """

    __tablename__ = 'class'

    ClassIndex = Column(Integer, nullable=False, primary_key=True)
    GradeIndex = Column('Grade', Integer, ForeignKey('grade.Grade'))
    ClassName = Column(Unicode(50), nullable=False)
    YearIndex = Column(Integer, ForeignKey('year.YearIndex'), nullable=False)
    ClassTeacherUsername = Column(Unicode(50), ForeignKey('user.Username'))
    DepartmentIndex = Column(Integer, ForeignKey('department.DepartmentIndex'), nullable=False)
    HasConduct = Column(Integer, nullable=False, default=1)  # boolean

    GradeObject = relationship(Grade, primaryjoin=GradeIndex == Grade.GradeIndex, foreign_keys=[Grade.GradeIndex], uselist=False)
    DepartmentObject = relationship(Department, primaryjoin=DepartmentIndex == Department.DepartmentIndex, foreign_keys=[Department.DepartmentIndex], uselist=False)
    YearObject = relationship(Year, primaryjoin=YearIndex == Year.YearIndex, foreign_keys=[Year.YearIndex], uselist=False)
    ClassTeacherObject = relationship(User, primaryjoin=ClassTeacherUsername == User.Username, foreign_keys=[User.Username], uselist=False)

    Link = "classes"

    def __repr__(self):
        return u"<Class('%s - %s')>" % (self.Year.YearName, self.ClassName)

    def __init__(self, ClassName, YearObject, DepartmentObject, GradeObject=None, ClassTeacherObject=None, HasConduct=True):
        super(Class, self).__init__()
        type_check = {("ClassName", unicode, False),
                      ("YearObject", Year, False),
                      ("DepartmentObject", Department, False),
                      ("GradeObject", Grade),
                      ("ClassTeacherObject", User),
                      ("HasConduct", bool, False)}
        self.check_type(locals(), type_check)

        self.ClassName = ClassName
        self.YearIndex = YearObject.YearIndex
        self.DepartmentIndex = DepartmentObject.DepartmentIndex
        if GradeObject is not None:
            self.GradeIndex = GradeObject.GradeIndex
        else:
            self.GradeIndex = None
        if ClassTeacherObject is not None:
            self.ClassTeacherUsername = ClassTeacherObject.Username
        else:
            self.ClassTeacherUsername = None
        if HasConduct:
            self.HasConduct = 1
        else:
            self.HasConduct = 0


class ClassTerm(Base, TableTop):
    """
    This class contains information about each class.  The primary key is
    auto-incrementing, and mandatory fields include Class, YearIndex and
    DepartmentIndex
    """

    __tablename__ = 'classterm'

    ClassTermIndex = Column(Integer, nullable=False, primary_key=True)
    ClassIndex = Column(Integer, ForeignKey('class.ClassIndex'), nullable=False)
    TermIndex = Column(Integer, ForeignKey('term.TermIndex'), nullable=False)
    AbsenceType = Column(Integer, nullable=False, default=0)
    AverageType = Column(Integer, nullable=False, default=0)
    ConductType = Column(Integer, nullable=False, default=0)
    EffortType = Column(Integer, nullable=False, default=0)
    Average = Column(Float)
    Effort = Column(Float)
    Conduct = Column(Float)
    AverageTypeIndex = Column(Integer, ForeignKey('nonmark_type.NonmarkTypeIndex'))
    ConductTypeIndex = Column(Integer, ForeignKey('nonmark_type.NonmarkTypeIndex'))
    EffortTypeIndex = Column(Integer, ForeignKey('nonmark_type.NonmarkTypeIndex'))
    CTCommentType = Column(Integer, nullable=False, default=0)
    HODCommentType = Column(Integer, nullable=False, default=0)
    PrincipalCommentType = Column(Integer, nullable=False, default=0)
    CanDoReport = Column(Integer, nullable=False, default=0)  # boolean
    ReportTemplate = Column(LargeBinary)
    ReportTemplateType = Column(Unicode(300))

    ClassObject = relationship(Class, primaryjoin=ClassIndex == Class.ClassIndex, foreign_keys=[Class.ClassIndex], uselist=False)
    TermObject = relationship(Term, primaryjoin=TermIndex == Term.TermIndex, foreign_keys=[Term.TermIndex], uselist=False)
    AverageNM = relationship(NonmarkType, primaryjoin=AverageTypeIndex == NonmarkType.NonmarkTypeIndex, foreign_keys=[NonmarkType.NonmarkTypeIndex], uselist=False)
    ConductNM = relationship(NonmarkType, primaryjoin=AverageTypeIndex == NonmarkType.NonmarkTypeIndex, foreign_keys=[NonmarkType.NonmarkTypeIndex], uselist=False)
    EffortNM = relationship(NonmarkType, primaryjoin=AverageTypeIndex == NonmarkType.NonmarkTypeIndex, foreign_keys=[NonmarkType.NonmarkTypeIndex], uselist=False)

    def __repr__(self):
        return u"<ClassTerm('%s - %s - %s')>" % (self.TermObject.TermName, self.ClassObject.YearObject.YearName, self.ClassObject.ClassName)

    def __init__(self, ClassObject, TermObject, AbsenceType=0, AverageType=0,
                 ConductType=0, EffortType=0, CTCommentType=0,
                 HODCommentType=0, PrincipalCommentType=0, AverageNM=None,
                 ConductNM=None, EffortNM=None, ReportTemplate=None,
                 ReportTemplateType=None):
        super(ClassTerm, self).__init__()
        type_check = {("ClassObject", Class, False),
                      ("TermObject", Term, False),
                      ("AbsenceType", int, False),
                      ("AverageType", int, False),
                      ("ConductType", int, False),
                      ("EffortType", int, False),
                      ("CTCommentType", int, False),
                      ("HODCommentType", int, False),
                      ("PrincipalCommentType", int, False),
                      ("AverageNM", NonmarkType),
                      ("ConductNM", NonmarkType),
                      ("EffortNM", NonmarkType),
                      ("ReportTemplate", str),
                      ("ReportTemplateType", unicode)}
        self.check_type(locals(), type_check)

        self.ClassIndex = ClassObject.ClassIndex
        self.TermIndex = TermObject.TermIndex
        self.AbsenceType = AbsenceType
        self.AverageType = AverageType
        self.ConductType = ConductType
        self.EffortType = EffortType
        self.CTCommentType = CTCommentType
        self.HODCommentType = HODCommentType
        self.PrincipalCommentType = PrincipalCommentType
        self.ReportTemplate = ReportTemplate
        self.ReportTemplateType = ReportTemplateType
        if AverageNM != None:
            self.AverageTypeIndex = AverageNM.NonmarkTypeIndex
        else:
            self.AverageTypeIndex = None
        if EffortNM != None:
            self.EffortTypeIndex = EffortNM.NonmarkTypeIndex
        else:
            self.EffortTypeIndex = None
        if ConductNM != None:
            self.ConductTypeIndex = ConductNM.NonmarkTypeIndex
        else:
            self.ConductTypeIndex = None

class SupportClass(Base, TableTop):
    __tablename__ = u'support_class'

    SupportClassIndex = Column(Integer, nullable=False, primary_key=True)
    Username = Column(Unicode(50), ForeignKey('user.Username'), nullable=False)
    ClassTermIndex = Column(Integer, ForeignKey('classterm.ClassTermIndex'), nullable=False)

    UserObject = relationship(User, primaryjoin=Username == User.Username, foreign_keys=[User.Username], uselist=False)
    ClassTermObject = relationship(ClassTerm, primaryjoin=ClassTermIndex == ClassTerm.ClassTermIndex, foreign_keys=[ClassTerm.ClassTermIndex], uselist=False)

    Link = 'support_class'

    def __repr__(self):
        return u"<SupportClass('%s: %s - %s - %s')>" % (self.UserObject.Username, self.ClassTermObject.Term.TermName, self.ClassTermObject.ClassObject.YearObject.YearName, self.ClassTermObject.ClassObject.ClassName)

    def __init__(self, ClassTermObject, UserObject):
        super(ClassList, self).__init__()
        type_check = {("ClassTermObject", ClassTerm, False),
                      ("UserObject", User, False)}
        self.check_type(locals(), type_check)

        self.ClassTermIndex = ClassTermObject.ClassTermIndex
        self.Username = UserObject.Username

class ClassList(Base, TableTop):
    """
    This class contains information about each class.  The primary key is
    auto-incrementing, and mandatory fields include Class, YearIndex and
    DepartmentIndex
    """

    __tablename__ = 'classlist'

    ClassListIndex = Column(Integer, nullable=False, primary_key=True)
    ClassTermIndex = Column(Integer, ForeignKey('classterm.ClassTermIndex'), nullable=False)
    Username = Column(Unicode(50), ForeignKey('user.Username'), nullable=False)
    Average = Column(Float, nullable=False, default= -1)
    Conduct = Column(Float, nullable=False, default= -1)
    Effort = Column(Float, nullable=False, default= -1)
    Rank = Column(Integer, nullable=False, default= -1)
    Absences = Column(Integer, nullable=False, default= -1)
    CTComment = Column(UnicodeText)
    CTCommentDone = Column(Integer, nullable=False, default=0)  # boolean
    HODComment = Column(UnicodeText)
    HODCommentDone = Column(Integer, nullable=False, default=0)  # boolean
    HODUsername = Column(Unicode(50), ForeignKey('user.Username'), nullable=False)
    PrincipalComment = Column(UnicodeText)
    PrincipalCommentDone = Column(Integer, nullable=False, default=0)  # boolean
    PrincipalUsername = Column(Unicode(50), ForeignKey('user.Username'), nullable=False)
    ReportDone = Column(Integer, nullable=False, default=0)  # boolean
    ReportProofread = Column(Integer, nullable=False, default=0)  # boolean
    ReportProofDone = Column(Integer, nullable=False, default=0)  # boolean
    ReportPrinted = Column(Integer, nullable=False, default=0)  # boolean
    ClassOrder = Column(Integer)

    HODObject = relationship(User, primaryjoin=HODUsername == User.Username, foreign_keys=[User.Username], uselist=False)
    PrincipalObject = relationship(User, primaryjoin=PrincipalUsername == User.Username, foreign_keys=[User.Username], uselist=False)
    UserObject = relationship(User, primaryjoin=Username == User.Username, foreign_keys=[User.Username], uselist=False)
    ClassTermObject = relationship(ClassTerm, primaryjoin=ClassTermIndex == ClassTerm.ClassTermIndex, foreign_keys=[ClassTerm.ClassTermIndex], uselist=False)

    def __repr__(self):
        return u"<ClassList('%s: %s - %s - %s')>" % (self.UserObject.Username, self.ClassTermObject.Term.TermName, self.ClassTermObject.ClassObject.YearObject.YearName, self.ClassTermObject.ClassObject.ClassName)

    def __init__(self, ClassTermObject, UserObject, ClassOrder=None):
        super(ClassList, self).__init__()
        type_check = {("ClassTermObject", ClassTerm, False),
                      ("UserObject", User, False),
                      ("ClassOrder", int)}
        self.check_type(locals(), type_check)

        self.ClassTermIndex = ClassTermObject.ClassTermIndex
        self.Username = UserObject.Username
        self.ClassOrder = ClassOrder


class Casenote(Base, TableTop):
    """
    This class contains casenotes.  The primary key is auto-incrementing, and
    mandatory fields include WorkerUsername, StudentUsername, Date and Level
    """

    __tablename__ = 'casenote'

    CasenoteIndex = Column('CaseNoteIndex', Integer(11), nullable=False, primary_key=True)
    CasenoteGroup = Column('CaseNoteGroup', Integer(11))
    StaffUsername = Column('WorkerUsername', Unicode(50), ForeignKey('user.Username'), nullable=False)
    StudentUsername = Column(Unicode(50), ForeignKey('user.Username'), nullable=False)
    Note = Column(UnicodeText)
    Date = Column(DateTime, nullable=False)
    Level = Column(Integer, nullable=False, default=1)

    StaffObject = relationship(User, primaryjoin=StaffUsername == User.Username, foreign_keys=[User.Username], uselist=False)
    StudentObject = relationship(User, primaryjoin=StudentUsername == User.Username, foreign_keys=[User.Username], uselist=False)

    Link = "casenotes"

    def __repr__(self):
        return u"<Casenote('%s -> %s (%s)')>" % (self.StaffUsername, self.StudentUsername, self.Date)

    def __init__(self, StaffObject, StudentObject, Level, Note, Date=datetime.now()):
        super(Casenote, self).__init__()
        type_check = {("StaffObject", User, False),
                      ("StudentObject", User, False),
                      ("Level", int, False),
                      ("Note", unicode),
                      ("Date", datetime, False)}
        self.check_type(locals(), type_check)

        self.StaffUsername = StaffObject.Username
        self.StudentUsername = StudentObject.Username
        self.Level = Level
        self.Note = Note
        self.Date = Date


class Log(Base, TableTop):
    __tablename__ = 'log'

    LogIndex = Column(Integer, nullable=False, primary_key=True)
    Username = Column(Unicode(50), nullable=False)
    Level = Column(Integer, nullable=False)
    Time = Column(DateTime, nullable=False)
    Comment = Column(UnicodeText)
    Page = Column(UnicodeText, nullable=False)
    RemoteHost = Column(UnicodeText, nullable=False)

    UserObject = relationship(User, primaryjoin=Username == User.Username, foreign_keys=[User.Username], backref=backref('Logs', uselist=True), uselist=False)

    Link = "logs"

    def __repr__(self):
        return u"<Log('%i - %s - %s')>" % (self.Level, self.Username, self.Comment)

    def __init__(self, Page, UserObject, Level, RemoteHost, Comment=None):
        super(Log, self).__init__()
        type_check = {("Page", unicode, False),
                      ("UserObject", (User, unicode), False),
                      ("Level", int, False),
                      ("RemoteHost", unicode, False),
                      ("Comment", unicode)}
        self.check_type(locals(), type_check)

        if isinstance(UserObject, unicode):
            username = UserObject
        else:  # isinstance(UserObject, User):
            username = UserObject.Username

        self.Username = username
        self.Level = Level
        self.Page = Page
        self.RemoteHost = RemoteHost
        self.Comment = Comment
        self.Time = datetime.now()


class LogIgnoreHost(Base, TableTop):
    __tablename__ = 'log_ignore_host'

    LogIgnoreHostIndex = Column(Integer, nullable=False, primary_key=True)
    HostAddr = Column(Unicode(32), nullable=False)

    Link = "ignore_hosts"

    def __repr__(self):
        return u"<LogIgnoreHost('%s')>" % (self.HostAddr)

    def __init__(self, HostAddr):
        super(LogIgnoreHost, self).__init__()
        type_check = {("HostAddr", unicode, False)}
        self.check_type(locals(), type_check)

        self.HostAddr = HostAddr

# Any changes to the Permission table *must* also be changed in model/__init__.py
class Permission(Base, TableTop):
    __tablename__ = u'permission'

    ConfigIndex = Column(Integer, nullable=False, primary_key=True)
    UUID = Column(Unicode(36), nullable=False, index=True)
    Type = Column(Unicode(50), nullable=False, index=True)
    Username = Column(Unicode(50), nullable=False, index=True)
    Level = Column(Integer, nullable=False, index=True)

    UserObject = relationship(User, primaryjoin=Username == User.Username, foreign_keys=[User.Username], backref=backref('PermissionList', uselist=True), uselist=False)

    Link = "permissions"

    def __repr__(self):
        return u"<Permission(%s - %s)>" % (self.Username, self.Type)

    def __init__(self, UUID, Type, UserObject, Level=1):
        super(Permission, self).__init__()
        type_check = {("UUID", unicode, False),
                      ("UserObject", (User, unicode), False),
                      ("Type", unicode, False)}
        self.check_type(locals(), type_check)

        if isinstance(UserObject, unicode):
            username = UserObject
        else:  # isinstance(UserObject, User):
            username = User.Username

        if Level == None:
            Level = 1
        self.UUID = UUID
        self.Type = Type
        self.Username = username
        self.Level = Level
