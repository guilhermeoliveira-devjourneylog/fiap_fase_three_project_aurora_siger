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
import time

# =========================================================
# RICH TERMINAL UI
# =========================================================

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.columns import Columns
from rich.rule import Rule
from rich import box

console = Console()

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
# UI HELPERS
# =========================================================

class UI:
    """
    Camada utilitária de interface Rich.

    Responsável por:
    - títulos;
    - seções;
    - alertas;
    - mensagens informativas;
    - painéis operacionais.
    """

    @staticmethod
    def titulo(texto):

        console.print()

        console.print(
            Panel.fit(
                Align.center(
                    f"[bold cyan]{texto}[/bold cyan]"
                ),
                border_style="bright_blue",
                padding=(1, 8)
            )
        )

    @staticmethod
    def secao(texto):

        console.print(
            Rule(
                f"[bold yellow]{texto}[/bold yellow]",
                style="yellow"
            )
        )

    @staticmethod
    def sucesso(texto):

        console.print(
            f"[bold green]✔ {texto}[/bold green]"
        )

    @staticmethod
    def alerta(texto):

        console.print(
            f"[bold red]⚠ {texto}[/bold red]"
        )

    @staticmethod
    def info(texto):

        console.print(
            f"[bold blue]ℹ {texto}[/bold blue]"
        )

    @staticmethod
    def painel_status(
        titulo,
        valor,
        cor
    ):

        return Panel.fit(

            f"[bold {cor}]{valor}[/bold {cor}]",

            title=titulo,

            border_style=cor,

            padding=(1, 3)
        )


# =========================================================
# SISTEMA CENTRAL
# =========================================================

