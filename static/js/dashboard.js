async function atualizarDashboard() {

    const response = await fetch("/api/status");

    const data = await response.json();

    document.getElementById(
        "alertas"
    ).innerText = data.alertas;

    document.getElementById(
        "registros"
    ).innerText = data.registros;

    const tabela = document.getElementById(
        "sensores-body"
    );

    tabela.innerHTML = "";

    data.sensores.forEach(sensor => {

        tabela.innerHTML += `

            <tr>

                <td>${sensor.sensor}</td>

                <td>${sensor.tipo}</td>

                <td>${sensor.valor}</td>

            </tr>
        `;
    });
}

setInterval(
    atualizarDashboard,
    2000
);

atualizarDashboard();