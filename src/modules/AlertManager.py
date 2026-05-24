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
                f"[bold cyan]{texto}[/bold cyan]",
                border_style="bright_blue",
                padding=(1, 5)
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
# ENUMS
# =========================================================

class TipoAlerta(Enum):

    ENERGETICO = "ENERGÉTICO"

    CLIMATICO = "CLIMÁTICO"

    ESTRUTURAL = "ESTRUTURAL"

    OPERACIONAL = "OPERACIONAL"

    CRITICO = "CRÍTICO"


class Severidade(Enum):

    BAIXA = 1

    MEDIA = 2

    ALTA = 3

    CRITICA = 4


class CanalNotificacao(Enum):

    PAINEL = "PAINEL CENTRAL"

    MOBILE = "DISPOSITIVO MÓVEL"

    RADIO = "RÁDIO OPERACIONAL"

    EMERGENCIA = "SISTEMA DE EMERGÊNCIA"


# =========================================================
# MODELOS
# =========================================================

@dataclass
class Alerta:

    id_alerta: int

    tipo: TipoAlerta

    severidade: Severidade

    mensagem: str

    timestamp: datetime


# =========================================================
# ALERT MANAGER
# =========================================================

class AlertManager:
    """
    Sistema responsável pela comunicação
    operacional da colônia Aurora.
    """

    def __init__(self):

        # ==============================================
        # ALERTAS
        # ==============================================

        self.alertas: List[Alerta] = []

        # ==============================================
        # FILA
        # ==============================================

        self.fila_alertas = []

        # ==============================================
        # OPERADORES
        # ==============================================

        self.operadores = [

            "Operador Alpha",

            "Operador Beta",

            "Supervisor Central"
        ]

        # ==============================================
        # CONTADOR
        # ==============================================

        self.contador_alertas = 0

        UI.titulo(
            "ALERT MANAGER ONLINE"
        )

    # =====================================================
    # GERAÇÃO
    # =====================================================

    def gerar_alerta(
        self,
        tipo: TipoAlerta,
        severidade: Severidade,
        mensagem: str
    ) -> Alerta:

        self.contador_alertas += 1

        alerta = Alerta(

            id_alerta=self.contador_alertas,

            tipo=tipo,

            severidade=severidade,

            mensagem=mensagem,

            timestamp=datetime.now()
        )

        self.alertas.append(alerta)

        # ==============================================
        # PRIORIDADE
        # ==============================================

        heapq.heappush(

            self.fila_alertas,

            (
                -alerta.severidade.value,

                alerta.id_alerta,

                alerta
            )
        )

        # ==============================================
        # COR POR SEVERIDADE
        # ==============================================

        cores = {

            Severidade.BAIXA: "green",

            Severidade.MEDIA: "yellow",

            Severidade.ALTA: "orange1",

            Severidade.CRITICA: "red"
        }

        cor = cores[severidade]

        painel = Panel.fit(

            (
                f"[bold cyan]ID:[/bold cyan] "
                f"{alerta.id_alerta}\n\n"

                f"[bold yellow]TIPO:[/bold yellow] "
                f"{alerta.tipo.value}\n\n"

                f"[bold red]SEVERIDADE:[/bold red] "
                f"{alerta.severidade.name}\n\n"

                f"[white]{alerta.mensagem}[/white]"
            ),

            title="[bold]ALERTA GERADO[/bold]",

            border_style=cor,

            padding=(1, 4)
        )

        console.print(painel)

        return alerta

    # =====================================================
    # CLASSIFICAÇÃO
    # =====================================================

    def classificar_alerta(
        self,
        alerta: Alerta
    ) -> str:

        UI.secao(
            "CLASSIFICAÇÃO OPERACIONAL"
        )

        if alerta.severidade == Severidade.CRITICA:

            classificacao = (
                "RISCO IMEDIATO À COLÔNIA"
            )

            cor = "red"

        elif alerta.severidade == Severidade.ALTA:

            classificacao = (
                "RISCO OPERACIONAL ELEVADO"
            )

            cor = "orange1"

        elif alerta.severidade == Severidade.MEDIA:

            classificacao = (
                "MONITORAMENTO NECESSÁRIO"
            )

            cor = "yellow"

        else:

            classificacao = (
                "EVENTO INFORMATIVO"
            )

            cor = "green"

        tabela = Table(
            title="Diagnóstico do Alerta",
            box=box.ROUNDED
        )

        tabela.add_column(
            "Campo",
            style="cyan"
        )

        tabela.add_column(
            "Valor",
            style=cor
        )

        tabela.add_row(
            "ID",
            str(alerta.id_alerta)
        )

        tabela.add_row(
            "Tipo",
            alerta.tipo.value
        )

        tabela.add_row(
            "Severidade",
            alerta.severidade.name
        )

        tabela.add_row(
            "Classificação",
            classificacao
        )

        console.print(tabela)

        return classificacao

    # =====================================================
    # NOTIFICAÇÃO
    # =====================================================

    def notificar_operador(
        self,
        alerta: Alerta
    ):

        UI.secao(
            "ENVIO DE NOTIFICAÇÕES"
        )

        # ==============================================
        # CANAL
        # ==============================================

        if alerta.severidade == Severidade.CRITICA:

            canal = (
                CanalNotificacao.EMERGENCIA
            )

            cor = "red"

        elif alerta.severidade == Severidade.ALTA:

            canal = (
                CanalNotificacao.RADIO
            )

            cor = "orange1"

        elif alerta.severidade == Severidade.MEDIA:

            canal = (
                CanalNotificacao.MOBILE
            )

            cor = "yellow"

        else:

            canal = (
                CanalNotificacao.PAINEL
            )

            cor = "green"

        tabela = Table(
            title="Distribuição Operacional",
            box=box.DOUBLE_EDGE,
            show_lines=True
        )

        tabela.add_column(
            "Operador",
            style="cyan"
        )

        tabela.add_column(
            "Canal",
            style=cor
        )

        tabela.add_column(
            "Mensagem",
            style="white"
        )

        for operador in self.operadores:

            tabela.add_row(
                operador,
                canal.value,
                alerta.mensagem
            )

        console.print(tabela)

    # =====================================================
    # PROCESSAMENTO
    # =====================================================

    def processar_fila_alertas(self):

        UI.titulo(
            "PROCESSAMENTO DA FILA"
        )

        while self.fila_alertas:

            _, _, alerta = heapq.heappop(
                self.fila_alertas
            )

            self.classificar_alerta(
                alerta
            )

            self.notificar_operador(
                alerta
            )

    # =====================================================
    # DASHBOARD
    # =====================================================

    def exibir_dashboard(self):

        UI.titulo(
            "DASHBOARD OPERACIONAL"
        )

        if not self.alertas:

            UI.sucesso(
                "Nenhum alerta ativo"
            )

            return

        tabela = Table(
            title="Central de Alertas",
            box=box.HEAVY,
            show_lines=True
        )

        tabela.add_column(
            "ID",
            style="yellow",
            justify="center"
        )

        tabela.add_column(
            "Tipo",
            style="cyan"
        )

        tabela.add_column(
            "Severidade",
            style="red"
        )

        tabela.add_column(
            "Mensagem",
            style="white"
        )

        tabela.add_column(
            "Horário",
            style="magenta"
        )

        for alerta in self.alertas:

            if alerta.severidade == Severidade.CRITICA:

                severidade = (
                    "[bold red]CRÍTICA[/bold red]"
                )

            elif alerta.severidade == Severidade.ALTA:

                severidade = (
                    "[bold orange1]ALTA[/bold orange1]"
                )

            elif alerta.severidade == Severidade.MEDIA:

                severidade = (
                    "[bold yellow]MÉDIA[/bold yellow]"
                )

            else:

                severidade = (
                    "[bold green]BAIXA[/bold green]"
                )

            tabela.add_row(

                str(alerta.id_alerta),

                alerta.tipo.value,

                severidade,

                alerta.mensagem,

                alerta.timestamp.strftime(
                    "%H:%M:%S"
                )
            )

        console.print(tabela)

    # =====================================================
    # ESTATÍSTICAS
    # =====================================================

    def exibir_estatisticas(self):

        UI.titulo(
            "ESTATÍSTICAS OPERACIONAIS"
        )

        estatisticas: Dict[str, int] = {}

        for alerta in self.alertas:

            tipo = alerta.tipo.value

            if tipo not in estatisticas:

                estatisticas[tipo] = 0

            estatisticas[tipo] += 1

        paineis = []

        for tipo, quantidade in (
            estatisticas.items()
        ):

            painel = Panel.fit(

                (
                    f"[bold cyan]{quantidade}"
                    f"[/bold cyan]"
                ),

                title=tipo,

                border_style="bright_blue",

                padding=(1, 4)
            )

            paineis.append(painel)

        console.print(
            Columns(paineis)
        )


