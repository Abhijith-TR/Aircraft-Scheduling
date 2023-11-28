# Aircraft-Scheduling
Library with various optimization algorithms created as a part of the term paper in CS512 - Artificial Intelligence.

The code is arranged as follows:

* `optimisation` : Contains the code for the optimisation algorithms (BCO, GA and FCFS)
* `problem`: Contains the code for the problem formulation and RHC optimiser
* `tests`: Contains the code for the unit tests
* `utils`: Contains the code for input utility functions
* `dataset` : Contains the IKLI dataset
* `data` : Contains parsed input text files
* `images`: Contains plots and images used in the report
* `result.py` and `result.ipynb`: Contain code for generating plots and images used in the report

## Running the code

### Requirements
Set up a virtual environment and install the requirements using the following commands:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

or on windows:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Running the code
The code can be run from the `run.ipynb` file. It contains example code for running the optimisation algorithms on the IKLI dataset as well as comparison with the previous paper. Ensure that the correct kernel is selected before running the code.

The code can be run on any dataset by changing the input file in the `run.ipynb` file.
