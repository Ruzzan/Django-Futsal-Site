def proper_paginator(futsals, index):
    start_index = 0
    end_index   = 7
    if futsals.number > index:
        start_index = futsals.number - index
        end_index   = futsals.number + index
    return (start_index, end_index)