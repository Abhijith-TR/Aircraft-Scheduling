import typing
import pandas as pd
from problem.airplane import Airplane

def make_input_from_csv(
    path: str, num_runways: int, output_path: str = "./my_input.txt"
):
    """
    Creates input file in the required format from csv file

    :param path: Path to csv file
    :param num_runways: Number of runways
    :param output_path: Path to output file
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(str(num_runways) + "\n")
        f.writelines("3\n")
        f.writelines(["82 69 60\n", "131 69 60\n", "196 157 96\n"])
        ac_df = pd.read_csv(path)

        categories = {"Light": 1, "Medium": 2, "Heavy": 3}
        f.writelines(f"{len(ac_df)}\n")
        for _, row in ac_df.iterrows():
            file_row = f"{row['mdl']} {categories[row['category']]} {row['sta_s'] - 60*40} \
                {row['sta_s'] - 20*60} {row['sta_s'] + 20*60} "

            for _ in range(num_runways):
                file_row += f"{row['sta_s']} "

            file_row += f"{row['cost_5']} {row['cost_5']}\n"
            f.writelines(file_row)
        f.writelines("0\n")


def input_ac_details(no_of_ac: int, file: typing.TextIO):
    """
    Function to input airplane details

    :param no_of_ac: No of airplanes to input
    :param file: File object to read from
    :return: List of Airplane objects
    """
    ac_list = []
    for _ in range(no_of_ac):
        ac_details = list(map(str, file.readline().split()))
        aeroplane = Airplane(
            ac_details[0],
            int(ac_details[1]),
            int(ac_details[2]),
            int(ac_details[3]),
            int(ac_details[4]),
            [int(j) for j in ac_details[5:-2]],
            float(ac_details[-2]),
            float(ac_details[-1]),
        )
        ac_list.append(aeroplane)
    return ac_list


def read_input(path: str = "./my_input.txt"):
    """
    Function to read input from file

    :return: Tuple of input values such as no of runways,
    no of airplane types, separation matrix, landing airplanes,
    takeoff airplanes
    """
    with open(path, "r", encoding="utf-8") as f:
        no_of_runways = int(f.readline())
        no_of_ac_types = int(f.readline())

        separation_matrix = []
        for _ in range(no_of_ac_types):
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
