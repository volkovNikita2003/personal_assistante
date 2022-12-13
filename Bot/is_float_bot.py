from Bot import bot_float_sep


def _isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_float_bot(s, float_sep):
    """
    Accepts a string - the message to the bot.
    Returns 'True' if the string is a number (int/float) with 'float_sep' else 'False'
    """
    value = s.strip()
    parts = value.split(float_sep, 1)
    if len(parts) == 1:
        # is int?
        return _isint(parts[0])
    elif len(parts) == 2:
        # is float?
        return _isint(parts[0]) and _isint(parts[1])
    return False
