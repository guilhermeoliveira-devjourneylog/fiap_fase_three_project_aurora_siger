from flask import Flask, render_template, jsonify
from datetime import datetime
import random

# =========================================================
# IMPORTS DOS MÓDULOS
# =========================================================

from src.modules.SensorManager import (
    SensorManager,
    TipoSensor
)

from src.modules.StorageManager import (
    StorageManager
)

from src.modules.ProcessingEngine import (
    ProcessingEngine
)

from src.modules.PredictionEngine import (
    PredictionEngine
)

from src.modules.DecisionEngine import (
    DecisionEngine,
    EventoOperacional
)

from src.modules.AlertManager import (
    AlertManager,
    TipoAlerta,
    Severidade
)

# =========================================================
# FLASK
# =========================================================

app = Flask(__name__)

# =========================================================
# SISTEMA AURORA
# =========================================================

class AuroraSystem:

    def __init__(self):

        self.sensor_manager = SensorManager()
        self.storage_manager = StorageManager()
        self.processing_engine = ProcessingEngine()
        self.prediction_engine = PredictionEngine()
        self.decision_engine = DecisionEngine()
        self.alert_manager = AlertManager()

        self.registrar_sensores()

    def registrar_sensores(self):

        sensores = [

            ("TEMP-INT-01", TipoSensor.TEMPERATURA_INTERNA, 18, 32),
            ("TEMP-EXT-01", TipoSensor.TEMPERATURA_EXTERNA, -120, 50),
            ("VENTO-01", TipoSensor.VELOCIDADE_VENTO, 0, 180),
            ("SOLAR-01", TipoSensor.GERACAO_SOLAR, 0, 1200),
            ("EOLICA-01", TipoSensor.GERACAO_EOLICA, 0, 900),
            ("ENERGIA-01", TipoSensor.CONSUMO_ENERGETICO, 100, 4000),
            ("ESTRUTURA-01", TipoSensor.INTEGRIDADE_ESTRUTURAL, 70, 100)

        ]

        for sensor_id, tipo, minimo, maximo in sensores:

            self.sensor_manager.registrar_sensor(
                sensor_id,
                tipo,
                minimo,
                maximo
            )

    # =====================================================
    # EXECUTA CICLO
    # =====================================================

    def executar_ciclo(self):

        self.sensor_manager.coletar_dados()

        sensores = []

        for sensor in self.sensor_manager.sensores.values():

            leitura = sensor.ultima_leitura

            if leitura:

                sensores.append({

                    "sensor": leitura.sensor_id,
                    "tipo": leitura.tipo.value,
                    "valor": round(leitura.valor, 2)
                })

                self.storage_manager.armazenar_telemetria(
                    sensor_id=leitura.sensor_id,
                    tipo=leitura.tipo.value,
                    valor=leitura.valor
                )

        return sensores

# =========================================================
# INSTÂNCIA GLOBAL
# =========================================================

aurora = AuroraSystem()

# =========================================================
# ROTAS
# =========================================================

@app.route("/")
def dashboard():

    return render_template("dashboard.html")

@app.route("/api/status")
def status():

    sensores = aurora.executar_ciclo()

    solar = 0
    eolica = 0
    consumo = 0

    for s in sensores:

        if s["tipo"] == "geracao_solar":
            solar = s["valor"]

        if s["tipo"] == "geracao_eolica":
            eolica = s["valor"]

        if s["tipo"] == "consumo_energetico":
            consumo = s["valor"]

    return jsonify({

        "timestamp":
            datetime.now().strftime("%H:%M:%S"),

        "sensores": sensores,

        "solar": solar,

        "eolica": eolica,

        "consumo": consumo,

        "alertas":
            len(aurora.alert_manager.alertas),

        "registros":
            len(aurora.storage_manager.historico)
    })

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )