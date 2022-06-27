$(document).ready(function () {
  const HEADER_TABLE = [
    "",
    "Name",
    "Status",
    "Giá mua",
    "Lãi/Lỗ",
    "Giá hiện tại",
    "Giá min \ntrong tuần",
    "Giá max \ntrong tuần",
    "% Giá Max-Min",
    "% Giá hiện tại\nso với giá max",
    "Min Time",
    "Max Time",
    "Giá trần",
    "Giá sàn",
    "Giá mở cửa",
    "Có trong\nInfina",
  ];

  // $.getJSON('https://topchonlua.com/batch/data/stock_T0.json', function (response) {
  //     console.log(response);
  // });
  // $.ajax({
  //     url: 'https://topchonlua.com/batch/data/stock_T0.json',
  //     headers: {
  //         'Content-Type': 'application/x-www-form-urlencoded'
  //     },
  //     type: "GET",
  //     dataType: "json",
  //     data: {
  //     },
  //     success: function (result) {
  //         console.log(result);
  //     },
  //     error: function () {
  //         console.log("error");
  //     }
  // })
  async function vietstock_api() {
    $.ajax({
     // url: "https://api.vietstock.vn/finance/sectorInfo_v2?sectorID=0&catID=0&capitalID=0&languageID=1",
      url: "https://api.fireant.vn/instruments",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest"
        // "User-Agent":
        //   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
      },
      type: "GET",
      dataType: "json",
      data: {},
      success: function (result) {
        console.log(result);
      },
      error: function () {
        console.log("error");
      },
    });
  }

  vietstock_api();

  async function loadIntoTable(url, table) {
    const tableHead = table.querySelector("thead");
    const tableBody = table.querySelector("tbody");
    const response = await fetch(url);
    const rows = await response.json();

    // clear the table
    tableHead.innerHTML = "<tr></tr>";
    tableBody.innerHTML = "";

    // Populate the header
    headers = ["Mã ck", "Giá mua"];
    for (const headerText of HEADER_TABLE) {
      const headerElement = document.createElement("th");
      headerElement.textContent = headerText;
      tableHead.querySelector("tr").appendChild(headerElement);
    }

    for (const key in rows) {
      const rowElement = document.createElement("tr");

      // Mã chứng khoán
      const maCKElement = document.createElement("td");
      maCKElement.textContent = key;
      rowElement.appendChild(maCKElement);

      // Giá đã mua
      const giaMuaElement = document.createElement("td");
      giaMuaElement.textContent = rows[key]["bought"];
      rowElement.appendChild(giaMuaElement);

      tableBody.appendChild(rowElement);
    }
  }

  loadIntoTable(
    "./HoiPhaDaoCK_Web/data/da_mua.json",
    document.querySelector("table")
  );
});
