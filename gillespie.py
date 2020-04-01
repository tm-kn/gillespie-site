import math
import random


class GillespiePoint:
    def __init__(
        self,
        *,
        time: float,
        susceptible_population: int,
        infected_population: int,
        recovered_population: int
    ):
        self.time = time
        self.susceptible_population = susceptible_population
        self.infected_population = infected_population
        self.recovered_population = recovered_population

    def as_dict(self):
        return {
            "time": self.time,
            "susceptible_population": self.susceptible_population,
            "infected_population": self.infected_population,
            "recovered_population": self.recovered_population,
        }


def gillespie(
    *,
    population: int,
    maximum_elapsed_time: float,
    start_time: float,
    spatial_parameter: float,
    rate_of_infection_after_contact: float,
    rate_of_cure: float,
    infected_population: int
):
    susceptible_population = population - infected_population
    recovered = 0
    yield GillespiePoint(
        time=start_time,
        susceptible_population=susceptible_population,
        infected_population=infected_population,
        recovered_population=recovered,
    )
    time = start_time
    while time < maximum_elapsed_time:
        if infected_population == 0:
            break
        w1 = (
            rate_of_infection_after_contact
            * susceptible_population
            * infected_population
            / spatial_parameter
        )
        w2 = rate_of_cure * infected_population
        w = w1 + w2
        dt = -math.log(random.uniform(0.0, 1.0)) / w
        time += dt
        if random.uniform(0.0, 1.0) < w1 / w:
            susceptible_population = susceptible_population - 1
            infected_population = infected_population + 1
        else:
            infected_population = infected_population - 1
            recovered += 1
        yield GillespiePoint(
            time=time,
            susceptible_population=susceptible_population,
            infected_population=infected_population,
            recovered_population=recovered,
        )
