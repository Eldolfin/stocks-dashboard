from typing import List, Optional
from pydantic import BaseModel, Field


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
    resolutions: List[Resolution]


class News(BaseModel):
    link: str
    providerPublishTime: int
    publisher: str
    thumbnail: Optional[Thumbnail] = None
    title: str
    type: str
    uuid: str
    relatedTickers: Optional[List[str]] = None


class Quote(BaseModel):
    dispSecIndFlag: Optional[bool] = None
    exchDisp: str
    exchange: str
    index: str
    industry: Optional[str] = None
    industryDisp: Optional[str] = None
    isYahooFinance: bool
    longname: str
    quoteType: str
    score: int
    sector: Optional[str] = None
    sectorDisp: Optional[str] = None
    shortname: str
    symbol: str
    typeDisp: str


class SearchResponse(BaseModel):
    lists: List
    nav: List
    news: List[News]
    quotes: List[Quote]
    research: List


##################
#  TICKER QUERY  #
##################
class TickerQuery(BaseModel):
    ticker_name: str
    period: str = "1mo"  # FIXME: this is not specific enough


class TickerCandle(BaseModel):
    Close: float
    Date: str
    Dividends: int
    High: float
    Low: float
    Open: float
    Stock_Splits: int = Field(..., alias="Stock Splits")
    Volume: int


class TickerResponse(BaseModel):
    candles: List[TickerCandle]
    query: TickerQuery


###############
#  KPI QUERY  #
###############


class AnalystPriceTargets(BaseModel):
    current: float
    high: int
    low: int
    mean: float
    median: int


class CompanyOfficer(BaseModel):
    age: Optional[int] = None
    exercisedValue: int
    fiscalYear: int
    maxAge: int
    name: str
    title: str
    totalPay: Optional[int] = None
    unexercisedValue: int
    yearBorn: Optional[int] = None


class Info(BaseModel):
    field_52WeekChange: float = Field(..., alias="52WeekChange")
    SandP52WeekChange: float
    address1: str
    ask: int
    askSize: int
    auditRisk: int
    averageAnalystRating: str
    averageDailyVolume10Day: int
    averageDailyVolume3Month: int
    averageVolume: int
    averageVolume10days: int
    beta: float
    bid: float
    bidSize: int
    boardRisk: int
    bookValue: float
    city: str
    companyOfficers: List[CompanyOfficer]
    compensationAsOfEpochDate: int
    compensationRisk: int
    corporateActions: List
    country: str
    cryptoTradeable: bool
    currency: str
    currentPrice: float
    currentRatio: float
    customPriceAlertConfidence: str
    dateShortInterest: int
    dayHigh: float
    dayLow: float
    debtToEquity: int
    displayName: str
    dividendDate: int
    dividendRate: int
    dividendYield: float
    earningsCallTimestampEnd: int
    earningsCallTimestampStart: int
    earningsGrowth: float
    earningsQuarterlyGrowth: float
    earningsTimestamp: int
    earningsTimestampEnd: int
    earningsTimestampStart: int
    ebitda: int
    ebitdaMargins: float
    enterpriseToEbitda: float
    enterpriseToRevenue: float
    enterpriseValue: int
    epsCurrentYear: float
    epsForward: float
    epsTrailingTwelveMonths: float
    esgPopulated: bool
    exDividendDate: int
    exchange: str
    exchangeDataDelayedBy: int
    exchangeTimezoneName: str
    exchangeTimezoneShortName: str
    executiveTeam: List
    fiftyDayAverage: float
    fiftyDayAverageChange: float
    fiftyDayAverageChangePercent: float
    fiftyTwoWeekChangePercent: float
    fiftyTwoWeekHigh: float
    fiftyTwoWeekHighChange: float
    fiftyTwoWeekHighChangePercent: float
    fiftyTwoWeekLow: float
    fiftyTwoWeekLowChange: float
    fiftyTwoWeekLowChangePercent: float
    fiftyTwoWeekRange: str
    financialCurrency: str
    firstTradeDateMilliseconds: int
    fiveYearAvgDividendYield: float
    floatShares: int
    forwardEps: float
    forwardPE: float
    freeCashflow: int
    fullExchangeName: str
    fullTimeEmployees: int
    gmtOffSetMilliseconds: int
    governanceEpochDate: int
    grossMargins: float
    grossProfits: int
    hasPrePostMarketData: bool
    heldPercentInsiders: float
    heldPercentInstitutions: float
    impliedSharesOutstanding: int
    industry: str
    industryDisp: str
    industryKey: str
    irWebsite: str
    isEarningsDateEstimate: bool
    language: str
    lastDividendDate: int
    lastDividendValue: float
    lastFiscalYearEnd: int
    lastSplitDate: int
    lastSplitFactor: str
    longBusinessSummary: str
    longName: str
    market: str
    marketCap: int
    marketState: str
    maxAge: int
    messageBoardId: str
    mostRecentQuarter: int
    netIncomeToCommon: int
    nextFiscalYearEnd: int
    numberOfAnalystOpinions: int
    open: float
    operatingCashflow: int
    operatingMargins: float
    overallRisk: int
    payoutRatio: float
    phone: str
    preMarketChange: float
    preMarketChangePercent: float
    preMarketPrice: float
    preMarketTime: int
    previousClose: float
    priceEpsCurrentYear: float
    priceHint: int
    priceToBook: float
    priceToSalesTrailing12Months: float
    profitMargins: float
    quickRatio: float
    quoteSourceName: str
    quoteType: str
    recommendationKey: str
    recommendationMean: float
    region: str
    regularMarketChange: float
    regularMarketChangePercent: float
    regularMarketDayHigh: float
    regularMarketDayLow: float
    regularMarketDayRange: str
    regularMarketOpen: float
    regularMarketPreviousClose: float
    regularMarketPrice: float
    regularMarketTime: int
    regularMarketVolume: int
    returnOnAssets: float
    returnOnEquity: float
    revenueGrowth: float
    revenuePerShare: float
    sector: str
    sectorDisp: str
    sectorKey: str
    shareHolderRightsRisk: int
    sharesOutstanding: int
    sharesPercentSharesOut: float
    sharesShort: int
    sharesShortPreviousMonthDate: int
    sharesShortPriorMonth: int
    shortName: str
    shortPercentOfFloat: float
    shortRatio: float
    sourceInterval: int
    state: str
    symbol: str
    targetHighPrice: int
    targetLowPrice: int
    targetMeanPrice: float
    targetMedianPrice: int
    totalCash: int
    totalCashPerShare: float
    totalDebt: int
    totalRevenue: int
    tradeable: bool
    trailingAnnualDividendRate: float
    trailingAnnualDividendYield: float
    trailingEps: float
    trailingPE: float
    trailingPegRatio: float
    triggerable: bool
    twoHundredDayAverage: float
    twoHundredDayAverageChange: float
    twoHundredDayAverageChangePercent: float
    typeDisp: str
    volume: int
    website: str
    zip: str


class KPIQuery(BaseModel):
    ticker_name: str


class KPIResponse(BaseModel):
    analyst_price_targets: AnalystPriceTargets
    info: Info
    query: KPIQuery


class NotFoundResponse(BaseModel):
    code: int = Field(-1, description="Status Code")
    message: str = Field(
        "Resource not found!", description="Exception Information"
    )
