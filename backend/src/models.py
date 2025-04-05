from typing import List, Optional
from pydantic import BaseModel, Field


###############
#  KPI QUERY  #
###############


class AnalystPriceTargets(BaseModel):
    current: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    mean: Optional[float] = None
    median: Optional[float] = None


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
    field_52WeekChange: Optional[float] = Field(None, alias="52WeekChange")
    SandP52WeekChange: Optional[float] = None
    address1: Optional[str] = None
    ask: Optional[float] = None
    askSize: Optional[int] = None
    auditRisk: Optional[int] = None
    averageAnalystRating: Optional[str] = None
    averageDailyVolume10Day: Optional[int] = None
    averageDailyVolume3Month: Optional[int] = None
    averageVolume: Optional[int] = None
    averageVolume10days: Optional[int] = None
    beta: Optional[float] = None
    bid: Optional[float] = None
    bidSize: Optional[int] = None
    boardRisk: Optional[int] = None
    bookValue: Optional[float] = None
    city: Optional[str] = None
    companyOfficers: Optional[List[CompanyOfficer]] = None
    compensationAsOfEpochDate: Optional[int] = None
    compensationRisk: Optional[int] = None
    corporateActions: Optional[List] = None
    country: Optional[str] = None
    cryptoTradeable: Optional[bool] = None
    currency: Optional[str] = None
    currentPrice: Optional[float] = None
    currentRatio: Optional[float] = None
    customPriceAlertConfidence: Optional[str] = None
    dateShortInterest: Optional[int] = None
    dayHigh: Optional[float] = None
    dayLow: Optional[float] = None
    debtToEquity: Optional[float] = None
    displayName: Optional[str] = None
    dividendDate: Optional[int] = None
    dividendRate: Optional[float] = None
    dividendYield: Optional[float] = None
    earningsCallTimestampEnd: Optional[int] = None
    earningsCallTimestampStart: Optional[int] = None
    earningsGrowth: Optional[float] = None
    earningsQuarterlyGrowth: Optional[float] = None
    earningsTimestamp: Optional[int] = None
    earningsTimestampEnd: Optional[int] = None
    earningsTimestampStart: Optional[int] = None
    ebitda: Optional[int] = None
    ebitdaMargins: Optional[float] = None
    enterpriseToEbitda: Optional[float] = None
    enterpriseToRevenue: Optional[float] = None
    enterpriseValue: Optional[int] = None
    epsCurrentYear: Optional[float] = None
    epsForward: Optional[float] = None
    epsTrailingTwelveMonths: Optional[float] = None
    esgPopulated: Optional[bool] = None
    exDividendDate: Optional[int] = None
    exchange: Optional[str] = None
    exchangeDataDelayedBy: Optional[int] = None
    exchangeTimezoneName: Optional[str] = None
    exchangeTimezoneShortName: Optional[str] = None
    executiveTeam: Optional[List] = None
    fiftyDayAverage: Optional[float] = None
    fiftyDayAverageChange: Optional[float] = None
    fiftyDayAverageChangePercent: Optional[float] = None
    fiftyTwoWeekChangePercent: Optional[float] = None
    fiftyTwoWeekHigh: Optional[float] = None
    fiftyTwoWeekHighChange: Optional[float] = None
    fiftyTwoWeekHighChangePercent: Optional[float] = None
    fiftyTwoWeekLow: Optional[float] = None
    fiftyTwoWeekLowChange: Optional[float] = None
    fiftyTwoWeekLowChangePercent: Optional[float] = None
    fiftyTwoWeekRange: Optional[str] = None
    financialCurrency: Optional[str] = None
    firstTradeDateMilliseconds: Optional[int] = None
    fiveYearAvgDividendYield: Optional[float] = None
    floatShares: Optional[float] = None
    forwardEps: Optional[float] = None
    forwardPE: Optional[float] = None
    freeCashflow: Optional[float] = None
    fullExchangeName: Optional[str] = None
    fullTimeEmployees: Optional[int] = None
    gmtOffSetMilliseconds: Optional[int] = None
    governanceEpochDate: Optional[int] = None
    grossMargins: Optional[float] = None
    grossProfits: Optional[float] = None
    hasPrePostMarketData: Optional[bool] = None
    heldPercentInsiders: Optional[float] = None
    heldPercentInstitutions: Optional[float] = None
    impliedSharesOutstanding: Optional[int] = None
    industry: Optional[str] = None
    industryDisp: Optional[str] = None
    industryKey: Optional[str] = None
    irWebsite: Optional[str] = None
    isEarningsDateEstimate: Optional[bool] = None
    language: Optional[str] = None
    lastDividendDate: Optional[int] = None
    lastDividendValue: Optional[float] = None
    lastFiscalYearEnd: Optional[int] = None
    lastSplitDate: Optional[int] = None
    lastSplitFactor: Optional[str] = None
    longBusinessSummary: Optional[str] = None
    longName: Optional[str] = None
    market: Optional[str] = None
    marketCap: Optional[float] = None
    marketState: Optional[str] = None
    maxAge: Optional[int] = None
    messageBoardId: Optional[str] = None
    mostRecentQuarter: Optional[int] = None
    netIncomeToCommon: Optional[int] = None
    nextFiscalYearEnd: Optional[int] = None
    numberOfAnalystOpinions: Optional[int] = None
    open: Optional[float] = None
    operatingCashflow: Optional[int] = None
    operatingMargins: Optional[float] = None
    overallRisk: Optional[int] = None
    payoutRatio: Optional[float] = None
    phone: Optional[str] = None
    previousClose: Optional[float] = None
    priceEpsCurrentYear: Optional[float] = None
    priceHint: Optional[float] = None
    priceToBook: Optional[float] = None
    priceToSalesTrailing12Months: Optional[float] = None
    profitMargins: Optional[float] = None
    quickRatio: Optional[float] = None
    quoteSourceName: Optional[str] = None
    quoteType: Optional[str] = None
    recommendationKey: Optional[str] = None
    recommendationMean: Optional[float] = None
    region: Optional[str] = None
    regularMarketChange: Optional[float] = None
    regularMarketChangePercent: Optional[float] = None
    regularMarketDayHigh: Optional[float] = None
    regularMarketDayLow: Optional[float] = None
    regularMarketDayRange: Optional[str] = None
    regularMarketOpen: Optional[float] = None
    regularMarketPreviousClose: Optional[float] = None
    regularMarketPrice: Optional[float] = None
    regularMarketTime: Optional[int] = None
    regularMarketVolume: Optional[int] = None
    returnOnAssets: Optional[float] = None
    returnOnEquity: Optional[float] = None
    revenueGrowth: Optional[float] = None
    revenuePerShare: Optional[float] = None
    sector: Optional[str] = None
    sectorDisp: Optional[str] = None
    sectorKey: Optional[str] = None
    shareHolderRightsRisk: Optional[int] = None
    sharesOutstanding: Optional[int] = None
    sharesPercentSharesOut: Optional[float] = None
    sharesShort: Optional[int] = None
    sharesShortPreviousMonthDate: Optional[int] = None
    sharesShortPriorMonth: Optional[int] = None
    shortName: Optional[str] = None
    shortPercentOfFloat: Optional[float] = None
    shortRatio: Optional[float] = None
    sourceInterval: Optional[int] = None
    state: Optional[str] = None
    symbol: Optional[str] = None
    targetHighPrice: Optional[float] = None
    targetLowPrice: Optional[float] = None
    targetMeanPrice: Optional[float] = None
    targetMedianPrice: Optional[float] = None
    totalCash: Optional[int] = None
    totalCashPerShare: Optional[float] = None
    totalDebt: Optional[int] = None
    totalRevenue: Optional[int] = None
    tradeable: Optional[bool] = None
    trailingAnnualDividendRate: Optional[float] = None
    trailingAnnualDividendYield: Optional[float] = None
    trailingEps: Optional[float] = None
    trailingPE: Optional[float] = None
    trailingPegRatio: Optional[float]
    triggerable: Optional[bool] = None
    twoHundredDayAverage: Optional[float] = None
    twoHundredDayAverageChange: Optional[float] = None
    twoHundredDayAverageChangePercent: Optional[float] = None
    typeDisp: Optional[str] = None
    volume: Optional[int] = None
    website: Optional[str] = None
    zip: Optional[str] = None
    fax: Optional[str] = None
    underlyingSymbol: Optional[str] = None


