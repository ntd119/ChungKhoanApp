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
  
  async function loadIntoTable(url, table) {
    const tableHead = table.querySelector("thead");
    const tableBody = table.querySelector("tbody");
    const response = await fetch(url);
    const rows = await response.json();

    // clear the table
    tableHead.innerHTML = "<tr></tr>";
    tableBody.innerHTML = "";

    // Populate the header
    for (const headerText of HEADER_TABLE) {
      const headerElement = document.createElement("th");
      headerElement.textContent = headerText;
      tableHead.querySelector("tr").appendChild(headerElement);
    }

    $.getJSON(
      "https://s.cafef.vn/ajax/marketmap.ashx?stock=1&type=1&cate=",
      function (response) {
        for (const key in rows) {
          filter_data = response.filter((x) => x.NoneSymbol === key)[0];
          console.log(filter_data);

          const rowElement = document.createElement("tr");

          // Mã chứng khoán
          const maCKElement = document.createElement("td");
          maCKElement.textContent = key;
          rowElement.appendChild(maCKElement);

          // Tên
          const nameElement = document.createElement("td");
          // nameElement.textContent = filter_data["Name"];
          rowElement.appendChild(nameElement);

          // Status
          const statusElement = document.createElement("td");
          statusElement.textContent = "";
          rowElement.appendChild(statusElement);

          // Giá đã mua
          giaDaMua =  rows[key]["bought"]
          const giaMuaElement = document.createElement("td");
          giaMuaElement.textContent = giaDaMua;
          rowElement.appendChild(giaMuaElement);

           // Status
           giaHienTai = filter_data["Price"] * 1000

           percent_change = parseFloat( ((giaHienTai - giaDaMua) / giaDaMua) * 100).toFixed(2)
           const laiLoElement = document.createElement("td");
           if (percent_change >=0) {
            laiLoElement.style.cssText = ' background-color:#00E11A;';
           } else {
            laiLoElement.style.cssText = ' background-color:#F33232;';
           }
           laiLoElement.textContent = percent_change + "%";
           rowElement.appendChild(laiLoElement);

            // Giá hiện tại 
            const giaHienTaiElement = document.createElement("td");
            giaHienTaiElement.textContent = giaHienTai;
            rowElement.appendChild(giaHienTaiElement);

          tableBody.appendChild(rowElement);
        }
      }
    );
  }

  loadIntoTable(
    "./HoiPhaDaoCK_Web/data/da_mua.json",
    document.querySelector("table")
  );
});
