from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
import hashlib
import numpy as np

# =========================================================
# RICH TERMINAL UI
# =========================================================

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich.rule import Rule
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
# MODELOS
# =========================================================

@dataclass
class Telemetria:

    sensor_id: str

    tipo: str

    valor: float

    timestamp: datetime


# =========================================================
# NÓ DA ÁRVORE
# =========================================================

class TreeNode:

    def __init__(self, nome: str):

        self.nome = nome

        self.filhos: List["TreeNode"] = []

    def adicionar_filho(
        self,
        node: "TreeNode"
    ):

        self.filhos.append(node)


# =========================================================
# STORAGE MANAGER
# =========================================================

class StorageManager:
    """
    Camada responsável pelo armazenamento
    e organização dos dados da colônia Aurora.
    """

    def __init__(self):

        # ==============================================
        # HISTÓRICO
        # ==============================================

        self.historico: List[Telemetria] = []

        # ==============================================
        # VETORES
        # ==============================================

        self.buffer_temperaturas = np.array([])

        # ==============================================
        # MATRIZ
        # ==============================================

        self.matriz_energia = np.zeros((5, 24))

        # ==============================================
        # HASH TABLE
        # ==============================================

        self.hash_telemetria: Dict[
            str,
            List[Telemetria]
        ] = {}

        # ==============================================
        # ÁRVORE
        # ==============================================

        self.arvore_colonia = TreeNode(
            "Aurora"
        )

        self._inicializar_arvore()

        UI.titulo(
            "STORAGE MANAGER ONLINE"
        )

    # =====================================================
    # ÁRVORE
    # =====================================================

    def _inicializar_arvore(self):

        energia = TreeNode("Energia")

        sensores = TreeNode("Sensores")

        infraestrutura = TreeNode(
            "Infraestrutura"
        )

        energia.adicionar_filho(
            TreeNode("Solar")
        )

        energia.adicionar_filho(
            TreeNode("Eólica")
        )

        energia.adicionar_filho(
            TreeNode("Consumo")
        )

        sensores.adicionar_filho(
            TreeNode("Temperatura")
        )

        sensores.adicionar_filho(
            TreeNode("Vento")
        )

        infraestrutura.adicionar_filho(
            TreeNode("Módulos")
        )

        infraestrutura.adicionar_filho(
            TreeNode("Integridade")
        )

        self.arvore_colonia.adicionar_filho(
            energia
        )

        self.arvore_colonia.adicionar_filho(
            sensores
        )

        self.arvore_colonia.adicionar_filho(
            infraestrutura
        )

    # =====================================================
    # ARMAZENAMENTO
    # =====================================================

    def armazenar_telemetria(
        self,
        sensor_id: str,
        tipo: str,
        valor: float
    ):

        registro = Telemetria(

            sensor_id=sensor_id,

            tipo=tipo,

            valor=valor,

            timestamp=datetime.now()
        )

        # ==============================================
        # LISTA
        # ==============================================

        self.historico.append(
            registro
        )

        # ==============================================
        # HASH TABLE
        # ==============================================

        if sensor_id not in self.hash_telemetria:

            self.hash_telemetria[
                sensor_id
            ] = []

        self.hash_telemetria[
            sensor_id
        ].append(registro)

        # ==============================================
        # BUFFER
        # ==============================================

        if "temperatura" in tipo.lower():

            self.buffer_temperaturas = np.append(

                self.buffer_temperaturas,

                valor
            )

        # ==============================================
        # OUTPUT VISUAL
        # ==============================================

        tabela = Table(
            title="Registro Armazenado",
            box=box.ROUNDED
        )

        tabela.add_column(
            "Sensor",
            style="cyan"
        )

        tabela.add_column(
            "Tipo",
            style="yellow"
        )

        tabela.add_column(
            "Valor",
            style="green"
        )

        tabela.add_column(
            "Horário",
            style="magenta"
        )

        tabela.add_row(
            sensor_id,
            tipo,
            f"{valor:.2f}",
            registro.timestamp.strftime(
                "%H:%M:%S"
            )
        )

        console.print(tabela)

    # =====================================================
    # CONSULTA
    # =====================================================

    def consultar_historico(
        self,
        sensor_id: Optional[str] = None
    ) -> List[Telemetria]:

        UI.titulo(
            "CONSULTA DE HISTÓRICO"
        )

        if sensor_id:

            UI.info(
                f"Consulta HASH: {sensor_id}"
            )

            registros = self.hash_telemetria.get(
                sensor_id,
                []
            )

        else:

            UI.info(
                "Consulta Global"
            )

            registros = self.historico

        if not registros:

            UI.alerta(
                "Nenhum registro encontrado"
            )

            return []

        tabela = Table(
            title="Histórico Telemetria",
            box=box.DOUBLE_EDGE,
            show_lines=True
        )

        tabela.add_column(
            "Sensor",
            style="cyan"
        )

        tabela.add_column(
            "Tipo",
            style="yellow"
        )

        tabela.add_column(
            "Valor",
            style="green"
        )

        tabela.add_column(
            "Timestamp",
            style="magenta"
        )

        for item in registros:

            tabela.add_row(
                item.sensor_id,
                item.tipo,
                f"{item.valor:.2f}",
                item.timestamp.strftime(
                    "%d/%m %H:%M:%S"
                )
            )

        console.print(tabela)

        return registros

    # =====================================================
    # HASH
    # =====================================================

    def atualizar_hash(self):

        UI.titulo(
            "VERIFICAÇÃO DE INTEGRIDADE HASH"
        )

        tabela = Table(
            title="SHA-256",
            box=box.HEAVY,
            show_lines=True
        )

        tabela.add_column(
            "Sensor",
            style="cyan"
        )

        tabela.add_column(
            "Hash",
            style="green"
        )

        for sensor_id, registros in (
            self.hash_telemetria.items()
        ):

            conteudo = "".join(

                f"{r.valor}{r.timestamp}"

                for r in registros
            )

            hash_integridade = hashlib.sha256(

                conteudo.encode()

            ).hexdigest()

            tabela.add_row(
                sensor_id,
                hash_integridade[:32] + "..."
            )

        console.print(tabela)

    # =====================================================
    # MATRIZ
    # =====================================================

    def atualizar_matriz_energia(
        self,
        modulo: int,
        hora: int,
        consumo: float
    ):

        self.matriz_energia[
            modulo
        ][hora] = consumo

        UI.sucesso(
            f"Matriz atualizada "
            f"(Módulo={modulo}, "
            f"Hora={hora}, "
            f"Consumo={consumo:.2f})"
        )

    def exibir_matriz_energia(self):

        UI.titulo(
            "MATRIZ ENERGÉTICA"
        )

        tabela = Table(
            title="Consumo Energético",
            box=box.SQUARE
        )

        tabela.add_column(
            "Módulo",
            style="cyan"
        )

        for hora in range(24):

            tabela.add_column(
                str(hora),
                justify="center"
            )

        for i, linha in enumerate(
            self.matriz_energia
        ):

            tabela.add_row(

                f"M-{i}",

                *[
                    (
                        f"[green]{v:.0f}[/green]"
                        if v > 0
                        else "-"
                    )

                    for v in linha
                ]
            )

        console.print(tabela)

    # =====================================================
    # TEMPERATURAS
    # =====================================================

    def calcular_media_temperaturas(self):

        UI.titulo(
            "ANÁLISE TÉRMICA"
        )

        if len(self.buffer_temperaturas) == 0:

            UI.alerta(
                "Sem temperaturas registradas"
            )

            return 0

        media = np.mean(
            self.buffer_temperaturas
        )

        painel = Panel.fit(

            f"[bold green]"
            f"{media:.2f} °C"
            f"[/bold green]",

            title="Temperatura Média",

            border_style="green",

            padding=(1, 5)
        )

        console.print(painel)

        return media

    # =====================================================
    # ÁRVORE
    # =====================================================

    def exibir_hierarquia(self):

        UI.titulo(
            "HIERARQUIA DA COLÔNIA"
        )

        arvore = Tree(
            "[bold cyan]Aurora[/bold cyan]"
        )

        energia = arvore.add(
            "[yellow]Energia[/yellow]"
        )

        energia.add(
            "[green]Solar[/green]"
        )

        energia.add(
            "[green]Eólica[/green]"
        )

        energia.add(
            "[green]Consumo[/green]"
        )

        sensores = arvore.add(
            "[yellow]Sensores[/yellow]"
        )

        sensores.add(
            "[green]Temperatura[/green]"
        )

        sensores.add(
            "[green]Vento[/green]"
        )

        infraestrutura = arvore.add(
            "[yellow]Infraestrutura[/yellow]"
        )

        infraestrutura.add(
            "[green]Módulos[/green]"
        )

        infraestrutura.add(
            "[green]Integridade[/green]"
        )

        console.print(arvore)


