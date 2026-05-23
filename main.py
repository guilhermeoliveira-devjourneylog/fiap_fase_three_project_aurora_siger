# =========================================================
# MAIN - SISTEMA AURORA
# =========================================================
# Integração completa das camadas:
#
# - SensorManager
# - StorageManager
# - ProcessingEngine
# - PredictionEngine
# - DecisionEngine
# - AlertManager
#
# =========================================================

from datetime import datetime
import random

# =========================================================
# IMPORTS DAS CAMADAS
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
# SISTEMA CENTRAL
# =========================================================

class AuroraSystem:

    def __init__(self):

        # ==============================================
        # CAMADAS
        # ==============================================

        self.sensor_manager = SensorManager()

        self.storage_manager = StorageManager()

        self.processing_engine = ProcessingEngine()

        self.prediction_engine = PredictionEngine()

        self.decision_engine = DecisionEngine()

        self.alert_manager = AlertManager()

        # ==============================================
        # CONFIGURAÇÃO INICIAL
        # ==============================================

        self._registrar_sensores()

    # =====================================================
    # REGISTRO DOS SENSORES
    # =====================================================

    def _registrar_sensores(self):

        self.sensor_manager.registrar_sensor(
            "TEMP-INT-01",
            TipoSensor.TEMPERATURA_INTERNA,
            18,
            32
        )

        self.sensor_manager.registrar_sensor(
            "TEMP-EXT-01",
            TipoSensor.TEMPERATURA_EXTERNA,
            -120,
            50
        )

        self.sensor_manager.registrar_sensor(
            "VENTO-01",
            TipoSensor.VELOCIDADE_VENTO,
            0,
            180
        )

        self.sensor_manager.registrar_sensor(
            "SOLAR-01",
            TipoSensor.GERACAO_SOLAR,
            0,
            1200
        )

        self.sensor_manager.registrar_sensor(
            "EOLICA-01",
            TipoSensor.GERACAO_EOLICA,
            0,
            900
        )

        self.sensor_manager.registrar_sensor(
            "ENERGIA-01",
            TipoSensor.CONSUMO_ENERGETICO,
            100,
            4000
        )

        self.sensor_manager.registrar_sensor(
            "ESTRUTURA-01",
            TipoSensor.INTEGRIDADE_ESTRUTURAL,
            70,
            100
        )

    # =====================================================
    # CICLO OPERACIONAL
    # =====================================================

    def executar_ciclo(self):

        print("\n================================================")
        print("INICIANDO CICLO OPERACIONAL DA COLÔNIA")
        print("================================================\n")

        # ==============================================
        # 1. COLETA
        # ==============================================

        self.sensor_manager.coletar_dados()

        # ==============================================
        # 2. VALIDAÇÃO
        # ==============================================

        self.sensor_manager.validar_dados()

        # ==============================================
        # 3. ARMAZENAMENTO
        # ==============================================

        for sensor in self.sensor_manager.sensores.values():

            leitura = sensor.ultima_leitura

            if leitura is None:
                continue

            self.storage_manager.armazenar_telemetria(
                sensor_id=leitura.sensor_id,
                tipo=leitura.tipo.value,
                valor=leitura.valor
            )

        # ==============================================
        # 4. PROCESSAMENTO
        # ==============================================

        for registro in self.storage_manager.historico:

            self.processing_engine.adicionar_registro(
                sensor_id=registro.sensor_id,
                tipo=registro.tipo,
                valor=registro.valor
            )

        self.processing_engine.processar_estatisticas()

        self.processing_engine.atualizar_estados()

        # ==============================================
        # 5. PREDIÇÃO
        # ==============================================

        solar = self._obter_valor_sensor(
            "geracao_solar"
        )

        eolica = self._obter_valor_sensor(
            "geracao_eolica"
        )

        consumo = self._obter_valor_sensor(
            "consumo_energetico"
        )

        self.prediction_engine.adicionar_registro(
            geracao_solar=solar,
            geracao_eolica=eolica,
            consumo=consumo
        )

        self.prediction_engine.executar_regressao_linear()

        self.prediction_engine.prever_geracao(
            passos_futuros=3
        )

        self.prediction_engine.simular_cenarios()

        # ==============================================
        # 6. MOTOR DE DECISÃO
        # ==============================================

        evento_energia = EventoOperacional(
            subsistema="energia",
            valor=consumo,
            limite=3500,
            timestamp=datetime.now()
        )

        self.decision_engine.executar_automacao(
            evento_energia
        )

        evento_estrutura = EventoOperacional(
            subsistema="estrutura",
            valor=random.uniform(60, 120),
            limite=100,
            timestamp=datetime.now()
        )

        self.decision_engine.executar_automacao(
            evento_estrutura
        )

        self.decision_engine.alterar_estado()

        # ==============================================
        # 7. ALERTAS
        # ==============================================

        self._processar_alertas()

        print("\n================================================")
        print("CICLO FINALIZADO")
        print("================================================\n")

    # =====================================================
    # ALERTAS
    # =====================================================

    def _processar_alertas(self):

        # ==============================================
        # ALERTAS DOS SENSORES
        # ==============================================

        for alerta in self.sensor_manager.alertas:

            alerta_obj = self.alert_manager.gerar_alerta(
                tipo=TipoAlerta.OPERACIONAL,
                severidade=Severidade.MEDIA,
                mensagem=alerta
            )

            self.alert_manager.notificar_operador(
                alerta_obj
            )

        # ==============================================
        # ALERTAS DECISION ENGINE
        # ==============================================

        for alerta in self.decision_engine.alertas:

            severidade = (
                Severidade.CRITICA
                if "CRÍTICO" in alerta
                or "EMERGÊNCIA" in alerta
                else Severidade.ALTA
            )

            alerta_obj = self.alert_manager.gerar_alerta(
                tipo=TipoAlerta.CRITICO,
                severidade=severidade,
                mensagem=alerta
            )

            self.alert_manager.notificar_operador(
                alerta_obj
            )

    # =====================================================
    # AUXILIAR
    # =====================================================

    def _obter_valor_sensor(
        self,
        tipo_sensor: str
    ) -> float:

        for sensor in self.sensor_manager.sensores.values():

            leitura = sensor.ultima_leitura

            if leitura and leitura.tipo.value == tipo_sensor:

                return leitura.valor

        return 0.0

    # =====================================================
    # DASHBOARD
    # =====================================================

    def exibir_dashboard(self):

        print("\n================================================")
        print("DASHBOARD DA COLÔNIA AURORA")
        print("================================================\n")

        # ==============================================
        # SENSORES
        # ==============================================

        self.sensor_manager.monitorar_integridade()

        # ==============================================
        # MATRIZ ENERGÉTICA
        # ==============================================

        self.storage_manager.exibir_matriz_energia()

        # ==============================================
        # ALERTAS
        # ==============================================

        self.alert_manager.exibir_dashboard()

        # ==============================================
        # ESTATÍSTICAS
        # ==============================================

        self.processing_engine.processar_estatisticas()

        self.prediction_engine.exibir_estatisticas()


# =========================================================
# EXECUÇÃO PRINCIPAL
# =========================================================

if __name__ == "__main__":

    sistema = AuroraSystem()

    # ==============================================
    # EXECUTA CICLOS
    # ==============================================

    for i in range(3):

        print(f"\n########## CICLO {i+1} ##########\n")

        sistema.executar_ciclo()

    # ==============================================
    # DASHBOARD FINAL
    # ==============================================

    sistema.exibir_dashboard()