# lesson/database.py
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

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, object_mapper

from sqlalchemy import Column, Integer, Unicode, Date, String, DateTime, UnicodeText, Float, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Session(object):
    def __init__(self, engine, **engine_opts):
        self.engine = create_engine(engine, **engine_opts)
        self.create_session = sessionmaker(bind=self.engine)  

class TableTop(object):
    def _get_list_link(self):
        if not hasattr(self, "Link"):
            return None
        return u"%s" % (self.Link)
    
    def _get_obj_link(self):
        if self.get_list_link() is None:
            return None
        return u"%s/%s" % (self.Link, unicode(self.get_primary_key()[1]))

    def _get_attr_link(self):
        if self.get_obj_link() is None:
            return None
        return u"%s/attributes" % (self.get_obj_link())

    def get_list_link(self):
        return self._get_list_link()
    
    def get_obj_link(self):
        return self._get_obj_link()
    
    def get_attr_link(self):
        return self._get_attr_link()
    
    def get_primary_key(self):
        mapper = object_mapper(self)
        return (unicode(mapper.primary_key[0].key), mapper.primary_key_from_instance(self)[0])

class Config(Base):
    __tablename__ = 'config'
    
    ConfigIndex = Column(Integer, nullable=False, primary_key=True)
    UUID        = Column(Unicode(36), nullable=False)
    Key         = Column(Unicode(50), nullable=False)
    Value       = Column(Unicode(1024), default=None)
    
    Link        = "config"
    
    def __repr__(self):
        return u"<Config('%s: %s')>" % (self.Key, self.UUID)
    
    def __init__(self, uuid, key, value):
        self.UUID  = uuid
        self.Key   = key
        self.Value = value

class Version(Base, TableTop):
    """
    This class contains a textual type, a UUID and the version of the item
    """
    __tablename__ = 'version'
    
    UUID    = Column(Unicode(36), nullable=False, primary_key=True)
    Type    = Column(Unicode(50), nullable=False)
    Version = Column(Integer(11), nullable=False)
    
    Link       = "versions"
    
    def __repr__(self):
        return u"<Version('%s - %i')>" % (self.Type, self.Version)

    def __init__(self, uuid, dtype, version):
        self.UUID = uuid
        self.Type = dtype
        self.Version = version
                   
class Year(Base, TableTop):
    """
    This class contains an auto-incrementing primary key, a number used for
    ordering the years, and a textual representation of the year
    """
    __tablename__ = 'year'
    
    YearIndex  = Column(Integer(11), nullable=False, primary_key=True)
    YearNumber = Column(Integer(11), nullable=False)
    Year       = Column(Unicode(50), nullable=False)
    
    Link       = "years"
    
    def __repr__(self):
        return u"<Year('%s')>" % (self.Year)

    def __init__(self, year_name, year_number):
        self.Year       = year_name
        self.YearNumber = year_number
        
class Department(Base, TableTop):
    """
    This class contains an auto-incrementing primary key and a text
    representation of the department
    """
    __tablename__ = 'department'
    
    DepartmentIndex = Column(Integer(11), nullable=False, primary_key=True)
    Department      = Column(Unicode(50), nullable=False)

    Link            = "departments"
    
    def __repr__(self):
        return u"<Department('%s')>" % (self.Department)

    def __init__(self, department_name):
        self.Department = department_name

class SubjectType(Base, TableTop):
    """
    This class contains an auto-incrementing primary key, the title of the
    subject type, and miscellaneous other information about the subject type
    """
    __tablename__ = 'subjecttype'
    
    SubjectTypeIndex = Column(Integer(11), nullable=False, primary_key=True)
    Title            = Column(Unicode(50), nullable=False)
    ShortTitle       = Column(Unicode(50))
    ID               = Column(Unicode(50))
    Description      = Column(UnicodeText())
    Weight           = Column(Integer(11))
    HighPriority     = Column(Integer(1), nullable=False, default=0)

    Link             = "SubjectTypes"
    
    def __repr__(self):
        return u"<SubjectType('%s')>" % (self.Title)

    def __init__(self, title, short_title=None, id_val=None, description=None, weight=None, high_priority=None):
        self.Title        = title
        self.ShortTitle   = short_title
        self.ID           = id_val
        self.Description  = description
        self.Weight       = weight
        self.HighPriority = high_priority
        
