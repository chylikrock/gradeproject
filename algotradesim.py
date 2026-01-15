import random
from typing import List, Optional, Tuple


def calculate_sma(prices: List[float], period: int) -> List[Optional[float]]:
    """
    Вычисление простой скользящей средней (SMA)

    Args:
        prices: список цен
        period: период SMA

    Returns:
        Список значений SMA
    """
    if len(prices) < period:
        return [None] * len(prices)

    sma_values = []
    for i in range(len(prices)):
        if i < period - 1:
            sma_values.append(None)
        else:
            window = prices[i - period + 1: i + 1]
            sma = sum(window) / period
            sma_values.append(sma)

    return sma_values


def calculate_ema(prices: List[float], period: int = 13) -> List[Optional[float]]:
    """
    Вычисление экспоненциальной скользящей средней (EMA)
    """
    if len(prices) < period:
        return [None] * len(prices)

    ema_values = [None] * (period - 1)

    sma = sum(prices[:period]) / period
    ema_values.append(sma)

    multiplier = 2 / (period + 1)

    for i in range(period, len(prices)):
        ema = (prices[i] - ema_values[i - 1]) * multiplier + ema_values[i - 1]
        ema_values.append(ema)

    return ema_values


def calculate_ema_with_none(prices: List[Optional[float]], period: int = 13) -> List[Optional[float]]:
    """
    Вычисление EMA для списка, который может содержать None значения
    """
    if len(prices) < period:
        return [None] * len(prices)

    start_idx = 0
    for i in range(len(prices)):
        if prices[i] is not None:
            start_idx = i
            break

    if len(prices) - start_idx < period:
        return [None] * len(prices)

    valid_prices = [p for p in prices if p is not None]

    if len(valid_prices) < period:
        return [None] * len(prices)

    ema_result = calculate_ema(valid_prices, period)

    result = [None] * start_idx
    result.extend(ema_result)

    while len(result) < len(prices):
        result.append(None)

    return result[:len(prices)]


def calculate_momentum(prices: List[float], period: int = 10) -> List[Optional[float]]:
    """
    Вычисление индикатора Momentum
    """
    momentum_values = []

    for i in range(len(prices)):
        if i < period:
            momentum_values.append(None)
        else:
            momentum = prices[i] - prices[i - period]
            momentum_values.append(momentum)

    return momentum_values


def calculate_rsi(close_prices: List[float], period: int = 14) -> List[Optional[float]]:
    """
    Вычисление индикатора RSI (Relative Strength Index)

    Args:
        close_prices: список цен закрытия
        period: период RSI (обычно 14)

    Returns:
        Список значений RSI
    """
    if len(close_prices) < period + 1:
        return [None] * len(close_prices)

    changes = [close_prices[i] - close_prices[i - 1]
               for i in range(1, len(close_prices))]

    gains = [max(change, 0) for change in changes]
    losses = [abs(min(change, 0)) for change in changes]

    rsi_values = [None] * period

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    if avg_loss == 0:
        first_rsi = 100
    else:
        rs = avg_gain / avg_loss
        first_rsi = 100 - (100 / (1 + rs))

    rsi_values.append(first_rsi)

    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

        rsi_values.append(rsi)

    return rsi_values


