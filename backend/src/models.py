from enum import Enum

from flask_login import UserMixin
from flask_openapi3 import FileStorage
from pydantic import BaseModel, ConfigDict, Field


class User(UserMixin):
    def __init__(self, id: int, email: str, profile_picture: str | None = None) -> None:
        self.id = id
        self.email = email
        self.profile_picture = profile_picture

    def get_id(self) -> str:
        return str(self.id)

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def to_dict(self) -> dict:
        return {"id": self.id, "email": self.email, "profile_picture": self.profile_picture}


###############
#  KPI QUERY  #
###############


class AnalystPriceTargets(BaseModel):
    current: float | None = None
    high: float | None = None
    low: float | None = None
    mean: float | None = None
    median: float | None = None


class CompanyOfficer(BaseModel):
    age: int | None = None
    exercisedValue: int
    fiscalYear: int | None = None
    maxAge: int
    name: str
    title: str
    totalPay: int | None = None
    unexercisedValue: int
    yearBorn: int | None = None


class Info(BaseModel):
    field_52WeekChange: float | None = Field(None, alias="52WeekChange")
    SandP52WeekChange: float | None = None
    address1: str | None = None
    ask: float | None = None
    askSize: int | None = None
    auditRisk: int | None = None
    averageAnalystRating: str | None = None
    averageDailyVolume10Day: int | None = None
    averageDailyVolume3Month: int | None = None
    averageVolume: int | None = None
    averageVolume10days: int | None = None
    beta: float | None = None
    bid: float | None = None
    bidSize: int | None = None
    boardRisk: int | None = None
    bookValue: float | None = None
    city: str | None = None
    companyOfficers: list[CompanyOfficer] | None = None
    compensationAsOfEpochDate: int | None = None
    compensationRisk: int | None = None
    corporateActions: list | None = None
    country: str | None = None
    cryptoTradeable: bool | None = None
    currency: str | None = None
    currentPrice: float | None = None
    currentRatio: float | None = None
    customPriceAlertConfidence: str | None = None
    dateShortInterest: int | None = None
    dayHigh: float | None = None
    dayLow: float | None = None
    debtToEquity: float | None = None
    displayName: str | None = None
    dividendDate: int | None = None
    dividendRate: float | None = None
    dividendYield: float | None = None
    earningsCallTimestampEnd: int | None = None
    earningsCallTimestampStart: int | None = None
    earningsGrowth: float | None = None
    earningsQuarterlyGrowth: float | None = None
    earningsTimestamp: int | None = None
    earningsTimestampEnd: int | None = None
    earningsTimestampStart: int | None = None
    ebitda: int | None = None
    ebitdaMargins: float | None = None
    enterpriseToEbitda: float | None = None
    enterpriseToRevenue: float | None = None
    enterpriseValue: int | None = None
    epsCurrentYear: float | None = None
    epsForward: float | None = None
    epsTrailingTwelveMonths: float | None = None
    esgPopulated: bool | None = None
    exDividendDate: int | None = None
    exchange: str | None = None
    exchangeDataDelayedBy: int | None = None
    exchangeTimezoneName: str | None = None
    exchangeTimezoneShortName: str | None = None
    executiveTeam: list | None = None
    fiftyDayAverage: float | None = None
    fiftyDayAverageChange: float | None = None
    fiftyDayAverageChangePercent: float | None = None
    fiftyTwoWeekChangePercent: float | None = None
    fiftyTwoWeekHigh: float | None = None
    fiftyTwoWeekHighChange: float | None = None
    fiftyTwoWeekHighChangePercent: float | None = None
    fiftyTwoWeekLow: float | None = None
    fiftyTwoWeekLowChange: float | None = None
    fiftyTwoWeekLowChangePercent: float | None = None
    fiftyTwoWeekRange: str | None = None
    financialCurrency: str | None = None
    firstTradeDateMilliseconds: int | None = None
    fiveYearAvgDividendYield: float | None = None
    floatShares: float | None = None
    forwardEps: float | None = None
    forwardPE: float | None = None
    freeCashflow: float | None = None
    fullExchangeName: str | None = None
    fullTimeEmployees: int | None = None
    gmtOffSetMilliseconds: int | None = None
    governanceEpochDate: int | None = None
    grossMargins: float | None = None
    grossProfits: float | None = None
    hasPrePostMarketData: bool | None = None
    heldPercentInsiders: float | None = None
    heldPercentInstitutions: float | None = None
    impliedSharesOutstanding: int | None = None
    industry: str | None = None
    industryDisp: str | None = None
    industryKey: str | None = None
    irWebsite: str | None = None
    isEarningsDateEstimate: bool | None = None
    language: str | None = None
    lastDividendDate: int | None = None
    lastDividendValue: float | None = None
    lastFiscalYearEnd: int | None = None
    lastSplitDate: int | None = None
    lastSplitFactor: str | None = None
    longBusinessSummary: str | None = None
    longName: str | None = None
    market: str | None = None
    marketCap: float | None = None
    marketState: str | None = None
    maxAge: int | None = None
    messageBoardId: str | None = None
    mostRecentQuarter: int | None = None
    netIncomeToCommon: int | None = None
    nextFiscalYearEnd: int | None = None
    numberOfAnalystOpinions: int | None = None
    open: float | None = None
    operatingCashflow: int | None = None
    operatingMargins: float | None = None
    overallRisk: int | None = None
    payoutRatio: float | None = None
    phone: str | None = None
    previousClose: float | None = None
    priceEpsCurrentYear: float | None = None
    priceHint: float | None = None
    priceToBook: float | None = None
    priceToSalesTrailing12Months: float | None = None
    profitMargins: float | None = None
    quickRatio: float | None = None
    quoteSourceName: str | None = None
    quoteType: str | None = None
    recommendationKey: str | None = None
    recommendationMean: float | None = None
    region: str | None = None
    regularMarketChange: float | None = None
    regularMarketChangePercent: float | None = None
    regularMarketDayHigh: float | None = None
    regularMarketDayLow: float | None = None
    regularMarketDayRange: str | None = None
    regularMarketOpen: float | None = None
    regularMarketPreviousClose: float | None = None
    regularMarketPrice: float | None = None
    regularMarketTime: int | None = None
    regularMarketVolume: int | None = None
    returnOnAssets: float | None = None
    returnOnEquity: float | None = None
    revenueGrowth: float | None = None
    revenuePerShare: float | None = None
    sector: str | None = None
    sectorDisp: str | None = None
    sectorKey: str | None = None
    shareHolderRightsRisk: int | None = None
    sharesOutstanding: int | None = None
    sharesPercentSharesOut: float | None = None
    sharesShort: int | None = None
    sharesShortPreviousMonthDate: int | None = None
    sharesShortPriorMonth: int | None = None
    shortName: str | None = None
    shortPercentOfFloat: float | None = None
    shortRatio: float | None = None
    sourceInterval: int | None = None
    state: str | None = None
    symbol: str | None = None
    targetHighPrice: float | None = None
    targetLowPrice: float | None = None
    targetMeanPrice: float | None = None
    targetMedianPrice: float | None = None
    totalCash: int | None = None
    totalCashPerShare: float | None = None
    totalDebt: int | None = None
    totalRevenue: int | None = None
    tradeable: bool | None = None
    trailingAnnualDividendRate: float | None = None
    trailingAnnualDividendYield: float | None = None
    trailingEps: float | None = None
    trailingPE: float | None = None
    trailingPegRatio: float | None = None
    triggerable: bool | None = None
    twoHundredDayAverage: float | None = None
    twoHundredDayAverageChange: float | None = None
    twoHundredDayAverageChangePercent: float | None = None
    typeDisp: str | None = None
    volume: int | None = None
    website: str | None = None
    zip: str | None = None
    fax: str | None = None
    underlyingSymbol: str | None = None


