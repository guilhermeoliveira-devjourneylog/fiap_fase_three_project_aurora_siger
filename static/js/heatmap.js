function gerarCor(valor) {

    if (valor < 1000)
        return "#00c853";

    if (valor < 2500)
        return "#ffd600";

    if (valor < 3500)
        return "#ff6d00";

    return "#d50000";
}

function atualizarHeatmap(sensores) {

    const heatmap =
        document.getElementById(
            "heatmap"
        );

    heatmap.innerHTML = "";

    sensores.forEach(sensor => {

        const cell =
            document.createElement("div");

        cell.className = "heat-cell";

        cell.style.background =
            gerarCor(sensor.valor);

        cell.innerHTML = `

            <div>

                <strong>
                    ${sensor.sensor}
                </strong>

                <br>

                ${sensor.valor}

            </div>
        `;

        heatmap.appendChild(cell);
    });
}