class KPIQuery(BaseModel):
    ticker_name: str


class MainKPIs(BaseModel):
    ratioPE: float
    freeCashflowYield: float


class KPIResponse(BaseModel):
    analyst_price_targets: Optional[AnalystPriceTargets] = None
    info: Info
    query: KPIQuery
    main: Optional[MainKPIs] = None


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


class RawQuote(BaseModel):
    dispSecIndFlag: Optional[bool] = None
    exchDisp: str
    exchange: str
    index: str
    industry: Optional[str] = None
    industryDisp: Optional[str] = None
    isYahooFinance: bool
    longname: Optional[str] = None
    quoteType: str
    score: int
    sector: Optional[str] = None
    sectorDisp: Optional[str] = None
    shortname: str
    symbol: str
    typeDisp: str


class Quote(BaseModel):
    raw: RawQuote
    info: Info
    icon_url: Optional[str] = None
    # Change % for since open
    today_change: Optional[float] = None


class SearchResponse(BaseModel):
    quotes: List[Quote]
    query: SearchQuery


##################
#  TICKER QUERY  #
##################
class TickerQuery(BaseModel):
    ticker_name: str
    period: str = "1mo"  # FIXME: this is not specific enough


class TickerCandle(BaseModel):
    Close: float
    Date: str
    Dividends: float
    High: float
    Low: float
    Open: float
    Stock_Splits: int = Field(..., alias="Stock Splits")
    Volume: int


class TickerResponse(BaseModel):
    candles: List[TickerCandle]
    query: TickerQuery
    delta: float


class NotFoundResponse(BaseModel):
    code: int = -1
    message: str = "Resource not found!"