def calculate_macd(close_prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[
    List[Optional[float]], List[Optional[float]], List[Optional[float]]]:
    """
    Вычисление индикатора MACD

    Args:
        close_prices: список цен закрытия
        fast: период быстрой EMA
        slow: период медленной EMA
        signal: период сигнальной линии

    Returns:
        Кортеж: (macd_line, signal_line, histogram)
    """
    ema_fast = calculate_ema(close_prices, fast)
    ema_slow = calculate_ema(close_prices, slow)

    macd_line = []
    for i in range(len(close_prices)):
        if ema_fast[i] is None or ema_slow[i] is None:
            macd_line.append(None)
        else:
            macd_line.append(ema_fast[i] - ema_slow[i])

    signal_line = calculate_ema_with_none(macd_line, signal)

    histogram = []
    for i in range(len(macd_line)):
        if macd_line[i] is None or signal_line[i] is None:
            histogram.append(None)
        else:
            histogram.append(macd_line[i] - signal_line[i])

    return macd_line, signal_line, histogram


def calculate_bull_bear_power(
        high_prices: List[float],
        low_prices: List[float],
        close_prices: List[float],
        period: int = 13
) -> tuple:
    """
    Вычисление индикатора Bull Bear Power
    """
    ema_close = calculate_ema(close_prices, period)

    bull_power = []
    bear_power = []

    for i in range(len(close_prices)):
        if ema_close[i] is None:
            bull_power.append(None)
            bear_power.append(None)
        else:
            bull_power.append(high_prices[i] - ema_close[i])
            bear_power.append(low_prices[i] - ema_close[i])

    return bull_power, bear_power


def generate_btc_price_data(days: int = 100) -> tuple:
    """
    Генерация тестовых данных цен для BTC
    """
    start_price = 50000.0

    close_prices = [start_price]
    high_prices = [start_price * 1.02]
    low_prices = [start_price * 0.98]

    for i in range(1, days):
        volatility = random.uniform(0.01, 0.05) if i < 30 else random.uniform(0.02, 0.08)

        if i < 40:
            trend = random.uniform(0.98, 1.04)
        elif i < 70:
            trend = random.uniform(0.96, 1.03)
        else:
            trend = random.uniform(0.94, 1.02)

        new_close = close_prices[-1] * trend

        new_high = new_close * (1 + random.uniform(0.005, volatility))
        new_low = new_close * (1 - random.uniform(0.005, volatility))

        if new_high <= new_low:
            new_high = new_low * 1.01

        new_close = max(new_low, min(new_high, new_close))

        close_prices.append(new_close)
        high_prices.append(new_high)
        low_prices.append(new_low)

    return close_prices, high_prices, low_prices


def plot_results(
        close_prices: List[float],
        momentum_values: List[Optional[float]],
        bull_power: List[Optional[float]],
        bear_power: List[Optional[float]],
        rsi_values: Optional[List[Optional[float]]] = None,
        macd_line: Optional[List[Optional[float]]] = None,
        signal_line: Optional[List[Optional[float]]] = None,
        histogram: Optional[List[Optional[float]]] = None
):
    """
    Простая текстовая визуализация результатов (без графиков)
    """
    print("\n" + "=" * 70)
    print("ТЕКСТОВАЯ ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТОВ")
    print("=" * 70)

    days_to_show = 30
    start_idx = max(0, len(close_prices) - days_to_show)

    print("\nСимвольный график цены (последние 30 дней):")
    print("-" * 70)

    display_prices = close_prices[start_idx:]
    min_price = min(display_prices)
    max_price = max(display_prices)

    for i, price in enumerate(display_prices):
        normalized = int(((price - min_price) / (max_price - min_price)) * 50) if max_price > min_price else 25
        day_num = start_idx + i + 1
        price_str = f"{price:.2f}"
        graph_bar = "█" * (normalized + 1)

        trend_marker = ""
        if i > 0:
            if price > display_prices[i - 1]:
                trend_marker = "↗"
            elif price < display_prices[i - 1]:
                trend_marker = "↘"
            else:
                trend_marker = "→"

        print(f"День {day_num:3d}: {trend_marker} {price_str} {graph_bar}")

    if rsi_values:
        print("\n" + "=" * 70)
        print("Индикатор RSI (последние 30 дней):")
        print("=" * 70)

        rsi_display = rsi_values[start_idx:]
        for i, rsi in enumerate(rsi_display):
            day_num = start_idx + i + 1
            if rsi is None:
                rsi_str = "N/A"
                bar = ""
            else:
                rsi_str = f"{rsi:.2f}"

                if rsi > 70:
                    level = "Перекупленность"
                elif rsi < 30:
                    level = "Перепроданность"
                else:
                    level = "Нейтрально"

                bar_length = min(20, int(abs(rsi - 50) / 2.5))
                if rsi > 50:
                    bar = "█" * bar_length + f" ↑ {level}"
                else:
                    bar = " " * (20 - bar_length) + "█" * bar_length + f" ↓ {level}"

            print(f"День {day_num:3d}: RSI: {rsi_str:6s} {bar}")

    if macd_line and signal_line and histogram:
        print("\n" + "=" * 70)
        print("Индикатор MACD (последние 30 дней):")
        print("=" * 70)

        macd_display = macd_line[start_idx:]
        signal_display = signal_line[start_idx:]
        hist_display = histogram[start_idx:]

        for i in range(len(macd_display)):
            day_num = start_idx + i + 1
            macd_val = macd_display[i]
            signal_val = signal_display[i]
            hist_val = hist_display[i]

            if macd_val is None or signal_val is None or hist_val is None:
                print(f"День {day_num:3d}: MACD: N/A | Signal: N/A | Hist: N/A")
            else:
                macd_str = f"{macd_val:+.2f}"
                signal_str = f"{signal_val:+.2f}"
                hist_str = f"{hist_val:+.2f}"

                if hist_val > 0:
                    signal = "Бычий"
                else:
                    signal = "Медвежий"

                if i > 0 and macd_display[i - 1] is not None and signal_display[i - 1] is not None:
                    if macd_val > signal_val and macd_display[i - 1] <= signal_display[i - 1]:
                        cross = "↑ Пересечение вверх"
                    elif macd_val < signal_val and macd_display[i - 1] >= signal_display[i - 1]:
                        cross = "↓ Пересечение вниз"
                    else:
                        cross = ""
                else:
                    cross = ""

                print(
                    f"День {day_num:3d}: MACD: {macd_str} | Signal: {signal_str} | Hist: {hist_str} [{signal}] {cross}")

    print("\n" + "=" * 70)
    print("Символьные графии индикаторов (последние 30 дней):")
    print("=" * 70)

    print("\nMomentum:")
    momentum_display = momentum_values[start_idx:]
    momentum_clean = [0 if v is None else v for v in momentum_display]
    mom_min = min(momentum_clean)
    mom_max = max(momentum_clean)

    for i, mom in enumerate(momentum_display):
        if mom is None:
            bar = " " * 25 + "N/A"
        else:
            normalized = int(((mom - mom_min) / (mom_max - mom_min)) * 25) if mom_max > mom_min else 12
            bar = (" " * (12 - normalized // 2)) + "█" * normalized
            if mom > 0:
                bar += " [+]"
            else:
                bar += " [-]"

        day_num = start_idx + i + 1
        mom_str = f"{mom:.2f}" if mom is not None else "      N/A     "
        print(f"День {day_num:3d}: {mom_str} {bar}")

    print("\nBull/Bear Power:")
    bull_display = bull_power[start_idx:]
    bear_display = bear_power[start_idx:]

    for i in range(len(bull_display)):
        bull = bull_display[i]
        bear = bear_display[i]
        day_num = start_idx + i + 1

        if bull is None or bear is None:
            print(f"День {day_num:3d}: Bull: N/A | Bear: N/A")
        else:
            bull_str = f"{bull:+.2f}"
            bear_str = f"{bear:+.2f}"

            bull_strength = ""
            bear_strength = ""


            if bull > 0:
                bull_strength = "█" * min(10, int(abs(bull) / 100))
            if bear < 0:
                bear_strength = "█" * min(10, int(abs(bear) / 100))

            print(f"День {day_num:3d}: Bull: {bull_str} {bull_strength:10s} | Bear: {bear_str} {bear_strength:10s}")


def main():
    """Основная функция для тестирования"""
    print("=" * 60)
    print("Тестирование индикаторов для BTC (с RSI и MACD)")
    print("=" * 60)

    # Генерация тестовых данных
    days = 100
    close_prices, high_prices, low_prices = generate_btc_price_data(days)

    print(f"\nСгенерировано {days} дней данных для BTC")
    print(f"Первые 5 значений закрытия: {[f'{p:.2f}' for p in close_prices[:5]]}")
    print(f"Последние 5 значений закрытия: {[f'{p:.2f}' for p in close_prices[-5:]]}")
    print(f"Минимальная цена: {min(close_prices):.2f}")
    print(f"Максимальная цена: {max(close_prices):.2f}")

    momentum_period = 10
    bbp_period = 13
    rsi_period = 14
    macd_fast = 12
    macd_slow = 26
    macd_signal = 9

    momentum_values = calculate_momentum(close_prices, momentum_period)
    bull_power, bear_power = calculate_bull_bear_power(
        high_prices, low_prices, close_prices, bbp_period
    )
    rsi_values = calculate_rsi(close_prices, rsi_period)
    macd_line, signal_line, histogram = calculate_macd(
        close_prices, macd_fast, macd_slow, macd_signal
    )

    print(f"\n{'=' * 60}")
    print(f"Результаты расчёта (последние 10 периодов):")
    print(f"{'=' * 60}")
    print(f"{'День':<6} {'Цена':<12} {'Momentum':<12} {'RSI':<8} {'MACD':<12} {'Hist':<12}")
    print(f"{'-' * 60}")

    start_idx = max(0, days - 10)
    for i in range(start_idx, days):
        price_str = f"{close_prices[i]:.2f}"
        mom_str = f"{momentum_values[i]:.2f}" if momentum_values[i] is not None else "None"
        rsi_str = f"{rsi_values[i]:.2f}" if rsi_values[i] is not None else "None"
        macd_str = f"{macd_line[i]:.2f}" if macd_line[i] is not None else "None"
        hist_str = f"{histogram[i]:.2f}" if histogram[i] is not None else "None"

        print(f"{i + 1:<6} {price_str:<12} {mom_str:<12} {rsi_str:<8} {macd_str:<12} {hist_str:<12}")

    print(f"\n{'=' * 60}")
    print("Анализ сигналов:")
    print(f"{'=' * 60}")

    mom_signals = []
    for i in range(momentum_period + 1, days - 1):
        if momentum_values[i] is not None and momentum_values[i - 1] is not None:
            if momentum_values[i] > 0 and momentum_values[i - 1] <= 0:
                mom_signals.append((i, "BUY", momentum_values[i]))
            elif momentum_values[i] < 0 and momentum_values[i - 1] >= 0:
                mom_signals.append((i, "SELL", momentum_values[i]))

    rsi_signals = []
    for i in range(rsi_period + 1, days - 1):
        if rsi_values[i] is not None and rsi_values[i - 1] is not None:
            if rsi_values[i] < 30 and rsi_values[i - 1] >= 30:
                rsi_signals.append((i, "Перепродано (BUY)", rsi_values[i]))
            elif rsi_values[i] > 70 and rsi_values[i - 1] <= 70:
                rsi_signals.append((i, "Перекуплено (SELL)", rsi_values[i]))

    macd_signals = []
    for i in range(max(macd_slow, macd_signal) + 1, days - 1):
        if macd_line[i] is not None and signal_line[i] is not None:

            if histogram[i] is not None and histogram[i - 1] is not None:
                if histogram[i] > 0 and histogram[i - 1] <= 0:
                    macd_signals.append((i, "Histogram ↑ (BUY)", macd_line[i], histogram[i]))
                elif histogram[i] < 0 and histogram[i - 1] >= 0:
                    macd_signals.append((i, "Histogram ↓ (SELL)", macd_line[i], histogram[i]))


    bbp_signals = []
    for i in range(bbp_period + 1, days - 1):
        if bull_power[i] is not None and bear_power[i] is not None:
            if bull_power[i] > 0 and bear_power[i] > 0:
                bbp_signals.append((i, "Сильный бычий", bull_power[i], bear_power[i]))
            elif bull_power[i] < 0 and bear_power[i] < 0:
                bbp_signals.append((i, "Сильный медвежий", bull_power[i], bear_power[i]))
            elif bull_power[i] > 0 > bear_power[i]:
                bbp_signals.append((i, "Борьба", bull_power[i], bear_power[i]))

    print(f"\nСигналы Momentum (пересечение нуля):")
    for signal in mom_signals[-10:]:
        print(f"  День {signal[0] + 1}: {signal[1]} (значение: {signal[2]:.2f})")

    print(f"\nСигналы RSI:")
    for signal in rsi_signals[-10:]:
        print(f"  День {signal[0] + 1}: {signal[1]} (значение: {signal[2]:.2f})")

    print(f"\nСигналы MACD:")
    for signal in macd_signals[-10:]:
        print(f"  День {signal[0] + 1}: {signal[1]} (MACD: {signal[2]:.2f})")

    print(f"\nСигналы Bull Bear Power:")
    for signal in bbp_signals[-10:]:
        print(f"  День {signal[0] + 1}: {signal[1]} (быки: {signal[2]:.2f}, медведи: {signal[3]:.2f})")


    print(f"\nСоздаем текстовую визуализацию...")
    plot_results(
        close_prices,
        momentum_values,
        bull_power,
        bear_power,
        rsi_values,
        macd_line,
        signal_line,
        histogram
    )


    print(f"\n{'=' * 60}")
    print("Статистика:")
    print(f"{'=' * 60}")

    valid_momentum = [m for m in momentum_values if m is not None]
    valid_bull = [b for b in bull_power if b is not None]
    valid_bear = [b for b in bear_power if b is not None]
    valid_rsi = [r for r in rsi_values if r is not None]
    valid_macd = [m for m in macd_line if m is not None]
    valid_hist = [h for h in histogram if h is not None]

    if valid_momentum:
        print(f"Momentum:")
        print(f"  Среднее: {sum(valid_momentum) / len(valid_momentum):.2f}")
        print(f"  Максимум: {max(valid_momentum):.2f}")
        print(f"  Минимум: {min(valid_momentum):.2f}")

    if valid_rsi:
        print(f"\nRSI:")
        print(f"  Среднее: {sum(valid_rsi) / len(valid_rsi):.2f}")
        print(f"  Максимум: {max(valid_rsi):.2f}")
        print(f"  Минимум: {min(valid_rsi):.2f}")
        print(f"  Дней в перекупленности (>70): {sum(1 for r in valid_rsi if r > 70)}")
        print(f"  Дней в перепроданности (<30): {sum(1 for r in valid_rsi if r < 30)}")

    if valid_macd:
        print(f"\nMACD:")
        print(f"  Среднее: {sum(valid_macd) / len(valid_macd):.2f}")
        print(f"  Максимум: {max(valid_macd):.2f}")
        print(f"  Минимум: {min(valid_macd):.2f}")
        print(f"  Положительных значений: {sum(1 for m in valid_macd if m > 0)}/{len(valid_macd)}")

    if valid_hist:
        print(f"\nMACD Гистограмма:")
        print(f"  Положительных значений: {sum(1 for h in valid_hist if h > 0)}/{len(valid_hist)}")

    if valid_bull and valid_bear:
        print(f"\nBull Power:")
        print(f"  Положительных значений: {sum(1 for b in valid_bull if b > 0)}/{len(valid_bull)}")
        print(f"  Среднее: {sum(valid_bull) / len(valid_bull):.2f}")

        print(f"\nBear Power:")
        print(f"  Отрицательных значений: {sum(1 for b in valid_bear if b < 0)}/{len(valid_bear)}")
        print(f"  Среднее: {sum(valid_bear) / len(valid_bear):.2f}")

    print("\n" + "=" * 60)
    print("Краткий отчёт:")
    print("=" * 60)

    last_price = close_prices[-1]
    first_price = close_prices[0]
    price_change = ((last_price - first_price) / first_price) * 100

    print(f"Начальная цена: ${first_price:.2f}")
    print(f"Конечная цена:  ${last_price:.2f}")
    print(f"Изменение за период: {price_change:+.2f}%")

    signals_summary = []

    if mom_signals:
        signals_summary.append(f"Momentum: {mom_signals[-1][1]}")

    if rsi_signals:
        signals_summary.append(f"RSI: {rsi_signals[-1][1]}")

    if macd_signals:
        signals_summary.append(f"MACD: {macd_signals[-1][1]}")

    if signals_summary:
        print(f"\nПоследние сигналы:")
        for signal in signals_summary:
            print(f"  {signal}")


    buy_signals = sum(1 for s in [mom_signals, rsi_signals, macd_signals]
                      if s and "BUY" in s[-1][1])
    sell_signals = sum(1 for s in [mom_signals, rsi_signals, macd_signals]
                       if s and "SELL" in s[-1][1])

    if buy_signals > sell_signals:
        print(
            f"\nОбщая рекомендация: ↑ Преобладают покупательские сигналы ({buy_signals}/{buy_signals + sell_signals})")
    elif sell_signals > buy_signals:
        print(f"\nОбщая рекомендация: ↓ Преобладают продажные сигналы ({sell_signals}/{buy_signals + sell_signals})")
    else:
        print(f"\nОбщая рекомендация: ↔ Нейтрально (сигналы сбалансированы)")


if __name__ == "__main__":
    main()