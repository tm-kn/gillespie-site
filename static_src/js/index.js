import "whatwg-fetch";
import "url-polyfill";
import "@babel/polyfill";

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

function getUrlParamsFromFormData() {
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
  return params;
}

function getChartUrl({
  population,
  maximumElapsedTime,
  startTime,
  spatialParameter,
  rateOfInfectionAfterContact,
  rateOfCure,
  infectedPopulation,
}) {
  return `/export-graph/png/?${getUrlParamsFromFormData()}`;
}

function loadChart() {
  const chartContainer = document.querySelector("#chart-container");
  chartContainer.innerHTML = "";
  const imageTag = document.createElement("img");
  imageTag.src = getChartUrl(getFormData());
  chartContainer.appendChild(imageTag);
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
    window.open(`/export-csv/?${getUrlParamsFromFormData()}`);
  });
}

function setUpDownloadJSONButton() {
  const button = document.querySelector("#download-json-button");
  button.addEventListener("click", () => {
    window.open(`/export-json/?${getUrlParamsFromFormData()}`);
  });
}

function setUpDownloadSVGButton() {
  const button = document.querySelector("#download-svg-button");
  button.addEventListener("click", () => {
    window.open(`/export-graph/svg/?${getUrlParamsFromFormData()}`);
  });
}

window.addEventListener("DOMContentLoaded", () => {
  loadChart();
  setUpForm();
  setUpDownloadCSVButton();
  setUpDownloadJSONButton();
  setUpDownloadSVGButton();
});
