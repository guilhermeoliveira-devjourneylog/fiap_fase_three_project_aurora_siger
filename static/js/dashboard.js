// =========================================================
// AURORA SIGER - DASHBOARD FRONT-END
// =========================================================
//
// Responsável por:
//
// - Atualização automática da interface
// - Comunicação com API Flask
// - Atualização dos painéis
// - Atualização da tabela de sensores
// - Atualização do gráfico Chart.js
// - Atualização do heatmap energético
// - Controle visual de status
//
// =========================================================


// =========================================================
// ELEMENTOS HTML
// =========================================================

const sensoresBody =
    document.getElementById(
        "sensores-body"
    );

const alertasElement =
    document.getElementById(
        "alertas"
    );

const registrosElement =
    document.getElementById(
        "registros"
    );

const statusElement =
    document.getElementById(
        "status-operacional"
    );

const timestampElement =
    document.getElementById(
        "timestamp"
    );


// =========================================================
// VALIDAÇÃO CHART.JS
// =========================================================

if (typeof Chart === "undefined") {

    console.error(
        "Chart.js não foi carregado."
    );
}


// =========================================================
// CHART.JS
// =========================================================

const chartContext =
    document.getElementById(
        "energiaChart"
    );

let energiaChart = null;

if (chartContext && typeof Chart !== "undefined") {

    energiaChart = new Chart(
        chartContext,
        {

            type: "line",

            data: {

                labels: [],

                datasets: [

                    {
                        label: "Consumo Energético",

                        data: [],

                        borderColor: "#ff6d00",

                        backgroundColor:
                            "rgba(255,109,0,0.1)",

                        borderWidth: 3,

                        tension: 0.4
                    },

                    {
                        label: "Geração Solar",

                        data: [],

                        borderColor: "#ffd600",

                        backgroundColor:
                            "rgba(255,214,0,0.1)",

                        borderWidth: 3,

                        tension: 0.4
                    },

                    {
                        label: "Geração Eólica",

                        data: [],

                        borderColor: "#00c853",

                        backgroundColor:
                            "rgba(0,200,83,0.1)",

                        borderWidth: 3,

                        tension: 0.4
                    }
                ]
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                animation: {

                    duration: 800
                },

                plugins: {

                    legend: {

                        labels: {

                            color: "white"
                        }
                    }
                },

                scales: {

                    x: {

                        ticks: {

                            color: "white"
                        },

                        grid: {

                            color: "#30363d"
                        }
                    },

                    y: {

                        beginAtZero: true,

                        ticks: {

                            color: "white"
                        },

                        grid: {

                            color: "#30363d"
                        }
                    }
                }
            }
        }
    );
}


// =========================================================
// HEATMAP
// =========================================================

function gerarCorHeatmap(valor) {

    if (valor < 500) {

        return "#00c853";
    }

    if (valor < 1500) {

        return "#64dd17";
    }

    if (valor < 2500) {

        return "#ffd600";
    }

    if (valor < 3500) {

        return "#ff6d00";
    }

    return "#d50000";
}


// =========================================================
// ATUALIZA HEATMAP
// =========================================================

function atualizarHeatmap(
    sensores
) {

    const heatmap =
        document.getElementById(
            "heatmap"
        );

    if (!heatmap) {

        return;
    }

    heatmap.innerHTML = "";

    sensores.forEach(sensor => {

        const cell =
            document.createElement(
                "div"
            );

        cell.classList.add(
            "heat-cell"
        );

        cell.style.background =
            gerarCorHeatmap(
                sensor.valor
            );

        cell.innerHTML = `

            <div class="heat-content">

                <strong>
                    ${sensor.sensor}
                </strong>

                <br>

                <span>
                    ${sensor.valor}
                </span>

            </div>
        `;

        heatmap.appendChild(
            cell
        );
    });
}


// =========================================================
// ATUALIZA TABELA
// =========================================================

