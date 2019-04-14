from dateutil.relativedelta import relativedelta


def diff(t_a, t_b):
    t_diff = relativedelta(t_b, t_a)
    return '{h}h {m}m {s}s {ms}ms'.format(h=t_diff.hours, m=t_diff.minutes, s=t_diff.seconds, ms=t_diff.microseconds)
