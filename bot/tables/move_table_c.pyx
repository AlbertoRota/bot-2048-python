# cython: language_level=3

cdef dict get_move_table():
    cdef short max_cell, cell_1, cell_2, cell_3, cell_4
    cdef short row[4]
    cdef short values[17]

    move_table = {}

    for cell_1 in range(17):
        for cell_2 in range(17):
            for cell_3 in range(17):
                for cell_4 in range(17):
                    row = [cell_1, cell_2, cell_3, cell_4]
                    move_table[row] = swipe_row_left(row)

    return move_table


cdef short[:] swipe_row_left(short[:] row):
    cdef short last_non_zero, first_free_cell, cell
    cdef short new_row[4]

    last_non_zero = -1
    first_free_cell = 0

    for i in range(len(row)):
        cell = row[i]
        if cell != 0:
            if cell == last_non_zero:
                new_row[first_free_cell - 1] = last_non_zero + 1
                last_non_zero = -1
            else:
                last_non_zero = cell
                new_row[first_free_cell] = cell
                first_free_cell += 1

    return new_row
