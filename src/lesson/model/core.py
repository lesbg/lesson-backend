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
version = 2

import sys

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from sqlalchemy import Column, Integer, Unicode, Date, String, DateTime, UnicodeText, Float, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

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
    Version = Column(Integer, nullable=False)

    Link = "versions"

    def __repr__(self):
        return u"<Version('%s - %i')>" % (self.Type, self.Version)

    def __init__(self, UUID, Type, Version):
        self.UUID = UUID
        self.Type = Type
        self.Version = Version


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
        return u"<Year('%s')>" % (self.Year)

    def __init__(self, YearName, YearNumber):
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
    HighPriority = Column(Integer, nullable=False, default=0) # boolean

    Link = "SubjectTypes"

    def __repr__(self):
        return u"<SubjectType('%s')>" % (self.Title)

    def __init__(self, Title, ShortTitle=None, ID=None, Description=None, Weight=None, HighPriority=None):
        self.Title = Title
        self.ShortTitle = ShortTitle
        self.ID = ID
        self.Description = Description
        self.Weight = Weight
        self.HighPriority = HighPriority


class Grade(Base, TableTop):
    """
    This class contains a unique ordered grade number, the department that
    the grade is in, and a text description of the grade
    """

    __tablename__ = 'grade'

    GradeIndex = Column('Grade', Integer(11), nullable=False, autoincrement=False, primary_key=True) #Rename ASAP
    DepartmentIndex = Column(Integer(11), ForeignKey('department.DepartmentIndex'), nullable=False)
    GradeName = Column(Unicode(50), nullable=False)

    Department = relationship(Department, primaryjoin=DepartmentIndex == Department.DepartmentIndex, foreign_keys=[Department.DepartmentIndex], uselist=False)

    def __repr__(self):
        return u"<Grade('%s')>" % (self.GradeName)

    def __init__(self, GradeIndex, Department, Description):
        self.GradeIndex = GradeIndex
        self.DepartmentIndex = Department.DepartmentIndex
        self.Grade = Description


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

    Department = relationship(Department, primaryjoin=DepartmentIndex == Department.DepartmentIndex, foreign_keys=[Department.DepartmentIndex], uselist=False)

    def __repr__(self):
        return u"<Term('%s')>" % (self.TermName)

    def __init__(self, TermName, TermNumber, Department, HasConduct=True):
        self.TermName = TermName
        self.TermNumber = TermNumber
        self.DepartmentIndex = Department.DepartmentIndex
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
    NonmarkType = Column(Unicode(50), nullable=False)
    DepartmentIndex = Column(Integer, ForeignKey('department.DepartmentIndex'))

    Department = relationship(Department, primaryjoin=DepartmentIndex == Department.DepartmentIndex, foreign_keys=[Department.DepartmentIndex], uselist=False)

    Link = 'nonmark_types'

    def __repr__(self):
        return u"<NonmarkType('%s')>" % (self.NonmarkType)

    def __init__(self, NonmarkType, Department):
        self.NonmarkType = NonmarkType
        self.DepartmentIndex = Department.DepartmentIndex


