const ctx = document
    .getElementById("energiaChart");

const energiaChart = new Chart(ctx, {

    type: "line",

    data: {

        labels: [],

        datasets: [

            {
                label: "Consumo Energético",

                data: [],

                tension: 0.4
            },

            {
                label: "Geração Solar",

                data: [],

                tension: 0.4
            },

            {
                label: "Geração Eólica",

                data: [],

                tension: 0.4
            }
        ]
    },

    options: {

        responsive: true,

        animation: true,

        scales: {

            y: {

                beginAtZero: true
            }
        }
    }
});

function atualizarGrafico(data) {

    energiaChart.data.labels.push(
        data.timestamp
    );

    energiaChart.data.datasets[0].data.push(
        data.consumo
    );

    energiaChart.data.datasets[1].data.push(
        data.solar
    );

    energiaChart.data.datasets[2].data.push(
        data.eolica
    );

    if (
        energiaChart.data.labels.length > 20
    ) {

        energiaChart.data.labels.shift();

        energiaChart.data.datasets.forEach(
            dataset => dataset.data.shift()
        );
    }

    energiaChart.update();
}