class Grade(Base, TableTop):
    """
    This class contains a unique ordered grade number, the department that
    the grade is in, and a text description of the grade
    """
    __tablename__ = 'grade'
    
    GradeIndex      = Column('Grade', Integer(11), nullable=False, autoincrement=False, primary_key=True) #Rename ASAP
    DepartmentIndex = Column(Integer(11), ForeignKey('department.DepartmentIndex'), nullable=False)
    Grade           = Column('GradeName', Unicode(50), nullable=False)
    
    Department      = relationship(Department, primaryjoin=DepartmentIndex==Department.DepartmentIndex, foreign_keys=[Department.DepartmentIndex], uselist=False)

    def __repr__(self):
        return u"<Grade('%s')>" % (self.Grade)

    def __init__(self, index, department, description):
        self.GradeIndex      = index
        self.DepartmentIndex = department.DepartmentIndex
        self.Grade           = description
     
class Term(Base, TableTop):
    """
    This class contains an auto-incrementing primary key, a number used for
    ordering the years, and a textual representation of the year
    """
    __tablename__ = 'term'
    
    TermIndex       = Column(Integer(11), nullable=False, primary_key=True)
    TermNumber      = Column(Integer(11), nullable=False)
    Term            = Column('TermName', Unicode(50), nullable=False) # Fix this in db ASAP
    DepartmentIndex = Column(Integer(11), ForeignKey('department.DepartmentIndex'), nullable=False)
    HasConduct      = Column(Integer(1), nullable=False, default=1)
    
    Department      = relationship(Department, primaryjoin=DepartmentIndex==Department.DepartmentIndex, foreign_keys=[Department.DepartmentIndex], uselist=False)
    
    def __repr__(self):
        return u"<Year('%s')>" % (self.Year)

    def __init__(self, term_name, term_number, department, has_conduct=True):
        self.Term = term_name
        self.TermNumber = term_number
        self.DepartmentIndex = department.DepartmentIndex
        if has_conduct:
            self.HasConduct = 1
        else:
            self.HasConduct = 0
            
class NonmarkType(Base, TableTop):
    """
    This class contains an auto-incrementing primary key, a mandatory
    description, and an optional applicable department
    """
    __tablename__ = 'nonmark_type'
    
    NonmarkTypeIndex = Column(Integer(11), nullable=False, primary_key=True)
    NonmarkType      = Column(Unicode(50), nullable=False)
    DepartmentIndex  = Column(Integer(11), ForeignKey('department.DepartmentIndex'))
    
    Department       = relationship(Department, primaryjoin=DepartmentIndex==Department.DepartmentIndex, foreign_keys=[Department.DepartmentIndex], uselist=False)

    Link             = 'nonmark_types'
    
    def __repr__(self):
        return u"<NonmarkType('%s')>" % (self.NonmarkType)
    
    def __init__(self, nonmark_type_description, department):
        self.NonmarkType = nonmark_type_description
        self.DepartmentIndex = department.DepartmentIndex

class NonmarkIndex(Base, TableTop):
    """
    This class contains an auto-incrementing primary key, a mandatory
    description, and an optional applicable department
    """
    __tablename__ = 'nonmark_index'
    
    NonmarkIndex     = Column(Integer(11), nullable=False, primary_key=True)
    NonmarkTypeIndex = Column(Integer(11), ForeignKey('nonmark_type.NonmarkTypeIndex'), nullable=False)
    Input            = Column(Unicode(8))
    Display          = Column(Unicode(8), nullable=False)
    MinScore         = Column(Float())
    Value            = Column(Float())
    
    NonmarkType      = relationship(NonmarkType, primaryjoin=NonmarkTypeIndex==NonmarkType.NonmarkTypeIndex, foreign_keys=[NonmarkType.NonmarkTypeIndex], backref=backref('NonmarkIndexes', uselist=True), uselist=False)

    Link             = 'nonmark_indexes'
    
    def __repr__(self):
        return u"<NonmarkIndex('%s: %s')>" % (self.NonmarkType.NonmarkType, self.Display)
    
    def __init__(self, nonmark_type, display, input_val=None, min_score=None, value=None):
        self.NonmarkTypeIndex = nonmark_type.NonmarkTypeIndex
        self.Display          = display
        self.Input            = input_val
        self.MinScore         = min_score
        self.Value            = value
    
