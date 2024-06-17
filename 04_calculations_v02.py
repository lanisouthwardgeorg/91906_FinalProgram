def to_feet(to_convert):
    answer = to_convert * 3.281
    return answer


def to_metres(to_convert):
    answer = to_convert / 3.281
    return answer


to_f_test = [0, 100, 1800]
to_m_test = [0, 100, 1800]

for item in to_m_test:
    print("{} f is {:.0f} m".format(item, to_metres(item)))

print()

for item in to_f_test:
    print("{} m is {:.0f} f".format(item, to_feet(item)))
