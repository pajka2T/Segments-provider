let form = document.getElementById("form")

form.addEventListener('submit', async function(e) {
    e.preventDefault();

    let textInput = document.getElementsByClassName("form-control");
    let radioInput = document.getElementsByName('typeOfActivity');

    let address = textInput[0].value;
    let radius = Number(textInput[1].value);
    console.log(typeof(radius), radioInput[0].value, radioInput[1].value);

    let type = radioInput[0].checked == true ? radioInput[0].value : radioInput[1].value;
    console.log(type)

    let segments = null;

    let resDiv = document.getElementById("resultsDiv");
    let resTabBody = document.getElementById("resultsBody");
    resTabBody.replaceChildren();
    if (document.getElementById("nothingInfo") != null)
        document.getElementById("nothingInfo").remove();

    resDiv.style.display = "block";

    const url = `http://127.0.0.1:8000/segments/address=${address}&radius=${radius}&type=${type}`
    await fetch(url, {
        method: "GET"
    })
    .then(response => response.json())
    .then(data => segments = data)
    .catch(err => console.log(err));
    console.log(segments);

    segments = segments["results"];
    
    if (segments.length === 0) {
        let nothingFound = document.createElement("trow");
        let info = document.createElement("p");
        info.textContent = "No segments found";
        nothingFound.appendChild(info);
        nothingFound.id = "nothingInfo";
        nothingFound.classList.add("text-center");
        resDiv.appendChild(nothingFound);
    }
    else {
        var ind = 1;
        for (segment of segments) {
            let row = document.createElement("tr");

            let numberCol = document.createElement("td");
            numberCol.textContent = ind;
            row.appendChild(numberCol);
            ind += 1;

            let nameCol = document.createElement("td");
            nameCol.textContent = segment["name"];
            row.appendChild(nameCol);
            let distCol = document.createElement("td");
            distCol.textContent = segment["distance"];
            row.appendChild(distCol);
            let elevCol = document.createElement("td");
            elevCol.textContent = segment["elevation"];
            row.appendChild(elevCol);
            let avgGradeCol = document.createElement("td");
            avgGradeCol.textContent = segment["avg_grade"];
            row.appendChild(avgGradeCol);
            let noEffortsCol = document.createElement("td");
            noEffortsCol.textContent = segment["no_efforts"];
            row.appendChild(noEffortsCol);
            let noAthletesCol = document.createElement("td");
            noAthletesCol.textContent = segment["no_athletes"];
            row.appendChild(noAthletesCol);
            let noStarsCol = document.createElement("td");
            noStarsCol.textContent = segment["no_stars"];
            row.appendChild(noStarsCol);
            let komCol = document.createElement("td");
            komCol.textContent = segment["kom"] === null ? "Not available" : segment["kom"];
            row.appendChild(komCol);
            let qomCol = document.createElement("td");
            qomCol.textContent = segment["qom"] === null ? "Not available" : segment["qom"];
            row.appendChild(qomCol);
            let llCol = document.createElement("td");
            llCol.textContent = segment["ll"] === null ? "Not available" : segment["ll"];
            row.appendChild(llCol);
            let llNoEffortsCol = document.createElement("td");
            llNoEffortsCol.textContent = segment["ll_no_efforts"] === null ? "Not available" : segment["ll_no_efforts"];
            row.appendChild(llNoEffortsCol);
            resTabBody.appendChild(row);
        }
    }
});

document.getElementById('radiusInput').addEventListener('keypress', (e) => {
    if (["-", "+", "e"].includes(e.key))
        e.preventDefault();
});
