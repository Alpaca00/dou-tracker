from dataclasses import dataclass
from enum import Enum


class Month(Enum):
    """Enumeration representing months of the year."""

    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12


MONTHS_MAPPING = {
    "січня": Month.JANUARY,
    "лютого": Month.FEBRUARY,
    "березня": Month.MARCH,
    "квітня": Month.APRIL,
    "травня": Month.MAY,
    "червня": Month.JUNE,
    "липня": Month.JULY,
    "серпня": Month.AUGUST,
    "вересня": Month.SEPTEMBER,
    "жовтня": Month.OCTOBER,
    "листопада": Month.NOVEMBER,
    "грудня": Month.DECEMBER,
}


@dataclass
class JobCategory:
    name: str
    value: str


class JobCategories(str, Enum):
    """Enumeration representing job categories."""
    DOT_NET = ".NET"
    ACCOUNT_MANAGER = "Account Manager"
    AI_ML = "AI/ML"
    ANALYST = "Analyst"
    ANDROID = "Android"
    ANIMATOR = "Animator"
    ARCHITECT = "Architect"
    ARTIST = "Artist"
    ASSISTANT = "Assistant"
    BIG_DATA = "Big Data"
    BLOCKCHAIN = "Blockchain"
    C_PLUS_PLUS = "C++"
    C_LEVEL = "C-level"
    COPYWRITER = "Copywriter"
    DATA_ENGINEER = "Data Engineer"
    DATA_SCIENCE = "Data Science"
    DBA = "DBA"
    DESIGN = "Design"
    DEVOPS = "DevOps"
    EMBEDDED = "Embedded"
    ENGINEERING_MANAGER = "Engineering Manager"
    ERLANG = "Erlang"
    ERP_CRM = "ERP/CRM"
    FINANCE = "Finance"
    FLUTTER = "Flutter"
    FRONT_END = "Front End"
    GOLANG = "Golang"
    HARDWARE = "Hardware"
    HR = "HR"
    IOS_MACOS = "iOS/macOS"
    JAVA = "Java"
    LEGAL = "Legal"
    MARKETING = "Marketing"
    NODE_JS = "Node.js"
    OFFICE_MANAGER = "Office Manager"
    OTHER = "Other"
    PHP = "PHP"
    PRODUCT_MANAGER = "Product Manager"
    PROJECT_MANAGER = "Project Manager"
    PYTHON = "Python"
    QA = "QA"
    REACT_NATIVE = "React Native"
    RUBY = "Ruby"
    RUST = "Rust"
    SALES = "Sales"
    SALESFORCE = "Salesforce"
    SAP = "SAP"
    SCALA = "Scala"
    SCRUM_MASTER = "Scrum Master"
    SECURITY = "Security"
    SEO = "SEO"
    SUPPORT = "Support"
    SYS_ADMIN = "SysAdmin"
    TECHNICAL_WRITER = "Technical Writer"
    UNITY = "Unity"
    UNREAL_ENGINE = "Unreal Engine"
    MILITARY = "Військова справа"

    @classmethod
    def get_all_categories(cls) -> list[JobCategory]:
        return [
            cls.DOT_NET,
            cls.ACCOUNT_MANAGER,
            cls.AI_ML,
            cls.ANALYST,
            cls.ANDROID,
            cls.ANIMATOR,
            cls.ARCHITECT,
            cls.ARTIST,
            cls.ASSISTANT,
            cls.BIG_DATA,
            cls.BLOCKCHAIN,
            cls.C_PLUS_PLUS,
            cls.C_LEVEL,
            cls.COPYWRITER,
            cls.DATA_ENGINEER,
            cls.DATA_SCIENCE,
            cls.DBA,
            cls.DESIGN,
            cls.DEVOPS,
            cls.EMBEDDED,
            cls.ENGINEERING_MANAGER,
            cls.ERLANG,
            cls.ERP_CRM,
            cls.FINANCE,
            cls.FLUTTER,
            cls.FRONT_END,
            cls.GOLANG,
            cls.HARDWARE,
            cls.HR,
            cls.IOS_MACOS,
            cls.JAVA,
            cls.LEGAL,
            cls.MARKETING,
            cls.NODE_JS,
            cls.OFFICE_MANAGER,
            cls.OTHER,
            cls.PHP,
            cls.PRODUCT_MANAGER,
            cls.PROJECT_MANAGER,
            cls.PYTHON,
            cls.QA,
            cls.REACT_NATIVE,
            cls.RUBY,
            cls.RUST,
            cls.SALES,
            cls.SALESFORCE,
            cls.SAP,
            cls.SCALA,
            cls.SCRUM_MASTER,
            cls.SECURITY,
            cls.SEO,
            cls.SUPPORT,
            cls.SYS_ADMIN,
            cls.TECHNICAL_WRITER,
            cls.UNITY,
            cls.UNREAL_ENGINE,
            cls.MILITARY,
        ]


class QuantityLines(str, Enum):
    """Enumeration representing quantity of days/pages."""
    ONE = 1
