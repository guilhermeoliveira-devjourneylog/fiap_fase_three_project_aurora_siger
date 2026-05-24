from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List
import heapq

# =========================================================
# RICH TERMINAL UI
# =========================================================

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.columns import Columns
from rich.rule import Rule
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
                border_style="bright_blue",
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

    @staticmethod
    def status_panel(
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
# ENUMS
# =========================================================

class NivelRisco(Enum):

    BAIXO = "BAIXO"

    MODERADO = "MODERADO"

    ALTO = "ALTO"

    CRITICO = "CRÍTICO"


class EstadoSistema(Enum):

    NORMAL = "NORMAL"

    ALERTA = "ALERTA"

    CONTINGENCIA = "CONTINGÊNCIA"

    EMERGENCIA = "EMERGÊNCIA"


# =========================================================
# MODELOS
# =========================================================

@dataclass
class EventoOperacional:

    subsistema: str

    valor: float

    limite: float

    timestamp: datetime


# =========================================================
# DECISION ENGINE
# =========================================================

class DecisionEngine:
    """
    Motor responsável por:
    - regras condicionais;
    - priorização;
    - análise de risco;
    - decisões automáticas;
    - acionamento de alertas.
    """

    def __init__(self):

        # ==============================================
        # Estado Global
        # ==============================================

        self.estado_atual = (
            EstadoSistema.NORMAL
        )

        # ==============================================
        # Heap Prioritário
        # ==============================================

        self.fila_prioridade = []

        # ==============================================
        # Alertas
        # ==============================================

        self.alertas: List[str] = []

        # ==============================================
        # Subsistemas
        # ==============================================

        self.subsistemas: Dict[str, Dict] = {

            "energia": {

                "estado": "ESTÁVEL",

                "prioridade": 1
            },

            "temperatura": {

                "estado": "NORMAL",

                "prioridade": 2
            },

            "estrutura": {

                "estado": "SEGURA",

                "prioridade": 0
            },

            "comunicacao": {

                "estado": "ONLINE",

                "prioridade": 3
            },

            "suporte_vida": {

                "estado": "ATIVO",

                "prioridade": -1
            }
        }

        UI.titulo(
            "DECISION ENGINE ONLINE"
        )

    # =====================================================
    # ANÁLISE DE RISCO
    # =====================================================

    def analisar_risco(
        self,
        evento: EventoOperacional
    ) -> NivelRisco:

        UI.secao(
            "ANÁLISE DE RISCO"
        )

        percentual = (
            evento.valor / evento.limite
        ) * 100

        # ==============================================
        # CLASSIFICAÇÃO
        # ==============================================

        if percentual < 70:

            risco = NivelRisco.BAIXO

            cor = "green"

        elif percentual < 90:

            risco = NivelRisco.MODERADO

            cor = "yellow"

        elif percentual < 110:

            risco = NivelRisco.ALTO

            cor = "orange1"

        else:

            risco = NivelRisco.CRITICO

            cor = "red"

        # ==============================================
        # TABELA
        # ==============================================

        tabela = Table(
            title="Diagnóstico Operacional",
            box=box.ROUNDED
        )

        tabela.add_column(
            "Subsistema",
            style="cyan"
        )

        tabela.add_column(
            "Valor",
            style="white"
        )

        tabela.add_column(
            "Limite",
            style="yellow"
        )

        tabela.add_column(
            "Uso %",
            style=cor
        )

        tabela.add_column(
            "Risco",
            style=cor
        )

        tabela.add_row(
            evento.subsistema.upper(),
            f"{evento.valor:.2f}",
            f"{evento.limite:.2f}",
            f"{percentual:.1f}%",
            risco.value
        )

        console.print(tabela)

        return risco

    # =====================================================
    # PRIORIZAÇÃO
    # =====================================================

    def priorizar_subsistemas(self):

        UI.titulo(
            "PRIORIZAÇÃO DE SUBSISTEMAS"
        )

        self.fila_prioridade.clear()

        for nome, dados in self.subsistemas.items():

            prioridade = dados["prioridade"]

            heapq.heappush(
                self.fila_prioridade,
                (
                    prioridade,
                    nome
                )
            )

        tabela = Table(
            title="Fila Operacional",
            box=box.DOUBLE_EDGE,
            show_lines=True
        )

        tabela.add_column(
            "Prioridade",
            justify="center",
            style="yellow"
        )

        tabela.add_column(
            "Subsistema",
            style="cyan"
        )

        tabela.add_column(
            "Estado",
            style="green"
        )

        while self.fila_prioridade:

            prioridade, nome = heapq.heappop(
                self.fila_prioridade
            )

            tabela.add_row(
                str(prioridade),
                nome.upper(),
                self.subsistemas[nome][
                    "estado"
                ]
            )

        console.print(tabela)

    # =====================================================
    # AUTOMAÇÃO
    # =====================================================

    def executar_automacao(
        self,
        evento: EventoOperacional
    ):

        UI.titulo(
            f"AUTOMAÇÃO • {evento.subsistema.upper()}"
        )

        risco = self.analisar_risco(
            evento
        )

        acao = (
            "Nenhuma ação necessária"
        )

        status = (
            "[green]ESTÁVEL[/green]"
        )

        # ==============================================
        # TEMPERATURA
        # ==============================================

        if evento.subsistema == "temperatura":

            if risco == NivelRisco.CRITICO:

                self.alertas.append(
                    "RESFRIAMENTO DE EMERGÊNCIA ATIVADO"
                )

                self.subsistemas[
                    "temperatura"
                ]["estado"] = "EMERGÊNCIA"

                acao = (
                    "Resfriamento ativado"
                )

                status = (
                    "[red]EMERGÊNCIA[/red]"
                )

        # ==============================================
        # ENERGIA
        # ==============================================

        elif evento.subsistema == "energia":

            if risco in [

                NivelRisco.ALTO,

                NivelRisco.CRITICO
            ]:

                self.alertas.append(
                    "MODO ECONOMIA DE ENERGIA"
                )

                self.subsistemas[
                    "energia"
                ]["estado"] = "CONTINGÊNCIA"

                acao = (
                    "Redução de consumo"
                )

                status = (
                    "[yellow]CONTINGÊNCIA[/yellow]"
                )

        # ==============================================
        # ESTRUTURA
        # ==============================================

        elif evento.subsistema == "estrutura":

            if risco == NivelRisco.CRITICO:

                self.alertas.append(
                    "ISOLAMENTO ESTRUTURAL"
                )

                self.subsistemas[
                    "estrutura"
                ]["estado"] = "RISCO CRÍTICO"

                acao = (
                    "Compartimentos isolados"
                )

                status = (
                    "[red]CRÍTICO[/red]"
                )

        # ==============================================
        # SUPORTE DE VIDA
        # ==============================================

        elif evento.subsistema == "suporte_vida":

            if risco != NivelRisco.BAIXO:

                self.alertas.append(
                    "PROTOCOLO DE SOBREVIVÊNCIA"
                )

                self.subsistemas[
                    "suporte_vida"
                ]["estado"] = "PROTEÇÃO"

                acao = (
                    "Protocolo ativado"
                )

                status = (
                    "[red]PROTEÇÃO[/red]"
                )

        # ==============================================
        # PAINEL DE DECISÃO
        # ==============================================

        painel = Panel.fit(

            (
                f"[bold cyan]SUBSISTEMA:[/bold cyan] "
                f"{evento.subsistema.upper()}\n\n"

                f"[bold yellow]AÇÃO:[/bold yellow] "
                f"{acao}\n\n"

                f"[bold green]STATUS:[/bold green] "
                f"{status}"
            ),

            title="Resposta Automática",

            border_style="bright_blue"
        )

        console.print(painel)

    # =====================================================
    # ALTERAÇÃO DE ESTADO
    # =====================================================

    def alterar_estado(self):

        UI.titulo(
            "ANÁLISE GLOBAL DA COLÔNIA"
        )

        estados_criticos = 0

        estados_alerta = 0

        tabela = Table(
            title="Status dos Subsistemas",
            box=box.HEAVY,
            show_lines=True
        )

        tabela.add_column(
            "Subsistema",
            style="cyan"
        )

        tabela.add_column(
            "Estado",
            style="white"
        )

        for nome, dados in self.subsistemas.items():

            estado = dados["estado"]

            cor = "green"

            if (
                "CRÍTICO" in estado
                or "EMERGÊNCIA" in estado
            ):

                cor = "red"

                estados_criticos += 1

            elif (
                "ALERTA" in estado
                or "CONTINGÊNCIA" in estado
            ):

                cor = "yellow"

                estados_alerta += 1

            tabela.add_row(
                nome.upper(),
                f"[{cor}]{estado}[/{cor}]"
            )

        console.print(tabela)

        # ==============================================
        # DECISÃO GLOBAL
        # ==============================================

        if estados_criticos > 0:

            self.estado_atual = (
                EstadoSistema.EMERGENCIA
            )

            cor = "red"

        elif estados_alerta > 0:

            self.estado_atual = (
                EstadoSistema.CONTINGENCIA
            )

            cor = "yellow"

        else:

            self.estado_atual = (
                EstadoSistema.NORMAL
            )

            cor = "green"

        console.print()

        console.print(
            Panel.fit(

                (
                    f"[bold {cor}]"
                    f"{self.estado_atual.value}"
                    f"[/bold {cor}]"
                ),

                title="ESTADO GLOBAL",

                border_style=cor,

                padding=(1, 8)
            )
        )

    # =====================================================
    # ALERTAS
    # =====================================================

    def exibir_alertas(self):

        UI.titulo(
            "CENTRAL DE ALERTAS"
        )

        if not self.alertas:

            UI.sucesso(
                "Nenhum alerta ativo"
            )

            return

        tabela = Table(
            title="Alertas Operacionais",
            box=box.DOUBLE,
            show_lines=True
        )

        tabela.add_column(
            "ID",
            style="yellow"
        )

        tabela.add_column(
            "Descrição",
            style="red"
        )

        tabela.add_column(
            "Timestamp",
            style="cyan"
        )

        for indice, alerta in enumerate(
            self.alertas,
            start=1
        ):

            tabela.add_row(
                str(indice),
                alerta,
                datetime.now().strftime(
                    "%H:%M:%S"
                )
            )

        console.print(tabela)


# =========================================================
# EXEMPLO DE UTILIZAÇÃO
# =========================================================

console.clear()

UI.titulo(
    "AURORA SIGER • DECISION ENGINE"
)

engine = DecisionEngine()

# =========================================================
# EVENTOS
# =========================================================

evento_temp = EventoOperacional(

    subsistema="temperatura",

    valor=118,

    limite=100,

    timestamp=datetime.now()
)

evento_energia = EventoOperacional(

    subsistema="energia",

    valor=92,

    limite=100,

    timestamp=datetime.now()
)

evento_estrutura = EventoOperacional(

    subsistema="estrutura",

    valor=135,

    limite=100,

    timestamp=datetime.now()
)

# =========================================================
# PRIORIZAÇÃO
# =========================================================

engine.priorizar_subsistemas()

# =========================================================
# AUTOMAÇÃO
# =========================================================

engine.executar_automacao(
    evento_temp
)

engine.executar_automacao(
    evento_energia
)

engine.executar_automacao(
    evento_estrutura
)

# =========================================================
# ESTADO GLOBAL
# =========================================================

engine.alterar_estado()

# =========================================================
# ALERTAS
# =========================================================

engine.exibir_alertas()

# =========================================================
# FINALIZAÇÃO
# =========================================================

console.print()

console.print(
    Panel.fit(

        "[bold cyan]"
        "DECISION ENGINE FINALIZADO"
        "[/bold cyan]",

        border_style="cyan",

        padding=(1, 5)
    )
)