class KPIQuery(BaseModel):
    ticker_name: str


class MainKPIs(BaseModel):
    ratioPE: float | None = None
    freeCashflowYield: float | None = None


class KPIResponse(BaseModel):
    analyst_price_targets: AnalystPriceTargets | None = None
    info: Info
    query: KPIQuery
    main: MainKPIs | None = None


##################
#  SEARCH QUERY  #
##################
class SearchQuery(BaseModel):
    query: str


class Resolution(BaseModel):
    height: int
    tag: str
    url: str
    width: int


class Thumbnail(BaseModel):
    resolutions: list[Resolution]


class News(BaseModel):
    link: str
    providerPublishTime: int
    publisher: str
    thumbnail: Thumbnail | None = None
    title: str
    type: str
    uuid: str
    relatedTickers: list[str] | None = None


class RawQuote(BaseModel):
    dispSecIndFlag: bool | None = None
    exchDisp: str
    exchange: str
    index: str
    industry: str | None = None
    industryDisp: str | None = None
    isYahooFinance: bool
    longname: str | None = None
    quoteType: str
    score: int
    sector: str | None = None
    sectorDisp: str | None = None
    shortname: str | None = None
    symbol: str
    typeDisp: str


class Quote(BaseModel):
    symbol: str
    long_name: str
    icon_url: str | None = None
    # Change % for since open
    today_change: float | None = None


