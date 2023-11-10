from typing import List


class Airplane:
    """
    Class to store airplane details

    Attributes
    ----------
    model : str
        Model of airplane
    ac_type : int
        Type of airplane
    eta_etd : List[int]
        List of eta and etd to all runways
    delay_cost : int
        Cost of arrival later than eta
    pre_cost : int
        Cost of arrival earlier than eta    

    """

    model: str
    ac_type: int
    input_time: int
    starting_time: int
    ending_time: int
    eta_etd: List[int]
    delay_cost: float
    pre_cost: float

    def __init__(
        self,
        model: str,
        ac_type: int,
        input_time: int,
        starting_time: int,
        ending_time: int,
        eta_etd: List[int],
        delay_cost: float,
        pre_cost: float,
    ):
        """
        Constructor for Airplane class

        :param ac_type: Type of airplane
        :param eta_etd: List of eta and etd to all runways
        :param delay_cost: Cost of arrival later than eta
        :param pre_cost: Cost of arrival earlier than eta
        """
        self.model = model
        self.ac_type = ac_type
        self.input_time = input_time
        self.starting_time = starting_time
        self.ending_time = ending_time
        self.eta_etd = eta_etd
        self.delay_cost = delay_cost
        self.pre_cost = pre_cost

    def __repr__(self):
        return f"Airplane({self.ac_type}, {self.eta_etd})"
