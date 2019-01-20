"""Solve the spy game!"""

import string
import math

all_characters = string.ascii_uppercase
matrix_width, matrix_height = 10, 10;


# column_shift, row_shift
coordinate_shifts = [
    [0, -1],
    [-1, 0], [1, 0],
    [0, 1]
]

def print_matrix(A):
    for row in A:
        for item in row:
            print('{:4}'.format(item), end='')
        print('\n', end='')


class SafetyFinder:
    """A class that contains everything we need to find the
    safest places in the city for Alex to hide out
    """

    def convert_alphanumeric_coordinate(self, agent):
        x_coordinate = all_characters.find(agent[0])
        y_coordinate = int(agent[1:]) - 1
        return [x_coordinate, y_coordinate]

    def convert2alphanumeric_coordinate(self, agent):
        first_char = all_characters[agent[0]]
        second_number = agent[1] + 1
        return first_char + str(second_number)


    def convert_coordinates(self, agents):

        """This method should take a list of alphanumeric coordinates (e.g. 'A6')
        and return an array of the coordinates converted to arrays with zero-indexing.
        For instance, 'A6' should become [0, 5]

        Arguments:
        agents -- a list-like object containing alphanumeric coordinates.

        Returns a list of coordinates in zero-indexed vector form.
        """
        return list(map(lambda a: self.convert_alphanumeric_coordinate(a), agents))


    def find_safe_spaces(self, agents):
        """This method will take an array with agent locations and find
        the safest places in the city for Alex to hang out.

        Arguments:
        agents -- a list-like object containing the map coordinates of agents.
            Each entry should be formatted in indexed vector form,
            e.g. [0, 5], [3, 7], etc.

        Returns a list of safe spaces in indexed vector form.
        """

        # initialize distance matrix with infinity
        distance_matrix = [[math.inf for x in range(matrix_width)] for y in range(matrix_height)]

        flood_items = agents
        flood_step = 0
        while flood_items:
            new_flood_items = []
            for flood_item in flood_items:
                [column_index, row_index] = flood_item
                # update distance matrix for the current item if it is within matrix & greater
                if 0 <= column_index < matrix_width and 0 <= row_index < matrix_height and flood_step < distance_matrix[row_index][column_index]:
                    distance_matrix[row_index][column_index] = flood_step

                    # get new neighbeiring items
                    for shift in coordinate_shifts:
                        column_index_new = column_index + shift[0]
                        row_index_new = row_index + shift[1]
                        new_flood_items.append([ column_index_new, row_index_new])

            flood_items = new_flood_items
            flood_step += 1
            # print_matrix(distance_matrix)
            # print('-----------')


        # find the max value in the matrix
        max_distance = max(map(max, distance_matrix))

        # return all coordinates with the max value
        safe_coordinates = []
        for row_index, row in enumerate(distance_matrix):
           for column_index, distance in enumerate(row):
                if distance == max_distance:
                    safe_coordinates.append([column_index, row_index])

        return sorted(safe_coordinates)

    def advice_for_alex(self, agents):
        """This method will take an array with agent locations and offer advice
        to Alex for where she should hide out in the city, with special advice for
        edge cases.

        Arguments:
        agents -- a list-like object containing the map coordinates of the agents.
            Each entry should be formatted in alphanumeric form, e.g. A10, E6, etc.

        Returns either a list of alphanumeric map coordinates for Alex to hide in,
        or a specialized message informing her of edge cases
        """
        agents_coordinates = self.convert_coordinates(agents)
        safe_places = self.find_safe_spaces(agents_coordinates)

        if not safe_places:
            return "There are no safe locations for Alex! :-("
        elif len(safe_places) == (matrix_width * matrix_height):
            return "The whole city is safe for Alex! :-)"

        return list(map(lambda x: self.convert2alphanumeric_coordinate(x), safe_places))


s = SafetyFinder()

# Level1
# print(s.convert_coordinates([]))
# print(s.convert_coordinates(['F3']))
# print(s.convert_coordinates(['B6', 'C2', 'J7']))
# print(s.convert_coordinates(['J10']))

# Level2
# print(s.find_safe_spaces([[1, 1], [3, 5], [4, 8], [7, 3], [7, 8], [9, 1]]))
# print(s.find_safe_spaces([[0, 0], [0, 9], [1, 5], [5, 1], [9, 0], [9, 9]]))
# print(s.find_safe_spaces([[0, 0]]))

# Level3
# print(s.advice_for_alex([]))
# agents_everywhere = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10',
#                   'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10',
#                   'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
#                   'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10',
#                   'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10',
#                   'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10',
#                   'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10',
#                   'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10',
#                   'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10',
#                   'J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10']
# print(s.advice_for_alex(agents_everywhere))

# print(s.advice_for_alex(['B2', 'D6', 'E9', 'H4', 'H9', 'J2']))
# print(s.advice_for_alex(['B4', 'C4', 'C8', 'E2', 'F10', 'H1', 'J6']))
# print(s.advice_for_alex(['A1', 'A10', 'B6', 'F2', 'J1', 'J10']))
# print(s.advice_for_alex(['A1']))
# print(s.advice_for_alex(['A12']))