class User(Base, TableTop):    
    """
    This class contains most user information.  The primary key is the
    username, and mandatory fields include FirstName and Surname
    """
    __tablename__ = 'user'
    
    Username        = Column(Unicode(50), nullable=False, primary_key=True)
    FirstName       = Column(Unicode(50), nullable=False)
    Surname         = Column(Unicode(50), nullable=False)
    Gender          = Column(Unicode(1))
    PhoneNumber     = Column(Unicode(20))
    CellNumber      = Column(Unicode(20))
    DOB             = Column(Date())
    Password        = Column(String(255))
    Password2       = Column(String(255))
    Permissions     = Column(Integer(11), default=0, nullable=False)
    Title           = Column(Unicode(10))
    House           = Column(Unicode(1))
    Email           = Column(Unicode(256))
    DateType        = Column(Integer(1))
    DateSeparator   = Column(Unicode(1))
    ActiveStudent   = Column(Integer(1), default=0, nullable=False)
    ActiveTeacher   = Column(Integer(1), default=0, nullable=False)
    SupportTeacher  = Column(Integer(1), default=0, nullable=False)
    DepartmentIndex = Column(Integer(11), ForeignKey('department.DepartmentIndex'))
    User1           = Column(Integer(1))
    User2           = Column(Integer(1))
    User3           = Column(Integer(1))
    User4           = Column(Integer(1))
    User5           = Column(Integer(1))

    Department      = relationship(Department, primaryjoin=DepartmentIndex==Department.DepartmentIndex, foreign_keys=[Department.DepartmentIndex], backref=backref('Users', uselist=True), uselist=False)
    
    Link            = "users"
    
    def __init__(self, username, firstname, surname):
        self.Username  = username
        self.FirstName = firstname
        self.Surname   = surname
        
    def __repr__(self):
        return u"<User('%s %s (%s)')>" % (self.FirstName, self.Surname, self.Username)

