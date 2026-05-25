from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

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
# MODELO DE DADOS
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
    Sistema responsável por:

    - ingestão energética;
    - regressão linear;
    - previsão operacional;
    - análise estatística;
    - análise de resíduos;
    - simulação de cenários.
    """

    def __init__(self):

        # =================================================
        # HISTÓRICO
        # =================================================

        self.historico: List[
            RegistroEnergetico
        ] = []

        # =================================================
        # LISTAS TEMPORÁRIAS
        # =================================================

        self.tempos = []

        self.geracao_solar = []

        self.geracao_eolica = []

        self.consumo = []

        # =================================================
        # MODELO
        # =================================================

        self.coeficiente_angular = 0.0

        self.coeficiente_linear = 0.0

        self.r2 = 0.0

        self.residuos = np.array([])

        self.y_pred = np.array([])

        self.modelo_treinado = False

        UI.titulo(
            "PREDICTION ENGINE INICIALIZADO"
        )

    # =====================================================
    # INGESTÃO
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

        timestamp = datetime.now()

        registro = RegistroEnergetico(

            timestamp=timestamp,

            geracao_solar=geracao_solar,

            geracao_eolica=geracao_eolica,

            consumo=consumo
        )

        self.historico.append(
            registro
        )

        # =================================================
        # TEMPO RELATIVO EM SEGUNDOS
        # =================================================

        if len(self.historico) == 1:

            tempo_relativo = 0

        else:

            tempo_relativo = (
                timestamp
                - self.historico[0].timestamp
            ).total_seconds()

        # =================================================
        # ARMAZENAMENTO
        # =================================================

        self.tempos.append(
            tempo_relativo
        )

        self.geracao_solar.append(
            geracao_solar
        )

        self.geracao_eolica.append(
            geracao_eolica
        )

        self.consumo.append(
            consumo
        )

        # =================================================
        # TABELA
        # =================================================

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
            "Tempo",
            style="green"
        )

        tabela.add_row(
            f"{geracao_solar:.2f}",
            f"{geracao_eolica:.2f}",
            f"{consumo:.2f}",
            f"{tempo_relativo:.2f}s"
        )

        console.print(tabela)

    # =====================================================
    # REGRESSÃO LINEAR
    # =====================================================

    def executar_regressao_linear(self):

        UI.titulo(
            "REGRESSÃO LINEAR"
        )

        if len(self.tempos) < 2:

            UI.alerta(
                "Dados insuficientes"
            )

            return

        # =================================================
        # ARRAYS NUMPY
        # =================================================

        x = np.array(
            self.tempos
        )

        y = np.array(
            self.geracao_solar
        )

        # =================================================
        # REGRESSÃO
        # =================================================

        coeficientes = np.polyfit(
            x,
            y,
            1
        )

        self.coeficiente_angular = (
            coeficientes[0]
        )

        self.coeficiente_linear = (
            coeficientes[1]
        )

        # =================================================
        # PREVISÕES
        # =================================================

        self.y_pred = (

            self.coeficiente_angular * x
            + self.coeficiente_linear

        )

        # =================================================
        # RESÍDUOS
        # =================================================

        self.residuos = (
            y - self.y_pred
        )

        # =================================================
        # R²
        # =================================================

        ss_res = np.sum(
            self.residuos ** 2
        )

        ss_tot = np.sum(
            (y - np.mean(y)) ** 2
        )

        self.r2 = (
            1 - (ss_res / ss_tot)
        )

        self.modelo_treinado = True

        # =================================================
        # TABELA
        # =================================================

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
            "R²",
            f"{self.r2:.4f}"
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

        UI.sucesso(
            "Modelo treinado"
        )

    # =====================================================
    # ANÁLISE DE RESÍDUOS
    # =====================================================

    def analisar_residuos(self):

        UI.titulo(
            "ANÁLISE DE RESÍDUOS"
        )

        if not self.modelo_treinado:

            UI.alerta(
                "Modelo ainda não treinado"
            )

            return

        tabela = Table(
            title="Resíduos do Modelo",
            box=box.HEAVY
        )

        tabela.add_column(
            "Índice",
            style="cyan"
        )

        tabela.add_column(
            "Real",
            style="yellow"
        )

        tabela.add_column(
            "Previsto",
            style="green"
        )

        tabela.add_column(
            "Resíduo",
            style="red"
        )

        for i in range(
            len(self.geracao_solar)
        ):

            tabela.add_row(
                str(i),

                f"{self.geracao_solar[i]:.2f}",

                f"{self.y_pred[i]:.2f}",

                f"{self.residuos[i]:.2f}"
            )

        console.print(tabela)

        media_residuo = np.mean(
            self.residuos
        )

        desvio_residuo = np.std(
            self.residuos
        )

        painel_1 = Panel.fit(

            (
                f"[bold red]"
                f"{media_residuo:.4f}"
                f"[/bold red]\n"
                f"Média dos Resíduos"
            ),

            border_style="red"

        )

        painel_2 = Panel.fit(

            (
                f"[bold magenta]"
                f"{desvio_residuo:.4f}"
                f"[/bold magenta]\n"
                f"Desvio Residual"
            ),

            border_style="magenta"

        )

        console.print(
            Columns(
                [
                    painel_1,
                    painel_2
                ]
            )
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

        if not self.modelo_treinado:

            UI.alerta(
                "Modelo ainda não treinado"
            )

            return []

        previsoes = []

        ultimo_tempo = (
            self.tempos[-1]
        )

        tabela = Table(
            title="Previsão Solar",
            box=box.HEAVY_EDGE,
            show_lines=True
        )

        tabela.add_column(
            "Horizonte",
            style="cyan"
        )

        tabela.add_column(
            "Previsão",
            style="green"
        )

        tabela.add_column(
            "Status",
            justify="center"
        )

        # =============================================
        # PASSO TEMPORAL MÉDIO
        # =============================================

        if len(self.tempos) > 1:

            delta = np.mean(
                np.diff(self.tempos)
            )

        else:

            delta = 1

        for i in range(
            passos_futuros
        ):

            tempo_futuro = (
                ultimo_tempo
                + delta * (i + 1)
            )

            y_previsto = (

                self.coeficiente_angular
                * tempo_futuro
                + self.coeficiente_linear

            )

            previsoes.append(
                y_previsto
            )

            # =========================================
            # STATUS
            # =========================================

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
    # SIMULAÇÃO DE CENÁRIOS
    # =====================================================

    def simular_cenarios(self):

        UI.titulo(
            "SIMULAÇÃO DE CENÁRIOS"
        )

        if len(self.geracao_solar) == 0:

            UI.alerta(
                "Sem dados disponíveis"
            )

            return

        media_solar = np.mean(
            self.geracao_solar
        )

        media_eolica = np.mean(
            self.geracao_eolica
        )

        media_consumo = np.mean(
            self.consumo
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
            "ESTATÍSTICAS"
        )

        if len(self.geracao_solar) == 0:

            UI.alerta(
                "Sem dados"
            )

            return

        painel_1 = Panel.fit(

            (
                f"[bold yellow]"
                f"{np.mean(self.geracao_solar):.2f}"
                f"[/bold yellow]\n"
                f"Média Solar"
            ),

            border_style="yellow"

        )

        painel_2 = Panel.fit(

            (
                f"[bold cyan]"
                f"{np.mean(self.geracao_eolica):.2f}"
                f"[/bold cyan]\n"
                f"Média Eólica"
            ),

            border_style="cyan"

        )

        painel_3 = Panel.fit(

            (
                f"[bold red]"
                f"{np.mean(self.consumo):.2f}"
                f"[/bold red]\n"
                f"Média Consumo"
            ),

            border_style="red"

        )

        painel_4 = Panel.fit(

            (
                f"[bold magenta]"
                f"{self.r2:.4f}"
                f"[/bold magenta]\n"
                f"R² do Modelo"
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
            "Análise concluída"
        )


# =========================================================
# EXEMPLO DE UTILIZAÇÃO
# =========================================================

UI.titulo(
    "AURORA - PREDICTION ENGINE"
)

engine = PredictionEngine()

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
# TREINAMENTO
# =========================================================

engine.executar_regressao_linear()

# =========================================================
# RESÍDUOS
# =========================================================

engine.analisar_residuos()

# =========================================================
# PREVISÃO
# =========================================================

engine.prever_geracao(
    passos_futuros=5
)

# =========================================================
# SIMULAÇÃO
# =========================================================

engine.simular_cenarios()

# =========================================================
# ESTATÍSTICAS
# =========================================================

engine.exibir_estatisticas()

UI.titulo(
    "ANÁLISE PREDITIVA FINALIZADA"
)