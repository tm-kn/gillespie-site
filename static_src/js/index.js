import "whatwg-fetch";
import "url-polyfill";
import "@babel/polyfill";
import Highcharts from "highcharts";
import HighchartsExporting from "highcharts/modules/exporting";
HighchartsExporting(Highcharts);

function getFormData() {
  return {
    population: document.querySelector("#population").value,
    maximumElapsedTime: document.querySelector("#maximum_elapsed_time").value,
    startTime: document.querySelector("#start_time").value,
    spatialParameter: document.querySelector("#spatial_parameter").value,
    rateOfInfectionAfterContact: document.querySelector(
      "#rate_of_infection_after_contact"
    ).value,
    rateOfCure: document.querySelector("#rate_of_cure").value,
    infectedPopulation: document.querySelector("#infected_population").value,
  };
}

async function fetchData({
  population,
  maximumElapsedTime,
  startTime,
  spatialParameter,
  rateOfInfectionAfterContact,
  rateOfCure,
  infectedPopulation,
}) {
  const params = new URLSearchParams();
  params.set("population", population);
  params.set("maximum_elapsed_time", maximumElapsedTime);
  params.set("start_time", startTime);
  params.set("spatial_parameter", spatialParameter);
  params.set("rate_of_infection_after_contact", rateOfInfectionAfterContact);
  params.set("rate_of_cure", rateOfCure);
  params.set("infected_population", infectedPopulation);
  const response = await fetch(`/data/?${params}`, {
    headers: {
      accept: "application/json",
    },
  });
  if (!response.ok) {
    throw new Error(`Unexpected HTTP Error: ${response.statusText}`);
  }
  return await response.json();
}

async function loadChart() {
  const chartContainer = document.querySelector("#chart-container");
  const data = await fetchData(getFormData());

  Highcharts.chart(chartContainer, {
    title: {
      text: "Susceptible, Infected and Recovered - cases vs. log (time)",
    },

    subtitle: {
      text: "SIR model - Gillespie algorithm solution",
    },

    yAxis: {
      title: {
        text: "Cases from 1 index case",
      },
    },

    xAxis: {
      title: {
        text: "Tme units (generic) log scale",
      },
    },

    legend: {
      layout: "vertical",
      align: "right",
      verticalAlign: "middle",
    },

    plotOptions: {
      series: {
        turboThreshold: 0,
      },
    },

    series: [
      {
        name: "Susceptible",
        data: data.map(({ susceptible_population, time }) => ({
          y: susceptible_population,
          x: time,
        })),
      },
      {
        name: "Infected",
        data: data.map(({ infected_population, time }) => ({
          y: infected_population,
          x: time,
        })),
      },
      {
        name: "Recovered",
        data: data.map(({ recovered_population, time }) => ({
          y: recovered_population,
          x: time,
        })),
      },
    ],

    responsive: {
      rules: [
        {
          condition: {
            maxWidth: 500,
          },
          chartOptions: {
            legend: {
              layout: "horizontal",
              align: "center",
              verticalAlign: "bottom",
            },
          },
        },
      ],
    },
  });
}

function setUpForm() {
  const form = document.querySelector("#algorithm-paramters-form");
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    loadChart();
  });
}

function setUpDownloadCSVButton() {
  const button = document.querySelector("#download-csv-button");
  button.addEventListener("click", () => {
    const params = new URLSearchParams();
    const {
      population,
      maximumElapsedTime,
      startTime,
      spatialParameter,
      rateOfInfectionAfterContact,
      rateOfCure,
      infectedPopulation,
    } = getFormData();
    params.set("population", population);
    params.set("maximum_elapsed_time", maximumElapsedTime);
    params.set("start_time", startTime);
    params.set("spatial_parameter", spatialParameter);
    params.set("rate_of_infection_after_contact", rateOfInfectionAfterContact);
    params.set("rate_of_cure", rateOfCure);
    params.set("infected_population", infectedPopulation);
    window.open(`/export-csv/?${params}`);
  });
}

window.addEventListener("DOMContentLoaded", () => {
  loadChart();
  setUpForm();
  setUpDownloadCSVButton();
});