class Class(Base, TableTop):
    """
    This class contains information about each class.  The primary key is
    auto-incrementing, and mandatory fields include Class, YearIndex and
    DepartmentIndex
    """

    __tablename__ = 'class'
    
    ClassIndex           = Column(Integer(11), nullable=False, primary_key=True)
    GradeIndex           = Column('Grade', Integer(11), ForeignKey('grade.Grade'))
    Class                = Column('ClassName', Unicode(50), nullable=False) # Fix this in db ASAP
    YearIndex            = Column(Integer(11), ForeignKey('year.YearIndex'), nullable=False)
    ClassTeacherUsername = Column(Unicode(50), ForeignKey('user.Username'))
    DepartmentIndex      = Column(Integer(11), ForeignKey('department.DepartmentIndex'), nullable=False)
    HasConduct           = Column(Integer(1), nullable=False, default=1)

    Grade                = relationship(Grade, primaryjoin=GradeIndex==Grade.GradeIndex, foreign_keys=[Grade.GradeIndex], uselist=False)
    Department           = relationship(Department, primaryjoin=DepartmentIndex==Department.DepartmentIndex, foreign_keys=[Department.DepartmentIndex], uselist=False)
    Year                 = relationship(Year, primaryjoin=YearIndex==Year.YearIndex, foreign_keys=[Year.YearIndex], uselist=False)
    ClassTeacher         = relationship(User, primaryjoin=ClassTeacherUsername==User.Username, foreign_keys=[User.Username], uselist=False)
    
    Link                 = "classes"
    
    def __repr__(self):
        return u"<Class('%s - %s')>" % (self.Year.Year, self.Class)
    
    def __init__(self, class_name, year, department, grade=None, class_teacher=None, has_conduct=True):
        self.Class           = class_name
        self.YearIndex       = year.YearIndex
        self.DepartmentIndex = department.DepartmentIndex
        self.Grade           = grade
        if class_teacher != None:
            self.ClassTeacherUsername = class_teacher.Username
        if has_conduct:
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
    
    ClassTermIndex       = Column(Integer(11), nullable=False, primary_key=True)
    ClassIndex           = Column(Integer(11), ForeignKey('class.ClassIndex'), nullable=False)
    TermIndex            = Column(Integer(11), ForeignKey('term.TermIndex'), nullable=False)
    AbsenceType          = Column(Integer(11), nullable=False, default=0)
    AverageType          = Column(Integer(11), nullable=False, default=0)
    ConductType          = Column(Integer(11), nullable=False, default=0)
    EffortType           = Column(Integer(11), nullable=False, default=0)
    Average              = Column(Float())
    Effort               = Column(Float())
    Conduct              = Column(Float())
    AverageTypeIndex     = Column(Integer(11), ForeignKey('nonmark_type.NonmarkTypeIndex'))
    ConductTypeIndex     = Column(Integer(11), ForeignKey('nonmark_type.NonmarkTypeIndex'))
    EffortTypeIndex      = Column(Integer(11), ForeignKey('nonmark_type.NonmarkTypeIndex'))
    CTCommentType        = Column(Integer(11), nullable=False, default=0)
    HODCommentType       = Column(Integer(11), nullable=False, default=0)
    PrincipalCommentType = Column(Integer(11), nullable=False, default=0)
    CanDoReport          = Column(Integer(1), nullable=False, default=0)
    ReportTemplate       = Column(LargeBinary())
    ReportTemplateType   = Column(Unicode(300))

    Class                = relationship(Class, primaryjoin=ClassIndex==Class.ClassIndex, foreign_keys=[Class.ClassIndex], uselist=False)
    Term                 = relationship(Term, primaryjoin=TermIndex==Term.TermIndex, foreign_keys=[Term.TermIndex], uselist=False)
    AverageNM            = relationship(NonmarkType, primaryjoin=AverageTypeIndex==NonmarkType.NonmarkTypeIndex, foreign_keys=[NonmarkType.NonmarkTypeIndex], uselist=False)
    ConductNM            = relationship(NonmarkType, primaryjoin=AverageTypeIndex==NonmarkType.NonmarkTypeIndex, foreign_keys=[NonmarkType.NonmarkTypeIndex], uselist=False)
    EffortNM             = relationship(NonmarkType, primaryjoin=AverageTypeIndex==NonmarkType.NonmarkTypeIndex, foreign_keys=[NonmarkType.NonmarkTypeIndex], uselist=False)
    
    def __repr__(self):
        return u"<ClassTerm('%s - %s - %s')>" % (self.Term.Term, self.Class.Year.Year, self.Class.Class)

    def __init__(self, class_object, term, absence_type=0, average_type=0, conduct_type=0, effort_type=0,
                       class_teacher_comment_type=0, hod_comment_type=0, principal_comment_type=0,
                       average_nonmark_type=None, conduct_nonmark_type=None, effort_nonmark_type=None,
                       report_template=None, report_template_type=None):
        self.ClassIndex           = class_object.ClassIndex
        self.TermIndex            = term.TermIndex
        self.AbsenceType          = absence_type
        self.AverageType          = average_type
        self.ConductType          = conduct_type
        self.EffortType           = effort_type
        self.CTCommentType        = class_teacher_comment_type
        self.HODCommentType       = hod_comment_type
        self.PrincipalCommentType = principal_comment_type
        self.ReportTemplate       = report_template
        self.ReportTemplateType   = report_template_type
        if average_nonmark_type != None:
            self.AverageTypeIndex = average_nonmark_type.NonmarkTypeIndex
        if effort_nonmark_type != None:
            self.EffortTypeIndex = effort_nonmark_type.NonmarkTypeIndex
        if conduct_nonmark_type != None:
            self.ConductTypeIndex = conduct_nonmark_type.NonmarkTypeIndex
            