function atualizarTabelaSensores(
    sensores
) {

    if (!sensoresBody) {

        return;
    }

    sensoresBody.innerHTML = "";

    sensores.forEach(sensor => {

        let classeValor =
            "valor-normal";

        // =============================================
        // CLASSIFICAÇÃO VISUAL
        // =============================================

        if (sensor.valor > 3000) {

            classeValor =
                "valor-critico";
        }

        else if (
            sensor.valor > 2000
        ) {

            classeValor =
                "valor-alerta";
        }

        const row =
            document.createElement(
                "tr"
            );

        row.innerHTML = `

            <td>
                ${sensor.sensor}
            </td>

            <td>
                ${sensor.tipo}
            </td>

            <td class="${classeValor}">
                ${sensor.valor}
            </td>
        `;

        sensoresBody.appendChild(
            row
        );
    });
}


// =========================================================
// ATUALIZA GRÁFICO
// =========================================================

function atualizarGrafico(
    data
) {

    if (!energiaChart) {

        return;
    }

    energiaChart.data.labels.push(
        data.timestamp
    );

    energiaChart.data.datasets[0].data.push(
        data.consumo || 0
    );

    energiaChart.data.datasets[1].data.push(
        data.solar || 0
    );

    energiaChart.data.datasets[2].data.push(
        data.eolica || 0
    );

    // =============================================
    // LIMITA HISTÓRICO
    // =============================================

    const limite = 20;

    if (
        energiaChart.data.labels.length
        > limite
    ) {

        energiaChart.data.labels.shift();

        energiaChart.data.datasets.forEach(
            dataset => {

                dataset.data.shift();
            }
        );
    }

    energiaChart.update();
}


// =========================================================
// STATUS OPERACIONAL
// =========================================================

function atualizarStatus(
    data
) {

    // =============================================
    // ALERTAS
    // =============================================

    if (alertasElement) {

        alertasElement.innerText =
            data.alertas;
    }

    // =============================================
    // REGISTROS
    // =============================================

    if (registrosElement) {

        registrosElement.innerText =
            data.registros;
    }

    // =============================================
    // TIMESTAMP
    // =============================================

    if (timestampElement) {

        timestampElement.innerText =
            data.timestamp;
    }

    // =============================================
    // STATUS
    // =============================================

    if (!statusElement) {

        return;
    }

    if (
        data.alertas > 10
    ) {

        statusElement.innerText =
            "CRÍTICO";

        statusElement.className =
            "status-critico";
    }

    else if (
        data.alertas > 5
    ) {

        statusElement.innerText =
            "ALERTA";

        statusElement.className =
            "status-alerta";
    }

    else {

        statusElement.innerText =
            "OPERACIONAL";

        statusElement.className =
            "status-online";
    }
}


// =========================================================
// FETCH API
// =========================================================

async function buscarDadosSistema() {

    try {

        const response =
            await fetch(
                "/api/status"
            );

        // =========================================
        // VERIFICA RESPOSTA
        // =========================================

        if (!response.ok) {

            throw new Error(
                "Erro na API Flask"
            );
        }

        const data =
            await response.json();

        // =========================================
        // LOG DEBUG
        // =========================================

        console.log(
            "Dados recebidos:",
            data
        );

        // =========================================
        // ATUALIZA COMPONENTES
        // =========================================

        atualizarTabelaSensores(
            data.sensores
        );

        atualizarHeatmap(
            data.sensores
        );

        atualizarGrafico(
            data
        );

        atualizarStatus(
            data
        );

    } catch (error) {

        console.error(
            "Erro ao atualizar dashboard:",
            error
        );

        if (statusElement) {

            statusElement.innerText =
                "OFFLINE";

            statusElement.className =
                "status-offline";
        }
    }
}


// =========================================================
// LOOP PRINCIPAL
// =========================================================

setInterval(

    buscarDadosSistema,

    2000
);


// =========================================================
// INICIALIZAÇÃO
// =========================================================

window.onload = () => {

    console.log(
        "AURORA SIGER ONLINE"
    );

    buscarDadosSistema();
};