class SearchResponse(BaseModel):
    quotes: list[Quote]
    query: SearchQuery


##########################
#  COMPARE GROWTH QUERY  #
##########################


class CompareGrowthQuery(BaseModel):
    ticker_names: list[str]
    period: str = "ytd"


class CompareGrowthResponse(BaseModel):
    query: CompareGrowthQuery
    candles: dict[str, list[float]]
    dates: list[str]


##################
#  TICKER QUERY  #
##################
class TickerQuery(BaseModel):
    ticker_name: str
    # defaults to "auto"
    interval: str | None = None
    period: str = "ytd"  # FIXME: this is not specific enough


class TickerResponse(BaseModel):
    dates: list[str]
    candles: list[float]
    query: TickerQuery
    delta: float
    # Point size sma
    smas: dict[int, list[float]]


class NotFoundResponse(BaseModel):
    code: int = -1
    message: str = "Resource not found!"


class BadRequestResponse(BaseModel):
    code: int = -2
    message: str = "Bad request!"
    error: str


#########################
#  HISTORICALKPI QUERY  #
#########################
class HistoricalKPI(BaseModel):
    dates: list[str]
    values: list[float]


class HistoricalKPIs(BaseModel):
    kpis: dict[str, HistoricalKPI]


####################
#  ETORO ANALYSIS  #
####################
class PrecisionEnum(str, Enum):
    B = "B"  # business day frequency
    D = "D"  # calendar day frequency
    W = "W"  # weekly frequency
    M = "M"  # monthly frequency
    Q = "Q"  # quarterly frequency
    Y = "Y"  # yearly frequency
    h = "h"  # hourly frequency
    min = "min"  # minutely frequency
    s = "s"  # secondly frequency
    ms = "ms"  # milliseconds
    us = "us"  # microseconds
    ns = "ns"  # nanoseconds


class EtoroForm(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    precision: PrecisionEnum
    file: FileStorage


class EtoroAnalysisResponse(BaseModel):
    close_date: list[str]
    closed_trades: list[int]
    profit_usd: list[float]


class EtoroAnalysisByNameQuery(BaseModel):
    filename: str
    precision: PrecisionEnum


class EtoroReportsResponse(BaseModel):
    reports: list[str]


class EtoroEvolutionInner(BaseModel):
    parts: dict[str, list[float]]
    dates: list[str]


class EtoroEvolutionResponse(BaseModel):
    evolution: EtoroEvolutionInner


######################
#  PROGRESS MODELS   #
######################


class TaskProgressResponse(BaseModel):
    step_name: str
    step_number: int
    step_count: int


class TaskStatusResponse(BaseModel):
    status: str  # pending, running, completed, failed
    progress: TaskProgressResponse | None = None
    error: str | None = None


class TaskStartResponse(BaseModel):
    task_id: str


class TaskIdPath(BaseModel):
    task_id: str


#################
#  AUTH MODELS  #
#################


class LoginBody(BaseModel):
    email: str
    password: str


class RegisterForm(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    email: str
    password: str
    profile_picture: FileStorage | None = None


class RegisterResponse(BaseModel):
    id: int
    email: str
    profile_picture: str | None = None


####################
#  PROFILE PICTURE #
####################
class ProfilePictureForm(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    profile_picture: FileStorage


class ProfilePicturePath(BaseModel):
    filename: str


class ProfilePictureResponse(BaseModel):
    message: str
    profile_picture: str


class ProfilePicturePathParams(BaseModel):
    user_email: str
    filename: str


class UserResponse(BaseModel):
    email: str
    profile_picture: str | None = None


class TaskResultResponse(BaseModel):
    """Generic response for task results. Can contain various data types."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    result: dict | None = None
