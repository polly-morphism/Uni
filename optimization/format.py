def add_positive(x0, y0, la0, dx, x, direction_norm):
    return f(
        x0 + ((la0 + dx) * x) / direction_norm, y0 + ((la0 + dx) * y) / direction_norm,
    )


def add_negative(x0, y0, la0, dx, x, direction_norm):
    return f(
        x0 + ((la0 - dx) * x) / direction_norm, y0 + ((la0 - dx) * y) / direction_norm,
    )


def svenn_DSK(direction, start, la0=0):
    """
    Алгоритм Свена
    """

    x0 = start[0]
    y0 = start[1]

    x = direction[0]
    y = direction[1]

    direction_norm = (x ** 2 + y ** 2) ** (1 / 2)

    nX = (x0 ** 2 + y0 ** 2) ** (1 / 2)

    dx = 0.1 * (nX / direction_norm)

    values_list = [
        f(x0 + ((la0) * x) / direction_norm, y0 + ((la0) * y) / direction_norm)
    ]
    la_list = [la0]

    if (
        add_negative(x0, y0, la0, dx, x, direction_norm)
        > f(x0 + ((la0) * x) / direction_norm, y0 + ((la0) * y) / direction_norm)
    ) and (
        f(x0 + ((la0) * x) / direction_norm, y0 + ((la0) * y) / direction_norm)
        > add_positive(x0, y0, la0, dx, x, direction_norm)
    ):
        determinator = 1
        values_list.append(add_positive(x0, y0, la0, dx, x, direction_norm))
        la_list.append(la0 + dx)
    elif (
        add_negative(x0, y0, la0, dx, x, direction_norm)
        < f(x0 + ((la0) * x) / direction_norm, y0 + ((la0) * y) / direction_norm)
    ) and (
        f(x0 + ((la0) * x) / direction_norm, y0 + ((la0) * y) / direction_norm)
        < add_positive(x0, y0, la0, dx, x, direction_norm)
    ):
        determinator = -1
        values_list.append(add_negative(x0, y0, la0, dx, x, direction_norm))
        la_list.append(la0 - dx)
    elif (
        add_negative(x0, y0, la0, dx, x, direction_norm)
        > f(x0 + ((la0) * x) / direction_norm, y0 + ((la0) * y) / direction_norm)
    ) and (
        f(x0 + ((la0) * x) / direction_norm, y0 + ((la0) * y) / direction_norm)
        < add_positive(x0, y0, la0, dx, x, direction_norm)
    ):
        return [la0 - dx, la0, la0 + dx]

    i = 1

    while values_list[i] < values_list[i - 1]:

        la_i = la_list[i] + determinator * (2 ** i) * dx
        la_list.append(la_i)

        values_list.append(
            f(x0 + ((la_i) * x) / direction_norm, y0 + ((la_i) * y) / direction_norm)
        )

        i += 1

    last4 = [
        la_list[i],
        (la_list[i] + la_list[i - 1]) / 2,
        la_list[i - 1],
        la_list[i - 2],
    ]
    last4_evaluated = []

    for la in last4:
        last4_evaluated.append(
            f(x0 + ((la) * x) / direction_norm, y0 + ((la) * y) / direction_norm)
        )

    inx = last4_evaluated.index(min(last4_evaluated))

    if inx == 1:
        last3 = [last4[0], last4[1], last4[2]]
    if inx == 2:
        last3 = [last4[1], last4[2], last4[3]]

    return last3
