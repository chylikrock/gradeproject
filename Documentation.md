# Документация:
# Базовые функции для работы с графиком:
1. calculate_sma() - Простая Скользящая Средняя. 

Код:
def calculate_sma(prices: List[float], period: int) -> List[Optional[float]]:

Что делает: Создает сглаженную линию на графике

Математика: SMA = (цена1 + цена2 + ... + ценаN) / N

На графике: Синяя линия поверх свечей

Как помогает: Показывает общий тренд, фильтруя "шум"

Пример в коде:
#Берем 20 последних цен → получаем линию SMA(20)
sma_line = calculate_sma(closing_prices, period=20)
#На графике: если цена выше SMA — восходящий тренд

2. calculate_ema() - Экспоненциальная Скользящая Средняя.

Код:
def calculate_ema(prices: List[float], period: int = 13) -> List[Optional[float]]:

Что делает: Быстрая реагирующая линия (больше вес новым ценам)

Математика: EMA = цена * k + вчерашняя_EMA * (1-k) где k = 2/(период+1)

На графике: Красная линия, ближе к текущей цене

Как помогает: Ловит ранние развороты тренда

Пример как разница между SMA и EMA:
Цена:    100 102 101 105 103 108 107
SMA:   -   -  101 102 103 105 106  ← сглаженная
EMA:   -   -  101 103 103 106 107  ← быстрее реагирует

3. calculate_rsi() - Индекс Относительной Силы.

Код:
def calculate_rsi(close_prices: List[float], period: int = 14) -> List[Optional[float]]:

Что делает: Измеряет "перекупленность/перепроданность"

Математика: RSI = 100 - 100/(1 + средний_рост/среднее_падение)

На графике: Отдельный индикатор 0-100 с уровнями 30/70

Как помогает: Предупреждает о разворотах

Пример импульса на график:
RSI > 70 → Красная зона → Возможен спад
RSI < 30 → Зеленая зона → Возможен рост
Между 30 и 70 → Желтая зона → Нейтрально

4. calculate_macd() - Схождение/Расхождение Скользящих Средних.

Код:
def calculate_macd(close_prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9)

Что делает: Три линии на одном графике

Математика:
    • MACD линия = EMA(12) - EMA(26) ← разница быстрой и медленной
    • Signal линия = EMA(MACD, 9) ← сглаженный MACD
    • Гистограмма = MACD - Signal ← разница линий

Пример импульса на график:
MACD пересекает Signal снизу вверх → Синий столбец → ПОКУПКА
MACD пересекает Signal сверху вниз → Красный столбец → ПРОДАЖА

5. calculate_momentum() - Импульс

Код:
def calculate_momentum(prices: List[float], period: int = 10) -> List[Optional[float]]:

Что делает: Измеряет скорость изменения цены

Математика: Momentum = цена_сегодня - цена_N_дней_назад

На графике: Осциллятор вокруг нуля

Как помогает: Определяет силу тренда

Пример импульса за 10 дней:
День 1: Цена = 0.00001000
День 10: Цена = 0.00001200
Momentum = 0.00001200 - 0.00001000 = +0.00000200 ← сильный рост

6. calculate_bull_bear_power() - Сила Быков/Медведей

Код:
def calculate_bull_bear_power(high_prices, low_prices, close_prices, period=13)

Что делает: Два индикатора для измерения давления

Математика:
    • Bull Power = максимум_дня - EMA(цены_закрытия) ← сила покупателей
    • Bear Power = минимум_дня - EMA(цены_закрытия) ← сила продавцов

Пример импульсов на график:
      Bull > 0 и растет → Быки контролируют
      Bear < 0 и падает → Медведи контролируют
      Оба > 0 → Сильный бычий тренд
      Оба < 0 → Сильный медвежий тренд

# Практическое применение на графиках:
Комбинация индикаторов образует стратегию. Вот пример одной из базовых стратегий с объяснением в коде:

#1. Определяем тренд по SMA
sma_20 = calculate_sma(prices, 20)
тренд_вверх = prices[-1] > sma_20[-1]