class NonmarkIndex(Base, TableTop):
    """
    This class contains an auto-incrementing primary key, a mandatory
    description, and an optional applicable department
    """

    __tablename__ = 'nonmark_index'

    NonmarkIndex = Column(Integer, nullable=False, primary_key=True)
    NonmarkTypeIndex = Column(Integer, ForeignKey('nonmark_type.NonmarkTypeIndex'), nullable=False)
    Input = Column(Unicode(8))
    Display = Column(Unicode(8), nullable=False)
    MinScore = Column(Float)
    Value = Column(Float)

    NonmarkType = relationship(NonmarkType, primaryjoin=NonmarkTypeIndex == NonmarkType.NonmarkTypeIndex, foreign_keys=[NonmarkType.NonmarkTypeIndex], backref=backref('NonmarkIndexes', uselist=True), uselist=False)

    Link = 'nonmark_indexes'

    def __repr__(self):
        return u"<NonmarkIndex('%s: %s')>" % (self.NonmarkType.NonmarkType, self.Display)

    def __init__(self, NonmarkType, Display, Input=None, MinScore=None, Value=None):
        self.NonmarkTypeIndex = NonmarkType.NonmarkTypeIndex
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
    ActiveStudent = Column(Integer, default=0, nullable=False) #boolean
    ActiveTeacher = Column(Integer, default=0, nullable=False) #boolean
    SupportTeacher = Column(Integer, default=0, nullable=False) #boolean
    DepartmentIndex = Column(Integer, ForeignKey('department.DepartmentIndex'))
    User1 = Column(Integer) #boolean
    User2 = Column(Integer) #boolean
    User3 = Column(Integer) #boolean
    User4 = Column(Integer) #boolean
    User5 = Column(Integer) #boolean

    Department = relationship(Department, primaryjoin=DepartmentIndex == Department.DepartmentIndex, foreign_keys=[Department.DepartmentIndex], backref=backref('Users', uselist=True), uselist=False)

    Link = "users"

    def __init__(self, Username, FirstName, Surname):
        self.Username = Username
        self.FirstName = FirstName
        self.Surname = Surname

    def __repr__(self):
        return u"<User('%s %s (%s)')>" % (self.FirstName, self.Surname, self.Username)


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
    HasConduct = Column(Integer, nullable=False, default=1) #boolean

    Grade = relationship(Grade, primaryjoin=GradeIndex == Grade.GradeIndex, foreign_keys=[Grade.GradeIndex], uselist=False)
    Department = relationship(Department, primaryjoin=DepartmentIndex == Department.DepartmentIndex, foreign_keys=[Department.DepartmentIndex], uselist=False)
    Year = relationship(Year, primaryjoin=YearIndex == Year.YearIndex, foreign_keys=[Year.YearIndex], uselist=False)
    ClassTeacher = relationship(User, primaryjoin=ClassTeacherUsername == User.Username, foreign_keys=[User.Username], uselist=False)

    Link = "classes"

    def __repr__(self):
        return u"<Class('%s - %s')>" % (self.Year.Year, self.Class)

    def __init__(self, ClassName, Year, Department, Grade=None, ClassTeacher=None, HasConduct=True):
        self.ClassName = ClassName
        self.YearIndex = Year.YearIndex
        self.DepartmentIndex = Department.DepartmentIndex
        self.GradeIndex = Grade.GradeIndex
        if ClassTeacher != None:
            self.ClassTeacherUsername = ClassTeacher.Username
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
    CanDoReport = Column(Integer, nullable=False, default=0) #boolean
    ReportTemplate = Column(LargeBinary)
    ReportTemplateType = Column(Unicode(300))

    Class = relationship(Class, primaryjoin=ClassIndex == Class.ClassIndex, foreign_keys=[Class.ClassIndex], uselist=False)
    Term = relationship(Term, primaryjoin=TermIndex == Term.TermIndex, foreign_keys=[Term.TermIndex], uselist=False)
    AverageNM = relationship(NonmarkType, primaryjoin=AverageTypeIndex == NonmarkType.NonmarkTypeIndex, foreign_keys=[NonmarkType.NonmarkTypeIndex], uselist=False)
    ConductNM = relationship(NonmarkType, primaryjoin=AverageTypeIndex == NonmarkType.NonmarkTypeIndex, foreign_keys=[NonmarkType.NonmarkTypeIndex], uselist=False)
    EffortNM = relationship(NonmarkType, primaryjoin=AverageTypeIndex == NonmarkType.NonmarkTypeIndex, foreign_keys=[NonmarkType.NonmarkTypeIndex], uselist=False)

    def __repr__(self):
        return u"<ClassTerm('%s - %s - %s')>" % (self.Term.TermName, self.Class.Year.YearName, self.Class.ClassName)

    def __init__(self, Class, Term, AbsenceType=0, AverageType=0, ConductType=0, EffortType=0,
                       CTCommentType=0, HODCommentType=0, PrincipalCommentType=0,
                       AverageNM=None, ConductNM=None, EffortNM=None,
                       ReportTemplate=None, ReportTemplateType=None):
        self.ClassIndex = Class.ClassIndex
        self.TermIndex = Term.TermIndex
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
        if EffortNM != None:
            self.EffortTypeIndex = EffortNM.NonmarkTypeIndex
        if ConductNM != None:
            self.ConductTypeIndex = ConductNM.NonmarkTypeIndex


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
    CTCommentDone = Column(Integer, nullable=False, default=0) #boolean
    HODComment = Column(UnicodeText)
    HODCommentDone = Column(Integer, nullable=False, default=0) #boolean
    HODUsername = Column(Unicode(50), ForeignKey('user.Username'), nullable=False)
    PrincipalComment = Column(UnicodeText)
    PrincipalCommentDone = Column(Integer, nullable=False, default=0) # boolean
    PrincipalUsername = Column(Unicode(50), ForeignKey('user.Username'), nullable=False)
    ReportDone = Column(Integer, nullable=False, default=0) # boolean
    ReportProofread = Column(Integer, nullable=False, default=0) # boolean
    ReportProofDone = Column(Integer, nullable=False, default=0) # boolean
    ReportPrinted = Column(Integer, nullable=False, default=0) # boolean
    ClassOrder = Column(Integer)

    HOD = relationship(User, primaryjoin=HODUsername == User.Username, foreign_keys=[User.Username], uselist=False)
    Principal = relationship(User, primaryjoin=PrincipalUsername == User.Username, foreign_keys=[User.Username], uselist=False)
    User = relationship(User, primaryjoin=Username == User.Username, foreign_keys=[User.Username], uselist=False)
    ClassTerm = relationship(ClassTerm, primaryjoin=ClassTermIndex == ClassTerm.ClassTermIndex, foreign_keys=[ClassTerm.ClassTermIndex], uselist=False)

    def __repr__(self):
        return u"<ClassList('%s: %s - %s - %s')>" % (self.User.Username, self.ClassTerm.Term.TermName, self.ClassTerm.Class.Year.YearName, self.ClassTerm.Class.ClassName)

    def __init__(self, ClassTerm, User, ClassOrder=None):
        self.ClassTermIndex = ClassTerm.ClassTermIndex
        self.Username = User.Username
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

    Staff = relationship(User, primaryjoin=StaffUsername == User.Username, foreign_keys=[User.Username], uselist=False)
    Student = relationship(User, primaryjoin=StudentUsername == User.Username, foreign_keys=[User.Username], uselist=False)

    Link = "casenotes"

    def __repr__(self):
        return u"<Casenote('%s -> %s (%s)')>" % (self.StaffUsername, self.StudentUsername, self.Date)

    def __init__(self, Staff, Student, Level, Note, Date=datetime.now()):
        self.StaffUsername = Staff.Username
        self.StudentUsername = Student.Username
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

    User = relationship(User, primaryjoin=Username == User.Username, foreign_keys=[User.Username], backref=backref('Logs', uselist=True), uselist=False)

    Link = "logs"

    def __repr__(self):
        return u"<Log('%i - %s - %s')>" % (self.Level, self.Username, self.Comment)

    def __init__(self, Page, User, Level, RemoteHost, Comment=None):
        print sys.modules[__name__]
        if isinstance(User, unicode):
            username = User
        elif isinstance(User, sys.modules[__name__].User):
            username = User.Username
        else:
            raise TypeError("'User' must either be unicode string or model.core.User")

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
        if HostAddr is None:
            raise ValueError("Host address must be set")
        self.HostAddr = HostAddr