class AuroraSystem:
    """
    Sistema central da Colônia Aurora.

    Responsável pela orquestração completa das camadas:
    - sensoriamento;
    - armazenamento;
    - processamento;
    - análise preditiva;
    - automação;
    - gerenciamento de alertas.

    Fluxo operacional:

    Sensores
        ↓
    Storage
        ↓
    Processing
        ↓
    Prediction
        ↓
    Decision
        ↓
    Alert System
    """

    def __init__(self):

        # =================================================
        # CAMADAS
        # =================================================

        self.sensor_manager = SensorManager()

        self.storage_manager = StorageManager()

        self.processing_engine = ProcessingEngine()

        self.prediction_engine = PredictionEngine()

        self.decision_engine = DecisionEngine()

        self.alert_manager = AlertManager()

        # =================================================
        # CONTROLE ANALÍTICO
        # =================================================

        self.ultimo_indice_processado = 0

        # =================================================
        # CONFIGURAÇÃO
        # =================================================

        self._registrar_sensores()

        UI.titulo(
            "SISTEMA AURORA INICIALIZADO"
        )

    # =====================================================
    # REGISTRO DOS SENSORES
    # =====================================================

    def _registrar_sensores(self):
        """
        Registra todos os sensores operacionais da colônia.
        """

        sensores = [

            (
                "TEMP-INT-01",
                TipoSensor.TEMPERATURA_INTERNA,
                18,
                32
            ),

            (
                "TEMP-EXT-01",
                TipoSensor.TEMPERATURA_EXTERNA,
                -120,
                50
            ),

            (
                "VENTO-01",
                TipoSensor.VELOCIDADE_VENTO,
                0,
                180
            ),

            (
                "SOLAR-01",
                TipoSensor.GERACAO_SOLAR,
                0,
                1200
            ),

            (
                "EOLICA-01",
                TipoSensor.GERACAO_EOLICA,
                0,
                900
            ),

            (
                "ENERGIA-01",
                TipoSensor.CONSUMO_ENERGETICO,
                100,
                4000
            ),

            (
                "ESTRUTURA-01",
                TipoSensor.INTEGRIDADE_ESTRUTURAL,
                70,
                100
            )

        ]

        tabela = Table(
            title="Sensores Registrados",
            box=box.ROUNDED,
            show_lines=True
        )

        tabela.add_column(
            "Sensor",
            style="cyan"
        )

        tabela.add_column(
            "Tipo",
            style="magenta"
        )

        tabela.add_column(
            "Faixa",
            style="green"
        )

        for (
            sensor_id,
            tipo,
            minimo,
            maximo
        ) in sensores:

            self.sensor_manager.registrar_sensor(
                sensor_id,
                tipo,
                minimo,
                maximo
            )

            tabela.add_row(
                sensor_id,
                tipo.value,
                f"{minimo} → {maximo}"
            )

        console.print(tabela)

    # =====================================================
    # CICLO OPERACIONAL
    # =====================================================

    def executar_ciclo(
        self,
        numero_ciclo: int
    ):
        """
        Executa um ciclo operacional completo do sistema.
        """

        UI.titulo(
            f"CICLO OPERACIONAL {numero_ciclo}"
        )

        # =================================================
        # STATUS GLOBAL
        # =================================================

        paineis = [

            UI.painel_status(
                "COLÔNIA",
                "ONLINE",
                "green"
            ),

            UI.painel_status(
                "ENERGIA",
                "ESTÁVEL",
                "cyan"
            ),

            UI.painel_status(
                "ESTRUTURA",
                "SEGURA",
                "yellow"
            ),

            UI.painel_status(
                "MODELO IA",
                (
                    "TREINADO"
                    if self.prediction_engine.modelo_treinado
                    else "AGUARDANDO"
                ),
                (
                    "green"
                    if self.prediction_engine.modelo_treinado
                    else "red"
                )
            ),

            UI.painel_status(
                "ALERTAS",
                str(
                    len(
                        self.alert_manager.alertas
                    )
                ),
                "red"
            )

        ]

        console.print(
            Columns(paineis)
        )

        # =================================================
        # ETAPA 1 • COLETA
        # =================================================

        UI.secao(
            "1 • COLETA SENSORIAL"
        )

        self.sensor_manager.coletar_dados()

        # =================================================
        # ETAPA 2 • VALIDAÇÃO
        # =================================================

        UI.secao(
            "2 • VALIDAÇÃO OPERACIONAL"
        )

        self.sensor_manager.validar_dados()

        # =================================================
        # ETAPA 3 • STORAGE
        # =================================================

        UI.secao(
            "3 • ARMAZENAMENTO"
        )

        tabela_storage = Table(
            title="Telemetria Armazenada",
            box=box.SIMPLE_HEAVY
        )

        tabela_storage.add_column(
            "Sensor",
            style="cyan"
        )

        tabela_storage.add_column(
            "Tipo",
            style="yellow"
        )

        tabela_storage.add_column(
            "Valor",
            justify="right",
            style="green"
        )

        for sensor in self.sensor_manager.sensores.values():

            leitura = sensor.ultima_leitura

            if leitura is None:
                continue

            self.storage_manager.armazenar_telemetria(
                sensor_id=leitura.sensor_id,
                tipo=leitura.tipo.value,
                valor=leitura.valor
            )

            tabela_storage.add_row(
                leitura.sensor_id,
                leitura.tipo.value,
                f"{leitura.valor:.2f}"
            )

        console.print(tabela_storage)

        # =================================================
        # ETAPA 4 • PROCESSAMENTO
        # =================================================

        UI.secao(
            "4 • PROCESSAMENTO ANALÍTICO"
        )

        novos_registros = (
            self.storage_manager.historico[
                self.ultimo_indice_processado:
            ]
        )

        for registro in novos_registros:

            self.processing_engine.adicionar_registro(
                sensor_id=registro.sensor_id,
                tipo=registro.tipo,
                valor=registro.valor
            )

        self.ultimo_indice_processado = len(
            self.storage_manager.historico
        )

        self.processing_engine.processar_estatisticas()

        self.processing_engine.atualizar_estados()

        # =================================================
        # ETAPA 5 • PREDICTION ENGINE
        # =================================================

        UI.secao(
            "5 • ANÁLISE PREDITIVA"
        )

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

        previsoes = []

        # =============================================
        # TREINAMENTO CONDICIONAL
        # =============================================

        if len(
            self.prediction_engine.historico
        ) >= 3:

            self.prediction_engine.executar_regressao_linear()

            self.prediction_engine.analisar_residuos()

            previsoes = (
                self.prediction_engine.prever_geracao(
                    passos_futuros=3
                )
            )

            # =========================================
            # ALERTAS PREDITIVOS
            # =========================================

            for previsao in previsoes:

                if previsao < 300:

                    alerta = (
                        "Previsão crítica de "
                        "geração solar futura"
                    )

                    alerta_obj = (
                        self.alert_manager.gerar_alerta(
                            tipo=TipoAlerta.ENERGETICO,
                            severidade=Severidade.CRITICA,
                            mensagem=alerta
                        )
                    )

                    self.alert_manager.notificar_operador(
                        alerta_obj
                    )

        else:

            UI.alerta(
                "Histórico insuficiente "
                "para análise preditiva"
            )

        # =============================================
        # PROJEÇÕES
        # =============================================

        if previsoes:

            tabela_previsao = Table(
                title="Projeção Energética",
                box=box.DOUBLE_EDGE
            )

            tabela_previsao.add_column(
                "Horizonte",
                style="cyan"
            )

            tabela_previsao.add_column(
                "Energia Prevista",
                style="green"
            )

            for i, valor in enumerate(
                previsoes,
                start=1
            ):

                tabela_previsao.add_row(
                    f"T+{i}",
                    f"{valor:.2f}"
                )

            console.print(
                tabela_previsao
            )

        self.prediction_engine.simular_cenarios()

        # =================================================
        # ETAPA 6 • DECISION ENGINE
        # =================================================

        UI.secao(
            "6 • MOTOR DE DECISÃO"
        )

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

            valor=random.uniform(
                60,
                120
            ),

            limite=100,

            timestamp=datetime.now()
        )

        self.decision_engine.executar_automacao(
            evento_estrutura
        )

        self.decision_engine.alterar_estado()

        # =================================================
        # ETAPA 7 • ALERTAS
        # =================================================

        UI.secao(
            "7 • SISTEMA DE ALERTAS"
        )

        self._processar_alertas()

        # =================================================
        # FINALIZAÇÃO
        # =================================================

        console.print()

        console.print(
            Panel.fit(

                "[bold green]"
                "CICLO OPERACIONAL FINALIZADO"
                "[/bold green]",

                border_style="green",

                padding=(1, 5)
            )
        )

    # =====================================================
    # ALERTAS
    # =====================================================

    def _processar_alertas(self):
        """
        Processa alertas operacionais e preditivos.
        """

        tabela_alertas = Table(
            title="Alertas Operacionais",
            box=box.HEAVY,
            show_lines=True
        )

        tabela_alertas.add_column(
            "Tipo",
            style="red"
        )

        tabela_alertas.add_column(
            "Severidade",
            style="yellow"
        )

        tabela_alertas.add_column(
            "Mensagem",
            style="white"
        )

        for alerta in self.sensor_manager.alertas:

            alerta_obj = self.alert_manager.gerar_alerta(

                tipo=TipoAlerta.OPERACIONAL,

                severidade=Severidade.MEDIA,

                mensagem=alerta
            )

            self.alert_manager.notificar_operador(
                alerta_obj
            )

            tabela_alertas.add_row(
                "SENSOR",
                "MÉDIA",
                alerta
            )

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

            tabela_alertas.add_row(
                "DECISION",
                severidade.name,
                str(alerta)
            )

        console.print(tabela_alertas)

    # =====================================================
    # AUXILIAR
    # =====================================================

    def _obter_valor_sensor(
        self,
        tipo_sensor: str
    ) -> float:
        """
        Obtém o valor mais recente de um sensor.
        """

        for sensor in self.sensor_manager.sensores.values():

            leitura = sensor.ultima_leitura

            if leitura and leitura.tipo.value == tipo_sensor:

                return leitura.valor

        return 0.0

    # =====================================================
    # DASHBOARD
    # =====================================================

    def exibir_dashboard(self):
        """
        Exibe o dashboard central da colônia.
        """

        UI.titulo(
            "DASHBOARD CENTRAL DA COLÔNIA"
        )

        dashboard = Columns([

            UI.painel_status(
                "SENSORES",
                str(
                    len(
                        self.sensor_manager.sensores
                    )
                ),
                "cyan"
            ),

            UI.painel_status(
                "REGISTROS",
                str(
                    len(
                        self.storage_manager.historico
                    )
                ),
                "green"
            ),

            UI.painel_status(
                "ALERTAS",
                str(
                    len(
                        self.alert_manager.alertas
                    )
                ),
                "red"
            ),

            UI.painel_status(
                "MODELO IA",
                (
                    "TREINADO"
                    if self.prediction_engine.modelo_treinado
                    else "AGUARDANDO"
                ),
                (
                    "green"
                    if self.prediction_engine.modelo_treinado
                    else "red"
                )
            )

        ])

        console.print(dashboard)

        UI.secao(
            "MONITORAMENTO DE SENSORES"
        )

        self.sensor_manager.monitorar_integridade()

        UI.secao(
            "MATRIZ ENERGÉTICA"
        )

        self.storage_manager.exibir_matriz_energia()

        UI.secao(
            "CENTRAL DE ALERTAS"
        )

        self.alert_manager.exibir_dashboard()

        UI.secao(
            "ESTATÍSTICAS GLOBAIS"
        )

        self.processing_engine.processar_estatisticas()

        UI.secao(
            "DIAGNÓSTICO PREDITIVO"
        )

        self.prediction_engine.exibir_estatisticas()

        console.print()

        console.print(
            Panel.fit(

                "[bold bright_green]"
                "DASHBOARD FINALIZADO"
                "[/bold bright_green]",

                border_style="bright_green",

                padding=(1, 6)
            )
        )


# =========================================================
# EXECUÇÃO PRINCIPAL
# =========================================================

if __name__ == "__main__":

    console.clear()

    UI.titulo(
        "AURORA SIGER"
    )

    sistema = AuroraSystem()

    # =====================================================
    # CICLOS OPERACIONAIS
    # =====================================================

    for i in range(5):

        sistema.executar_ciclo(
            numero_ciclo=i + 1
        )

        # =============================================
        # DELTA TEMPORAL REALISTA
        # =============================================

        time.sleep(1)

    # =====================================================
    # DASHBOARD FINAL
    # =====================================================

    sistema.exibir_dashboard()

    # =====================================================
    # FINALIZAÇÃO
    # =====================================================

    console.print()

    console.print(
        Panel.fit(

            "[bold cyan]"
            "Pressione ENTER para encerrar "
            "o Sistema Aurora"
            "[/bold cyan]",

            border_style="cyan"
        )
    )

    input()