#2. Проверяем момент входа по RSI
rsi = calculate_rsi(prices, 14)
перепроданность = rsi[-1] < 30 if rsi[-1] else False

#3. Подтверждаем сигнал MACD
macd_line, signal_line, _ = calculate_macd(prices)
macd_сигнал = macd_line[-1] > signal_line[-1] if macd_line[-1] else False

#Торговый сигнал
if тренд_вверх and перепроданность and macd_сигнал:
    print("Сигнал к покупке")
else:
    print("Сигнал к продаже")

# Также в стратегиях можно найти визуальные паттерны. Вот пример нескольких из них:

1. Дивергенция RSI (пример):

#Графически: цена делает новый максимум, а RSI — нет

цена_макс = max(prices[-10:])

rsi_макс = max(rsi_values[-10:]) if all(rsi_values[-10:]) else None

if цена_растет but rsi_падает:
    
    print("Медвежья дивергенция → возможен разворот вниз")

2. Пересечение скользящих средних (пример):

sma_50 = calculate_sma(prices, 50)

sma_200 = calculate_sma(prices, 200)

#"Золотой крест" на графике

if sma_50[-1] > sma_200[-1] and sma_50[-2] <= sma_200[-2]:
    print("Золотой крест → сильный бычий сигнал")


# Пример на графике (Пример: Pepe):

ЦЕНА PEPE/USDT:
    
    │                              ▒▒▒
   
    │                         ▒▒▒▒▒
    
    │                    ▒▒▒▒▒


0.000012 ┤             ▒▒▒                EMA(13) ────────
   
    │           ▒▒▒▒▒                   SMA(20) ─•─•─•─•─
    
    │      ▒▒▒▒▒
    
    │ ▒▒▒▒▒


0.000008┼────────────────────────────────────────
    

RSI (ниже графика цены):

 100 ┤          │
 
  70 ┤───────┼────── Перекупленность  ← Внимание!
  
  50 ┼───────────────
  30 ┤───────┼────── Перепроданность  ← Возможность!
   0 ┤          │

# Заключение:
Этот модуль — это переход от обычного обучения к пониманию технического анализа на трёх языках: математики (формул), программирования (алгоритмов) и графиков (визуализации). Это поможет перестать просто ставить индикаторы и начать понимать, что стоит за каждой линией и импульсом на графике с помощью простых примеров.
# Удачи в обучении!


# English version (also in releases):

# Documentation:
# Basic functions for working with the schedule:

1. calculate_sma() is A Simple Moving Average.

Code:
def calculate_sma(prices: List[float], period: int) -> List[Optional[float]]:

What does: Creates a smoothed line on the chart

Math: SMA = (price1 + price2 + ... + Price N) / N

On the chart: The blue line on top of the candles

How it helps: Shows the general trend by filtering out the "noise"

An example in the code:
#We take the last 20 prices → we get the SMA(20) line
sma_line = calculate_sma(closing_prices, period=20)
#On the chart: if the price is above the SMA, there is an uptrend

2. calculate_ema() is An Exponential Moving Average.

Code:
def calculate_ema(prices: List[float], period: int = 13) -> List[Optional[float]]:

What does: Fast reaction line (more weight for new prices)

Math: EMA = price * k + yesterday's system * (1-k) where k = 2/(period+1)

On the chart: The red line is closer to the current price

How it helps: Catches early trend reversals

Example of the difference between SMA and EMA:
Price: 100 102 101 105 103 108 107
SMA: - - 101 102 103 105 106 , smoothed
The EMA: - - 101 103 103 106 107 Reacts faster

3. calculate_rsi() is The Relative Strength Index.

Code:
def calculate_rsi(close_prices: List[float], period: int = 14) -> List[Optional[float]]:

What it does: Measures "overbought/oversold"

Math: RSI = 100 - 100/(1 + average rise/average fall)

On the chart: A separate 0-100 indicator with 30/70 levels

How it helps: Warns about U-turns

