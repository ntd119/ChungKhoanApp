

$(document).ready(function () {
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

    async function loadIntoTable(url, table){
        const tableHead = table.querySelector("thead");
        const tableBody = table.querySelector("tbody");
        const response = await fetch(url);
        const rows = await response.json();
    
        // clear the table
        tableHead.innerHTML = "<tr></tr>";
        tableBody.innerHTML = "";

        // Populate the header
        headers = ["A", "B"];
        for(const headerText of headers) {
            const headerElement = document.createElement("th");
            headerElement.textContent = headerText;
            tableHead.querySelector("tr").appendChild(headerElement);
        }

        // Populate the row
        for(const row of rows) {
            const rowElement = document.createElement("tr");
            
            for(const cellText of row) {
                const cellElement = document.createElement("td");
                cellElement.textContent = cellText;
                rowElement.appendChild(cellElement);
            }

            tableBody.appendChild(rowElement);
        }
    }
    
    loadIntoTable("./HoiPhaDaoCK_Web/data/da_mua.json", document.querySelector("table"));
});

