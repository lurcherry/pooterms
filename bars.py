def hp_bar(current, maximum=100):

    filled = int((current / maximum) * 10)

    filled = max(0, min(10, filled))

    return "🟥" * filled + "⬜" * (10 - filled)


def exp_bar(current, maximum):

    filled = int((current / maximum) * 10)

    filled = max(0, min(10, filled))

    return "🟦" * filled + "⬜" * (10 - filled)


def durability_bar(current, maximum):

    filled = int((current / maximum) * 10)

    filled = max(0, min(10, filled))

    return "🟩" * filled + "⬜" * (10 - filled)