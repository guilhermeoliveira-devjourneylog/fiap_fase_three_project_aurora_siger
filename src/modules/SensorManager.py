from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
import random


# =========================================================
# ENUMS
# =========================================================

class StatusSensor(Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    ALERTA = "ALERTA"
    FALHA = "FALHA"


class TipoSensor(Enum):
    TEMPERATURA_INTERNA = "temperatura_interna"
    TEMPERATURA_EXTERNA = "temperatura_externa"
    VELOCIDADE_VENTO = "velocidade_vento"
    GERACAO_SOLAR = "geracao_solar"
    GERACAO_EOLICA = "geracao_eolica"
    CONSUMO_ENERGETICO = "consumo_energetico"
    ESTADO_MODULOS = "estado_modulos"
    INTEGRIDADE_ESTRUTURAL = "integridade_estrutural"


# =========================================================
# MODELO DE DADOS
# =========================================================

@dataclass
class LeituraSensor:
    sensor_id: str
    tipo: TipoSensor
    valor: float
    timestamp: datetime


# =========================================================
# CLASSE SENSOR
# =========================================================

class Sensor:

    def __init__(
        self,
        sensor_id: str,
        tipo: TipoSensor,
        limite_min: float,
        limite_max: float
    ):

        self.sensor_id = sensor_id
        self.tipo = tipo
        self.limite_min = limite_min
        self.limite_max = limite_max

        self.status = StatusSensor.ONLINE
        self.ultima_leitura: Optional[LeituraSensor] = None

    def gerar_leitura(self) -> float:
        """
        Simulação de leitura baseada no tipo de sensor.
        """

        faixa = {
            TipoSensor.TEMPERATURA_INTERNA: (18, 32),
            TipoSensor.TEMPERATURA_EXTERNA: (-80, 40),
            TipoSensor.VELOCIDADE_VENTO: (0, 180),
            TipoSensor.GERACAO_SOLAR: (0, 1000),
            TipoSensor.GERACAO_EOLICA: (0, 700),
            TipoSensor.CONSUMO_ENERGETICO: (50, 1200),
            TipoSensor.ESTADO_MODULOS: (0, 100),
            TipoSensor.INTEGRIDADE_ESTRUTURAL: (0, 100)
        }

        minimo, maximo = faixa[self.tipo]

        return round(random.uniform(minimo, maximo), 2)


# =========================================================
# SENSOR MANAGER
# =========================================================

class SensorManager:

    def __init__(self):

        self.sensores: Dict[str, Sensor] = {}
        self.historico: List[LeituraSensor] = []
        self.alertas: List[str] = []

    # =====================================================
    # REGISTRO
    # =====================================================

    def registrar_sensor(
        self,
        sensor_id: str,
        tipo: TipoSensor,
        limite_min: float,
        limite_max: float
    ):

        sensor = Sensor(
            sensor_id,
            tipo,
            limite_min,
            limite_max
        )

        self.sensores[sensor_id] = sensor

        print(f"[INFO] Sensor registrado: {sensor_id}")

    # =====================================================
    # COLETA
    # =====================================================

    def coletar_dados(self):

        print("\n[COLETA DE DADOS]\n")

        for sensor in self.sensores.values():

            valor = sensor.gerar_leitura()

            leitura = LeituraSensor(
                sensor_id=sensor.sensor_id,
                tipo=sensor.tipo,
                valor=valor,
                timestamp=datetime.now()
            )

            sensor.ultima_leitura = leitura

            self.historico.append(leitura)

            print(
                f"{sensor.sensor_id} | "
                f"{sensor.tipo.value} | "
                f"{valor}"
            )

    # =====================================================
    # VALIDAÇÃO
    # =====================================================

    def validar_dados(self):

        print("\n[VALIDAÇÃO DOS DADOS]\n")

        for sensor in self.sensores.values():

            leitura = sensor.ultima_leitura

            if leitura is None:
                continue

            valor = leitura.valor

            if sensor.limite_min <= valor <= sensor.limite_max:

                sensor.status = StatusSensor.ONLINE

                print(
                    f"[OK] {sensor.sensor_id} "
                    f"-> {valor}"
                )

            else:

                sensor.status = StatusSensor.ALERTA

                alerta = (
                    f"[ALERTA] {sensor.sensor_id} "
                    f"fora da faixa operacional "
                    f"({valor})"
                )

                self.alertas.append(alerta)

                print(alerta)

    # =====================================================
    # MONITORAMENTO
    # =====================================================

    def monitorar_integridade(self):

        print("\n[MONITORAMENTO DA INTEGRIDADE]\n")

        for sensor in self.sensores.values():

            leitura = sensor.ultima_leitura

            if leitura is None:

                sensor.status = StatusSensor.OFFLINE

            print(
                f"Sensor: {sensor.sensor_id}\n"
                f"Tipo: {sensor.tipo.value}\n"
                f"Status: {sensor.status.value}\n"
                f"Último valor: "
                f"{leitura.valor if leitura else 'N/A'}\n"
            )

    # =====================================================
    # ALERTAS
    # =====================================================

    def exibir_alertas(self):

        print("\n[ALERTAS DO SISTEMA]\n")

        if not self.alertas:
            print("Nenhum alerta ativo.")
            return

        for alerta in self.alertas:
            print(alerta)


# =========================================================
# INICIALIZAÇÃO DA CAMADA DE SENSORES
# =========================================================

sensor_manager = SensorManager()

# Temperatura interna
sensor_manager.registrar_sensor(
    "TEMP-INT-01",
    TipoSensor.TEMPERATURA_INTERNA,
    18,
    30
)

# Temperatura externa
sensor_manager.registrar_sensor(
    "TEMP-EXT-01",
    TipoSensor.TEMPERATURA_EXTERNA,
    -100,
    50
)

# Velocidade do vento
sensor_manager.registrar_sensor(
    "VENTO-01",
    TipoSensor.VELOCIDADE_VENTO,
    0,
    150
)

# Geração solar
sensor_manager.registrar_sensor(
    "SOLAR-01",
    TipoSensor.GERACAO_SOLAR,
    0,
    1000
)

# Geração eólica
sensor_manager.registrar_sensor(
    "EOLICA-01",
    TipoSensor.GERACAO_EOLICA,
    0,
    700
)

# Consumo energético
sensor_manager.registrar_sensor(
    "ENERGIA-01",
    TipoSensor.CONSUMO_ENERGETICO,
    100,
    1000
)

# Estado dos módulos
sensor_manager.registrar_sensor(
    "MODULO-01",
    TipoSensor.ESTADO_MODULOS,
    70,
    100
)

# Integridade estrutural
sensor_manager.registrar_sensor(
    "ESTRUTURA-01",
    TipoSensor.INTEGRIDADE_ESTRUTURAL,
    80,
    100
)

# =========================================================
# EXECUÇÃO
# =========================================================

sensor_manager.coletar_dados()

sensor_manager.validar_dados()

sensor_manager.monitorar_integridade()

sensor_manager.exibir_alertas()