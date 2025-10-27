const csvUrl = "https://raw.githubusercontent.com/baraa-baba/webscraping-automation2/main/bitcoin_hourly_data.csv";

async function fetchCsvData() {
  try {
    const response = await fetch(csvUrl);
    if (!response.ok) {
      throw new Error("Network response was not ok " + response.statusText);
    }
    const csvText = await response.text();
    const rows = csvText.trim().split("\n").map(row => row.split(","));
    createTable(rows);
  } catch (error) {
    console.error("Error fetching CSV data:", error);
    document.getElementById("data-container").innerHTML = `<p style="color: red;">Failed to load data. Check console for details.</p>`;
  }
}

function createTable(rows) {
  let html = "<table><thead><tr>";
  rows[0].forEach(header => { html += `<th>${header}</th>`; });
  html += "</tr></thead><tbody>";
  for (let i = 1; i < rows.length; i++) {
    html += "<tr>";
    rows[i].forEach(cell => { html += `<td>${cell}</td>`; });
    html += "</tr>";
  }
  html += "</tbody></table>";
  document.getElementById("data-container").innerHTML = html;
}

window.addEventListener("DOMContentLoaded", fetchCsvData);