# =========================================================
# EXECUÇÃO
# =========================================================

console.clear()

UI.titulo(
    "AURORA SIGER • ALERT MANAGER"
)

manager = AlertManager()

# =========================================================
# ALERTAS
# =========================================================

alerta1 = manager.gerar_alerta(

    tipo=TipoAlerta.ENERGETICO,

    severidade=Severidade.ALTA,

    mensagem=(
        "Sobrecarga detectada "
        "no núcleo solar."
    )
)

alerta2 = manager.gerar_alerta(

    tipo=TipoAlerta.CLIMATICO,

    severidade=Severidade.MEDIA,

    mensagem=(
        "Tempestade de areia "
        "aproximando-se."
    )
)

alerta3 = manager.gerar_alerta(

    tipo=TipoAlerta.ESTRUTURAL,

    severidade=Severidade.CRITICA,

    mensagem=(
        "Falha estrutural "
        "detectada no módulo B."
    )
)

alerta4 = manager.gerar_alerta(

    tipo=TipoAlerta.OPERACIONAL,

    severidade=Severidade.BAIXA,

    mensagem=(
        "Rotina de manutenção "
        "agendada."
    )
)

# =========================================================
# PROCESSAMENTO
# =========================================================

manager.processar_fila_alertas()

# =========================================================
# DASHBOARD
# =========================================================

manager.exibir_dashboard()

# =========================================================
# ESTATÍSTICAS
# =========================================================

manager.exibir_estatisticas()

# =========================================================
# FINALIZAÇÃO
# =========================================================

console.print()

console.print(
    Panel.fit(
        "[bold cyan]"
        "ALERT MANAGER FINALIZADO"
        "[/bold cyan]",
        border_style="cyan",
        padding=(1, 5)
    )
)