from typing import List, Optional
from pydantic import BaseModel


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


class NotFoundResponse(BaseModel):
    code: int = Field(-1, description="Status Code")
    message: str = Field(
        "Resource not found!", description="Exception Information"
    )
