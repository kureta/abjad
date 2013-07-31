# -*- encoding: utf-8 -*-
def make_desordre_pitches():

    right_hand = [
        [[-1, 4, 5], [-1, 4, 5, 7, 9]],
        [[0, 7, 9 ], [-1, 4, 5, 7, 9]],
        [[2, 4, 5, 7, 9], [0, 5, 7]],
        [[-3, -1, 0, 2, 4, 5, 7]],
        [[-3, 2, 4], [-3, 2, 4, 5, 7]],
        [[2, 5, 7], [ -3, 9, 11, 12, 14]],
        [[4, 5, 7, 9, 11], [2, 4, 5]],
        [[-5, 4, 5, 7, 9, 11, 12],],
        [[2, 9, 11], [2, 9, 11, 12, 14]],
        ]

    left_hand = [
        [[-9, -4, -2], [-9, -4, -2, 1, 3]],
        [[-6, -2, 1], [-9, -4, -2, 1, 3]],
        [[-4, -2, 1, 3, 6], [-4, -2, 1]],
        [[-9, -6, -4, -2, 1, 3, 6, 1]],
        [[-6, -2, 1], [-6, -2, 1, 3, -2]],
        [[-4, 1, 3], [-6, 3, 6, -6, -4]],
        [[-14, -11, -9, -6,-4], [-14, -11, -9]],
        [[-11, -2, 1, -6, -4, -2, 1, 3]],
        [[-6, 1, 3], [-6, -4, -2, 1, 3]],
        ]

    return [right_hand, left_hand]