# =========================================================
# EXEMPLO DE UTILIZAÇÃO
# =========================================================

console.clear()

UI.titulo(
    "AURORA SIGER • STORAGE MANAGER"
)

storage = StorageManager()

# =========================================================
# ARMAZENAMENTO
# =========================================================

storage.armazenar_telemetria(
    "TEMP-INT-01",
    "temperatura_interna",
    24.5
)

storage.armazenar_telemetria(
    "VENTO-01",
    "velocidade_vento",
    83.2
)

storage.armazenar_telemetria(
    "SOLAR-01",
    "geracao_solar",
    720.8
)

# =========================================================
# CONSULTA
# =========================================================

storage.consultar_historico(
    "TEMP-INT-01"
)

# =========================================================
# HASH
# =========================================================

storage.atualizar_hash()

# =========================================================
# MATRIZ
# =========================================================

storage.atualizar_matriz_energia(
    modulo=0,
    hora=10,
    consumo=520
)

storage.exibir_matriz_energia()

# =========================================================
# MÉDIA
# =========================================================

storage.calcular_media_temperaturas()

# =========================================================
# HIERARQUIA
# =========================================================

storage.exibir_hierarquia()

# =========================================================
# FINALIZAÇÃO
# =========================================================

console.print()

console.print(
    Panel.fit(
        "[bold cyan]"
        "STORAGE MANAGER FINALIZADO"
        "[/bold cyan]",
        border_style="cyan",
        padding=(1, 5)
    )
)