Example of an impulse on the chart:
RSI > 70 → Red zone → Possible recession
RSI < 30 → Green Zone → Growth is possible
Between 30 and 70 → Yellow zone → Neutral

4. calculate_macd() - Convergence/Divergence Of Moving Averages.

Code:
def calculate_macd(close_prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9)
What it does: Three lines on one chart

Mathematics:
• MACD line = EMA(12) - EMA(26) ← The difference between fast and slow
• Signal line = EMA(MACD, 9) ← smoothed MACD
• Histogram = MACD - Signal ← line difference

An example of an impulse on the chart:
The MACD crosses the Signal from bottom to top → Blue column → BUY
The MACD crosses the Signal from top to bottom → Red Column → SELL

5. calculate_momentum() - Momentum

Code:
def calculate_momentum(prices: List[float], period: int = 10) -> List[Optional[float]]:

What it does: Measures the rate of price change

Math: Momentum = price today - Price today

On the chart: An oscillator around zero

How it helps: Determines the strength of the trend

Example of a 10-day pulse:
Day 1: Price = 0.00001000
Day 10: Price = 0.00001200
Momentum = 0.00001200 - 0.00001000 = +0.00000200 ← strong growth

6. calculate_bull_bear_power() - Bull Power/Bears

Code:
def calculate_bull_bear_power(high_prices, low_prices, close_prices, period=13)

What it does: Two indicators for measuring pressure

Mathematics:
• Bull Power = max_day - EMA(closing price_) , the power of buyers
• Bear Power = minimum_day - EMA(closing price_) , the power of sellers

Example of impulses on the chart:
Bull > 0 and rising → Bulls in control
Bear < 0 and falls → Bears control
Both > 0 → Strong bullish trend
Both < 0 → Strong bearish trend


# Practical application on graphs:

# The combination of indicators forms a strategy. Here is an example of one of the basic strategies with an explanation in the code:

#1. We determine the trend by SMA
sma_20 = calculate_sma(prices, 20)
trend_up = prices[-1] > sma_20[-1]

#2. Check the moment of entry by RSI
rsi = calculate_rsi(prices, 14)
oversold = rsi[-1] < 30 if rsi[-1] else False

#3. Confirm
the MACD signal macd_line, signal_line, _ = calculate_macd(prices)
macd_signal = macd_line[-1] > signal_line[-1] if macd_line[-1] else False

#Trading signal
if trend_up and oversold and macd_sign:
print("Buy signal")
else:
print("Sell signal")

# You can also find visual patterns in strategies. Here is an example of a few of them:

1. RSI Divergence (example):
#Graphically: the price makes a new maximum, but the RSI does not
price_max = max(prices[-10:])
hsi_max = max(rsi_values[-10:]) if all(rsi_values[-10:]) else None

if the price goes up but the price goes down:
print("Bearish divergence → possible downward reversal")

2. Intersection of moving averages (example):
sma_50 = calculate_sma(prices, 50)
sma_200 = calculate_sma(prices, 200)

#"Golden cross" on the chart
if sma_50[-1] > sma_200[-1] and sma_50[-2] <= sma_200[-2]:
print("GOLDEN CROSS → strong bullish signal")

# Example on the chart (Example: Pepe):

PEPE/USDT PRICE:
│ ▒▒▒▒▒
│ ▒▒▒▒▒
0.000012 ┤ ▒▒▒ EMA(13) ────────
│ ▒▒▒▒▒ SMA(20) ─•─•─•─•─
│ ▒▒▒▒▒
│ ▒▒▒▒▒
0.000008┼────────────────────────────────────────

RSI (below the price chart):
100 ┤ │
70 ┤───────┼────── Overbought ← Attention!
50 ┼───────────────
30 ┤───────┼────── Oversold ← Opportunity!
0 ┤ │

# Conclusion:
This module is a transition from regular learning to understanding technical analysis in three languages: mathematics (formulas), programming (algorithms) and graphs (visualization). This will help you stop just setting indicators and start understanding what is behind each line and pulse on the chart using simple examples.
# Good luck learning!
