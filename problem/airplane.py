class Airplane:
    """
    Class to store airplane details

    Attributes:
        ac_type: Type of airplane
        eta_etd: List of eta and etd
        delay_cost: Cost of delay
        pre_cost: Cost of preponement
    """

    ac_type: int
    input_time: int
    starting_time: int
    ending_time: int
    eta_etd: list[int]
    delay_cost: int
    pre_cost: int

    def __init__(
        self,
        ac_type: int,
        input_time: int,
        starting_time: int,
        ending_time: int,
        eta_etd: list[int],
        delay_cost: int,
        pre_cost: int,
    ):
        """
        Constructor for Airplane class

        :param ac_type: Type of airplane
        :param eta_etd: List of eta and etd to all runways
        :param delay_cost: Cost of arrival later than eta
        :param pre_cost: Cost of arrival earlier than eta
        """
        self.ac_type = ac_type
        self.input_time = input_time
        self.starting_time = starting_time
        self.ending_time = ending_time
        self.eta_etd = eta_etd
        self.delay_cost = delay_cost
        self.pre_cost = pre_cost
