from dataclasses import dataclass
from datetime import datetime
from typing import List
import numpy as np

# =========================================================
# RICH TERMINAL UI
# =========================================================

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule
from rich.columns import Columns
from rich.progress import track
from rich.text import Text
from rich import box

console = Console()

# =========================================================
# UI HELPERS
# =========================================================

class UI:

    @staticmethod
    def titulo(texto):

        console.print()

        console.print(
            Panel.fit(
                Align.center(
                    f"[bold cyan]{texto}[/bold cyan]"
                ),
                border_style="cyan",
                padding=(1, 6)
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


# =========================================================
# MODELOS
# =========================================================

@dataclass
class RegistroEnergetico:

    timestamp: datetime

    geracao_solar: float

    geracao_eolica: float

    consumo: float


# =========================================================
# PREDICTION ENGINE
# =========================================================

class PredictionEngine:
    """
    Camada responsável por:
    - regressão linear;
    - previsão de geração;
    - simulação de cenários;
    - análise preditiva da colônia Aurora.
    """

    def __init__(self):

        # ==============================================
        # Histórico
        # ==============================================

        self.historico: List[
            RegistroEnergetico
        ] = []

        # ==============================================
        # Vetores NumPy
        # ==============================================

        self.vetor_tempo = np.array([])

        self.vetor_geracao_solar = np.array([])

        self.vetor_geracao_eolica = np.array([])

        self.vetor_consumo = np.array([])

        # ==============================================
        # Regressão Linear
        # ==============================================

        self.coeficiente_angular = 0.0

        self.coeficiente_linear = 0.0

        UI.titulo(
            "PREDICTION ENGINE INICIALIZADO"
        )

    # =====================================================
    # REGISTRO
    # =====================================================

    def adicionar_registro(
        self,
        geracao_solar: float,
        geracao_eolica: float,
        consumo: float
    ):

        UI.secao(
            "INGESTÃO ENERGÉTICA"
        )

        indice_tempo = len(
            self.vetor_tempo
        )

        registro = RegistroEnergetico(

            timestamp=datetime.now(),

            geracao_solar=geracao_solar,

            geracao_eolica=geracao_eolica,

            consumo=consumo
        )

        self.historico.append(registro)

        # ==============================================
        # Vetores
        # ==============================================

        self.vetor_tempo = np.append(
            self.vetor_tempo,
            indice_tempo
        )

        self.vetor_geracao_solar = np.append(
            self.vetor_geracao_solar,
            geracao_solar
        )

        self.vetor_geracao_eolica = np.append(
            self.vetor_geracao_eolica,
            geracao_eolica
        )

        self.vetor_consumo = np.append(
            self.vetor_consumo,
            consumo
        )

        # ==============================================
        # TABELA
        # ==============================================

        tabela = Table(
            title="Novo Registro Energético",
            box=box.ROUNDED
        )

        tabela.add_column(
            "Solar",
            style="yellow"
        )

        tabela.add_column(
            "Eólica",
            style="cyan"
        )

        tabela.add_column(
            "Consumo",
            style="red"
        )

        tabela.add_column(
            "Timestamp",
            style="green"
        )

        tabela.add_row(
            f"{geracao_solar:.2f}",
            f"{geracao_eolica:.2f}",
            f"{consumo:.2f}",
            registro.timestamp.strftime(
                "%H:%M:%S"
            )
        )

        console.print(tabela)

    # =====================================================
    # REGRESSÃO LINEAR
    # =====================================================

    def executar_regressao_linear(self):

        UI.titulo(
            "REGRESSÃO LINEAR"
        )

        if len(self.vetor_tempo) < 2:

            UI.alerta(
                "Dados insuficientes para regressão"
            )

            return

        # ==============================================
        # MODELO:
        # y = ax + b
        # ==============================================

        coeficientes = np.polyfit(
            self.vetor_tempo,
            self.vetor_geracao_solar,
            1
        )

        self.coeficiente_angular = (
            coeficientes[0]
        )

        self.coeficiente_linear = (
            coeficientes[1]
        )

        tabela = Table(
            title="Modelo Preditivo",
            box=box.DOUBLE_EDGE
        )

        tabela.add_column(
            "Parâmetro",
            style="cyan"
        )

        tabela.add_column(
            "Valor",
            style="green"
        )

        tabela.add_row(
            "Coeficiente Angular",
            f"{self.coeficiente_angular:.4f}"
        )

        tabela.add_row(
            "Coeficiente Linear",
            f"{self.coeficiente_linear:.4f}"
        )

        tabela.add_row(
            "Equação",
            (
                f"y = "
                f"{self.coeficiente_angular:.2f}x + "
                f"{self.coeficiente_linear:.2f}"
            )
        )

        console.print(tabela)

        # ==============================================
        # WIDGET MATEMÁTICO
        # ==============================================

        console.print(
            "\n[bold magenta]Equação Visual:[/bold magenta]"
        )

        print(
            ''
        )

    # =====================================================
    # PREVISÃO
    # =====================================================

    def prever_geracao(
        self,
        passos_futuros: int = 5
    ) -> List[float]:

        UI.titulo(
            "PREVISÃO ENERGÉTICA"
        )

        previsoes = []

        ultimo_indice = len(
            self.vetor_tempo
        )

        tabela = Table(
            title="Previsão de Geração Solar",
            box=box.HEAVY_EDGE,
            show_lines=True
        )

        tabela.add_column(
            "Horizonte",
            style="cyan"
        )

        tabela.add_column(
            "Geração Prevista",
            style="green"
        )

        tabela.add_column(
            "Status",
            justify="center"
        )

        for i in range(passos_futuros):

            x_futuro = (
                ultimo_indice + i
            )

            y_previsto = (
                self.coeficiente_angular
                * x_futuro
                + self.coeficiente_linear
            )

            previsoes.append(
                y_previsto
            )

            # ==========================================
            # STATUS
            # ==========================================

            if y_previsto < 300:

                status = (
                    "[red]CRÍTICO[/red]"
                )

            elif y_previsto < 600:

                status = (
                    "[yellow]ALERTA[/yellow]"
                )

            else:

                status = (
                    "[green]ESTÁVEL[/green]"
                )

            tabela.add_row(
                f"T+{i+1}",
                f"{y_previsto:.2f}",
                status
            )

        console.print(tabela)

        return previsoes

    # =====================================================
    # SIMULAÇÃO
    # =====================================================

    def simular_cenarios(self):

        UI.titulo(
            "SIMULAÇÃO DE CENÁRIOS"
        )

        if len(
            self.vetor_geracao_solar
        ) == 0:

            UI.alerta(
                "Sem dados disponíveis"
            )

            return

        media_solar = np.mean(
            self.vetor_geracao_solar
        )

        media_eolica = np.mean(
            self.vetor_geracao_eolica
        )

        media_consumo = np.mean(
            self.vetor_consumo
        )

        cenarios = {

            "NORMAL": {

                "solar": media_solar,

                "eolica": media_eolica,

                "consumo": media_consumo
            },

            "TEMPESTADE_DE_AREIA": {

                "solar": media_solar * 0.25,

                "eolica": media_eolica * 1.40,

                "consumo": media_consumo * 1.15
            },

            "FALHA_ENERGÉTICA": {

                "solar": media_solar * 0.40,

                "eolica": media_eolica * 0.50,

                "consumo": media_consumo * 1.30
            },

            "EXPANSÃO_DA_COLÔNIA": {

                "solar": media_solar * 1.50,

                "eolica": media_eolica * 1.60,

                "consumo": media_consumo * 1.80
            }
        }

        tabela = Table(
            title="Cenários Operacionais",
            box=box.DOUBLE,
            show_lines=True
        )

        tabela.add_column(
            "Cenário",
            style="cyan"
        )

        tabela.add_column(
            "Solar",
            style="yellow"
        )

        tabela.add_column(
            "Eólica",
            style="blue"
        )

        tabela.add_column(
            "Consumo",
            style="red"
        )

        tabela.add_column(
            "Saldo",
            style="green"
        )

        tabela.add_column(
            "Status",
            justify="center"
        )

        for nome, dados in cenarios.items():

            saldo = (
                dados["solar"]
                + dados["eolica"]
                - dados["consumo"]
            )

            # ==========================================
            # STATUS OPERACIONAL
            # ==========================================

            if saldo < 0:

                status = (
                    "[red]RISCO[/red]"
                )

            elif saldo < 300:

                status = (
                    "[yellow]ALERTA[/yellow]"
                )

            else:

                status = (
                    "[green]ESTÁVEL[/green]"
                )

            tabela.add_row(
                nome,
                f"{dados['solar']:.2f}",
                f"{dados['eolica']:.2f}",
                f"{dados['consumo']:.2f}",
                f"{saldo:.2f}",
                status
            )

        console.print(tabela)

    # =====================================================
    # ESTATÍSTICAS
    # =====================================================

    def exibir_estatisticas(self):

        UI.titulo(
            "ESTATÍSTICAS ENERGÉTICAS"
        )

        if len(
            self.vetor_geracao_solar
        ) == 0:

            UI.alerta(
                "Sem dados estatísticos"
            )

            return

        painel_1 = Panel.fit(

            (
                f"[bold yellow]"
                f"{np.mean(self.vetor_geracao_solar):.2f}"
                f"[/bold yellow]\n"
                f"Média Solar"
            ),

            border_style="yellow"

        )

        painel_2 = Panel.fit(

            (
                f"[bold cyan]"
                f"{np.mean(self.vetor_geracao_eolica):.2f}"
                f"[/bold cyan]\n"
                f"Média Eólica"
            ),

            border_style="cyan"

        )

        painel_3 = Panel.fit(

            (
                f"[bold red]"
                f"{np.mean(self.vetor_consumo):.2f}"
                f"[/bold red]\n"
                f"Média Consumo"
            ),

            border_style="red"

        )

        painel_4 = Panel.fit(

            (
                f"[bold magenta]"
                f"{np.std(self.vetor_geracao_solar):.2f}"
                f"[/bold magenta]\n"
                f"Desvio Solar"
            ),

            border_style="magenta"

        )

        console.print(
            Columns(
                [
                    painel_1,
                    painel_2,
                    painel_3,
                    painel_4
                ]
            )
        )

        UI.sucesso(
            "Análise estatística concluída"
        )


# =========================================================
# EXEMPLO DE UTILIZAÇÃO
# =========================================================

UI.titulo(
    "AURORA - PREDICTION ENGINE"
)

engine = PredictionEngine()

# =========================================================
# HISTÓRICO
# =========================================================

engine.adicionar_registro(
    geracao_solar=500,
    geracao_eolica=220,
    consumo=600
)

engine.adicionar_registro(
    geracao_solar=540,
    geracao_eolica=230,
    consumo=640
)

engine.adicionar_registro(
    geracao_solar=610,
    geracao_eolica=240,
    consumo=700
)

engine.adicionar_registro(
    geracao_solar=680,
    geracao_eolica=260,
    consumo=740
)

engine.adicionar_registro(
    geracao_solar=720,
    geracao_eolica=300,
    consumo=790
)

# =========================================================
# REGRESSÃO
# =========================================================

engine.executar_regressao_linear()

# =========================================================
# PREVISÃO
# =========================================================

engine.prever_geracao(
    passos_futuros=5
)

# =========================================================
# SIMULAÇÕES
# =========================================================

engine.simular_cenarios()

# =========================================================
# ESTATÍSTICAS
# =========================================================

engine.exibir_estatisticas()

UI.titulo(
    "ANÁLISE PREDITIVA FINALIZADA"
)