class ClassList(Base, TableTop):
    """
    This class contains information about each class.  The primary key is
    auto-incrementing, and mandatory fields include Class, YearIndex and
    DepartmentIndex
    """

    __tablename__ = 'classlist'
    
    ClassListIndex       = Column(Integer(11), nullable=False, primary_key=True)
    ClassTermIndex       = Column(Integer(11), ForeignKey('classterm.ClassTermIndex'), nullable=False)
    Username             = Column(Unicode(50), ForeignKey('user.Username'), nullable=False)
    Average              = Column(Float(), nullable=False, default=-1)
    Conduct              = Column(Float(), nullable=False, default=-1)
    Effort               = Column(Float(), nullable=False, default=-1)
    Rank                 = Column(Integer(11), nullable=False, default=-1)
    Absences             = Column(Integer(11), nullable=False, default=-1)
    CTComment            = Column(UnicodeText())
    CTCommentDone        = Column(Integer(1), nullable=False, default=0)
    HODComment           = Column(UnicodeText())
    HODCommentDone       = Column(Integer(1), nullable=False, default=0)
    HODUsername          = Column(Unicode(50), ForeignKey('user.Username'), nullable=False)
    PrincipalComment     = Column(UnicodeText())
    PrincipalCommentDone = Column(Integer(1), nullable=False, default=0)
    PrincipalUsername    = Column(Unicode(50), ForeignKey('user.Username'), nullable=False)
    ReportDone           = Column(Integer(1), nullable=False, default=0)
    ReportProofread      = Column(Integer(1), nullable=False, default=0)
    ReportProofDone      = Column(Integer(1), nullable=False, default=0)
    ReportPrinted        = Column(Integer(1), nullable=False, default=0)
    ClassOrder           = Column(Integer(11))

    HOD                  = relationship(User, primaryjoin=HODUsername==User.Username, foreign_keys=[User.Username], uselist=False)
    Principal            = relationship(User, primaryjoin=PrincipalUsername==User.Username, foreign_keys=[User.Username], uselist=False)
    User                 = relationship(User, primaryjoin=Username==User.Username, foreign_keys=[User.Username], uselist=False)
    ClassTerm            = relationship(ClassTerm, primaryjoin=ClassTermIndex==ClassTerm.ClassTermIndex, foreign_keys=[ClassTerm.ClassTermIndex], uselist=False)

    def __repr__(self):
        return u"<ClassList('%s: %s - %s - %s')>" % (self.User.Username, self.ClassTerm.Term.Term, self.ClassTerm.Class.Year.Year, self.ClassTerm.Class.Class)
    
    def __init__(self, class_term, user, order=None):
        self.ClassTermIndex  = class_term.ClassTermIndex
        self.Username        = user.Username
        self.ClassOrder      = order
            
class Casenote(Base, TableTop):
    """
    This class contains casenotes.  The primary key is auto-incrementing, and
    mandatory fields include WorkerUsername, StudentUsername, Date and Level
    """

    __tablename__ = 'casenote'
    
    CasenoteIndex   = Column('CaseNoteIndex', Integer(11), nullable=False, primary_key=True)
    CasenoteGroup   = Column('CaseNoteGroup', Integer(11))
    WorkerUsername  = Column(Unicode(50), ForeignKey('user.Username'), nullable=False)
    StudentUsername = Column(Unicode(50), ForeignKey('user.Username'), nullable=False)
    Note            = Column(UnicodeText())
    Date            = Column(DateTime(), nullable=False)
    Level           = Column(Integer(11), nullable=False, default=1)

    WorkerUser      = relationship(User, primaryjoin=WorkerUsername==User.Username, foreign_keys=[User.Username], uselist=False)
    StudentUser     = relationship(User, primaryjoin=StudentUsername==User.Username, foreign_keys=[User.Username], uselist=False)
    
    Link            = "casenotes"
    
    def __repr__(self):
        return u"<Casenote('%s -> %s (%s)')>" % (self.WorkerUsername, self.StudentUsername, self.Date)

    def __init__(self, worker, student, level, note, date=datetime.now()):
        self.WorkerUsername  = worker.Username
        self.StudentUsername = student.Username
        self.Level           = level
        self.Note            = note
        self.Date            = date
            
class Log(Base, TableTop):    
    __tablename__ = 'log'
    
    LogIndex      = Column(Integer(11), nullable=False, primary_key=True)
    Username      = Column(Unicode(50), nullable=False)
    Level         = Column(Integer(11), nullable=False)
    Time          = Column(DateTime(), nullable=False)
    Comment       = Column(UnicodeText())
    Page          = Column(UnicodeText(), nullable=False)
    RemoteHost    = Column(UnicodeText(), nullable=False)
    
    User          = relationship(User, primaryjoin=Username==User.Username, foreign_keys=[User.Username], backref=backref('Logs', uselist=True), uselist=False)

    Link          = "logs"
    
    def __repr__(self):
        return u"<Log('%i %s')>" % (self.Code, self.Username)
    
    def __init__(self, page, username, level, remote_host, comment=None):
        self.Username       = username
        self.Level          = level
        self.Page           = page
        self.RemoteHost     = remote_host
        self.Comment        = comment
        self.Time = datetime.now()
            
class LogIgnoreHost(Base, TableTop):
    __tablename__ = 'log_ignore_host'
    
    LogIgnoreHostIndex = Column(Integer(), nullable=False, primary_key=True)
    HostAddr           = Column(Unicode(32), nullable=False)
    
    Link               = "ignore_hosts"
    
    def __repr__(self):
        return u"<LogIgnoreHost('%s')>" % (self.HostAddr)

    def __init__(self, host_addr):
        if host_addr is None:
            raise ValueError("Host address must be set")
        self.HostAddr = host_addr