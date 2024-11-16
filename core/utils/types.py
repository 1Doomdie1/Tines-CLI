from enum import StrEnum, IntEnum

class keep_events_for_type(StrEnum):
    _1h   = "1h"
    _6h   = "6h"
    _1d   = "1d"
    _3d   = "3d"
    _7d   = "7d"
    _14d  = "15d"
    _30d  = "30d"
    _60d  = "60d"
    _90d  = "90d"
    _180d = "180d"
    _365d = "365d"

class List_Workflows_Filter_Types(StrEnum):
    LOCKED                 = "LOCKED"
    FAVORITE               = "FAVORITE"
    DISABLED               = "DISABLED"
    PUBLISHED              = "PUBLISHED"
    API_ENABLED            = "API_ENABLED"
    HIGH_PRIORITY          = "HIGH_PRIORITY"
    SEND_TO_STORY_ENABLED  = "SEND_TO_STORY_ENABLED"
    CHANGE_CONTROL_ENABLED = "CHANGE_CONTROL_ENABLED"

class List_Workflows_Order_Types(StrEnum):
    NAME                  = "NAME"
    NAME_DESC             = "NAME_DESC"
    RECENTLY_EDITED       = "RECENTLY_EDITED"
    ACTION_COUNT_ASC      = "ACTION_COUNT_ASC"
    ACTION_COUNT_DESC     = "ACTION_COUNT_DESC"
    LEAST_RECENTLY_EDITED = "LEAST_RECENTLY_EDITED"

class Output_Format_Types(StrEnum):
    JSON  = "json"
    TABLE = "table"

class STS_Access_Source_Types(StrEnum):
    STS               = "STS"
    OFF               = "OFF"
    WORKBENCH         = "WORKBENCH"
    STS_AND_WORKBENCH = "STS_AND_WORKBENCH"

class STS_Access_Types(StrEnum):
    TEAM           = "TEAM"
    GLOBAL         = "GLOBAL"
    SPECIFIC_TEAMS = "SPECIFIC_TEAMS"

class Workflow_Modes_Types(StrEnum):
    LIVE = "LIVE"
    TEST = "TEST"
    ALL  = "*"

class Workflow_Import_Types(StrEnum):
    NEW             = "new"
    VERSION_REPLACE = "versionReplace"

class Team_Member_Types(StrEnum):
    VIEWER     = "VIEWER"
    EDITOR     = "EDITOR"
    TEAM_ADMIN = "TEAM_ADMIN"
