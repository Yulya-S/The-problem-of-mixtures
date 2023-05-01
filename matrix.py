def subtract_from_line(what_to_take_away, which_line_to_apply, multiply_by):
    copy = what_to_take_away.copy()
    line = multiply_line(copy, multiply_by)
    for i in range(len(which_line_to_apply)):
        which_line_to_apply[i] -= line[i]


def multiply_line(line, multyply_by):
    for i in range(len(line)):
        line[i] *= multyply_by
    return line


def divide_line(line, divide_by):
    for i in range(len(line)):
        line[i] /= divide_by
    return line
