# Finance dashboard

using flask for the backend and svelte for the frontend.

## Getting started

### Live version

available at [wsb.eldolfin.top](https://wsb.eldolfin.top/)

### Development

dependencies: just, docker, docker-compose, npm

### Backend

```sh
just dev-docker
```

full deployment with reverse proxy at http://localhost:8085/

- backend hot reloads
- frontend does not

api doc at http://localhost:5000/openapi/

### Frontend

- start the backend with the command above

```sh
just dev-front
```

launches the front in dev-mode

- both backend and frontend hot reload now

front available at http://localhost:5173/

## TODO

- [ ] compare growth graph
- [ ] KPIs
  - [x] PER/DCF/Estimated Next Year PE
  - [ ] fix PE and dividend Yield
  - [ ] fix buttons and URL reload
  - [ ] format numbers in Millions, Billions and $ / %
  - [x] add %PNL over period
  - [ ] add LIVE price (red:green) next to FULL NAME
  - [ ] graphs earning growth
  - [ ] outstanding shares
  - [ ] Market sentiment (reddit & Insider buy/Sell)
  - [ ] add average 2y return

- [x] Live search engine
  - [~] Quick view : Price and today's PNL
- [x]: display price overtime
  - [ ]: variable candle size
  - [x]: variable time frame (zoom)
- [ ]: calendar
- [ ]:
  [news](https://yfinance-python.org/reference/api/yfinance.Ticker.news.html)
- [ ]:
  [advanced search](https://yfinance-python.org/reference/yfinance.screener.html)

- [ ] portfolio
  - [ ] import data from etoro csv
  - [ ] store persistant in db
  - [ ] user account with separate data
  - [ ] net invested
  - [ ] compare portfolio to tickers
  - [ ] show fees
  - [ ] compute sharpe ratio
  - [ ] trade history for data analysis
- [ ]: gamification
  - [ ]: fireworks when ATH/daily PNL > 5%

- [x]: deploy with domain name
