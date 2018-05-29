from enum import Enum


class FieldsTypes(Enum):
    NominalData = 0
    OrdinalData = 1
    IntervalData = 2
    RatioData = 3


class FieldRolls(Enum):
    Parameter = 0
    ParameterReduction = 1
    Result = 2
    ResultEncoding = 3
    ExpectedResultReduction = 4
    StepResult = 5
    ResultPresentation = 6
    Other = 7


class DialogResults(Enum):
    Cancel = 0
    OK = 1


class Icons(Enum):
    Success = 0
    Error = 1
    Question = 2
    Warning = 3
    Info = 4


class NormalizeMethod(Enum):
    OneOfN = 0
    QualitativeToRange = 1
    EquilateralEncoding = 2
    NormalizeToRange = 3
    ReciprocalNormalization = 4


class NormalizeRange(Enum):
    ZeroToOne = 0
    MinusOneToOne = 1
