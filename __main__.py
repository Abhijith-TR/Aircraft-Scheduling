import typing


class Aeroplane:
    """
    Class to store airplane details

    Attributes:
        ac_type: Type of airplane
        eta_etd: List of eta and etd
        delay_cost: Cost of delay
        pre_cost: Cost of preponement
    """
    ac_type: int
    eta_etd: list[int]
    delay_cost: int
    pre_cost: int

    def __init__(self, ac_type: int, eta_etd: list[int], delay_cost: int, pre_cost: int):
        """
        Constructor for Aeroplane class

        :param ac_type: Type of airplane
        :param eta_etd: List of eta and etd to all runways
        :param delay_cost: Cost of arrival later than eta
        :param pre_cost: Cost of arrival earlier than eta
        """
        self.ac_type = ac_type
        self.eta_etd = eta_etd
        self.delay_cost = delay_cost
        self.pre_cost = pre_cost


def input_ac_details(no_of_ac: int, file: typing.TextIO):
    """
    Function to input airplane details

    :param no_of_ac: No of airplanes to input
    :param file: File object to read from
    :return: List of Aeroplane objects
    """
    ac_list = []
    for i in range(no_of_ac):
        ac_details = list(map(int, file.readline().split()))
        aeroplane = Aeroplane(
            ac_details[0], ac_details[1:-2], ac_details[-2], ac_details[-1]
        )
        ac_list.append(aeroplane)
    return ac_list


def read_input():
    """
    Function to read input from file

    :return: Tuple of input values such as no of runways,
    no of airplane types, separation matrix, landing airplanes,
    takeoff airplanes
    """
    with open("input.txt", "r") as f:
        no_of_runways = int(f.readline())
        no_of_ac_types = int(f.readline())

        separation_matrix = []
        for i in range(no_of_ac_types):
            separation_matrix.append(list(map(int, f.readline().split())))

        no_of_landing_ac = int(f.readline())
        landing_ac = input_ac_details(no_of_landing_ac, f)

        no_of_takeoff_ac = int(f.readline())
        takeoff_ac = input_ac_details(no_of_takeoff_ac, f)

    return (
        no_of_runways,
        no_of_ac_types,
        separation_matrix,
        landing_ac,
        takeoff_ac,
    )


if __name__ == "__main__":
    main()
