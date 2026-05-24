from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List
import numpy as np

# =========================================================
# RICH TERMINAL UI
# =========================================================

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.rule import Rule
from rich import box

console = Console()

# =========================================================
# MODELO
# =========================================================

@dataclass
class RegistroProcessado:
    sensor_id: str
    tipo: str
    valor: float
    timestamp: datetime


# =========================================================
# UI AUXILIAR
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
                padding=(1, 4)
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
    def erro(texto):

        console.print(
            f"[bold red]✖ {texto}[/bold red]"
        )

    @staticmethod
    def info(texto):

        console.print(
            f"[bold blue]ℹ {texto}[/bold blue]"
        )

    @staticmethod
    def warning(texto):

        console.print(
            f"[bold yellow]⚠ {texto}[/bold yellow]"
        )


# =========================================================
# PROCESSING ENGINE
# =========================================================

class ProcessingEngine:
    """
    Camada responsável pelo processamento dos dados
    da colônia Aurora.

    Responsabilidades:
    - limpeza de dados;
    - validação;
    - cálculos;
    - estatísticas;
    - agregações;
    - atualização de estados.
    """

    def __init__(self):

        # ==============================================
        # Histórico processado
        # ==============================================

        self.dados_processados: List[
            RegistroProcessado
        ] = []

        # ==============================================
        # Vetores NumPy
        # ==============================================

        self.vetor_temperaturas = np.array([])

        self.vetor_consumo = np.array([])

        # ==============================================
        # Matrizes
        # ==============================================

        self.matriz_operacional = np.zeros(
            (5, 24)
        )

        # ==============================================
        # Estatísticas
        # ==============================================

        self.estatisticas: Dict[
            str,
            Dict
        ] = {}

        # ==============================================
        # Estados
        # ==============================================

        self.estado_colonia = {
            "energia": "ESTÁVEL",
            "temperatura": "NORMAL",
            "estrutura": "SEGURA"
        }

        UI.titulo(
            "PROCESSING ENGINE INICIALIZADO"
        )

    # =====================================================
    # LIMPEZA
    # =====================================================

    def limpar_dados(
        self,
        registros: List[RegistroProcessado]
    ) -> List[RegistroProcessado]:

        UI.secao(
            "LIMPEZA DE DADOS"
        )

        dados_limpos = []

        for registro in registros:

            if registro.valor is None:
                continue

            if np.isnan(registro.valor):
                continue

            dados_limpos.append(registro)

        tabela = Table(
            title="Resultado da Limpeza",
            box=box.ROUNDED
        )

        tabela.add_column(
            "Registros Recebidos",
            justify="center"
        )

        tabela.add_column(
            "Registros Válidos",
            justify="center"
        )

        tabela.add_row(
            str(len(registros)),
            str(len(dados_limpos))
        )

        console.print(tabela)

        UI.sucesso(
            "Limpeza concluída"
        )

        return dados_limpos

    # =====================================================
    # VALIDAÇÃO
    # =====================================================

    def validar_dados(
        self,
        registro: RegistroProcessado
    ) -> bool:

        limites = {
            "temperatura_interna": (-20, 50),
            "temperatura_externa": (-150, 80),
            "velocidade_vento": (0, 250),
            "geracao_solar": (0, 1500),
            "geracao_eolica": (0, 1200),
            "consumo_energetico": (0, 5000),
            "integridade_estrutural": (0, 100)
        }

        if registro.tipo not in limites:

            UI.erro(
                f"Tipo desconhecido -> {registro.tipo}"
            )

            return False

        minimo, maximo = limites[
            registro.tipo
        ]

        valido = (
            minimo <= registro.valor <= maximo
        )

        tabela = Table(
            title="Validação Operacional",
            box=box.SIMPLE_HEAVY
        )

        tabela.add_column("Sensor")
        tabela.add_column("Tipo")
        tabela.add_column("Valor")
        tabela.add_column("Status")

        status = (
            "[green]VÁLIDO[/green]"
            if valido
            else "[red]INVÁLIDO[/red]"
        )

        tabela.add_row(
            registro.sensor_id,
            registro.tipo,
            f"{registro.valor:.2f}",
            status
        )

        console.print(tabela)

        return valido

    # =====================================================
    # MÉDIA
    # =====================================================

    def calcular_media(
        self,
        vetor: np.ndarray
    ) -> float:

        UI.secao(
            "CÁLCULO DE MÉDIA"
        )

        if len(vetor) == 0:

            UI.warning(
                "Vetor vazio"
            )

            return 0

        media = float(np.mean(vetor))

        painel = Panel.fit(
            f"[bold cyan]{media:.2f}[/bold cyan]",
            title="Média Calculada",
            border_style="cyan"
        )

        console.print(painel)

        return media

    # =====================================================
    # MATRIZ
    # =====================================================

    def atualizar_matriz(
        self,
        modulo: int,
        horario: int,
        valor: float
    ):

        self.matriz_operacional[
            modulo
        ][horario] = valor

        tabela = Table(
            title="Atualização Matricial",
            box=box.MINIMAL_DOUBLE_HEAD
        )

        tabela.add_column("Módulo")
        tabela.add_column("Horário")
        tabela.add_column("Valor")

        tabela.add_row(
            str(modulo),
            str(horario),
            f"{valor:.2f}"
        )

        console.print(tabela)

    # =====================================================
    # ESTATÍSTICAS
    # =====================================================

    def processar_estatisticas(self):

        UI.titulo(
            "PROCESSAMENTO ESTATÍSTICO"
        )

        if len(self.vetor_temperaturas) > 0:

            self.estatisticas["temperaturas"] = {

                "media":
                    float(
                        np.mean(
                            self.vetor_temperaturas
                        )
                    ),

                "maximo":
                    float(
                        np.max(
                            self.vetor_temperaturas
                        )
                    ),

                "minimo":
                    float(
                        np.min(
                            self.vetor_temperaturas
                        )
                    ),

                "desvio_padrao":
                    float(
                        np.std(
                            self.vetor_temperaturas
                        )
                    )
            }

        if len(self.vetor_consumo) > 0:

            self.estatisticas["consumo"] = {

                "media":
                    float(
                        np.mean(
                            self.vetor_consumo
                        )
                    ),

                "pico":
                    float(
                        np.max(
                            self.vetor_consumo
                        )
                    ),

                "minimo":
                    float(
                        np.min(
                            self.vetor_consumo
                        )
                    )
            }

        for categoria, valores in (
            self.estatisticas.items()
        ):

            tabela = Table(
                title=f"{categoria.upper()}",
                box=box.ROUNDED
            )

            tabela.add_column("Métrica")
            tabela.add_column("Valor")

            for chave, valor in valores.items():

                tabela.add_row(
                    chave,
                    f"{valor:.2f}"
                )

            console.print(tabela)

    # =====================================================
    # AGREGAÇÕES
    # =====================================================

    def executar_agregacoes(
        self,
        registros: List[RegistroProcessado]
    ):

        UI.titulo(
            "AGREGAÇÕES ANALÍTICAS"
        )

        agregacoes = {}

        for registro in registros:

            if registro.tipo not in agregacoes:

                agregacoes[
                    registro.tipo
                ] = []

            agregacoes[
                registro.tipo
            ].append(
                registro.valor
            )

        tabela = Table(
            title="Resultado das Agregações",
            box=box.HEAVY
        )

        tabela.add_column("Tipo")
        tabela.add_column("Média")
        tabela.add_column("Soma")
        tabela.add_column("Quantidade")

        for tipo, valores in agregacoes.items():

            media = np.mean(valores)

            soma = np.sum(valores)

            tabela.add_row(
                tipo,
                f"{media:.2f}",
                f"{soma:.2f}",
                str(len(valores))
            )

        console.print(tabela)

    # =====================================================
    # ESTADOS
    # =====================================================

    def atualizar_estados(self):

        UI.titulo(
            "ATUALIZAÇÃO DOS ESTADOS"
        )

        media_temp = self.calcular_media(
            self.vetor_temperaturas
        )

        media_consumo = self.calcular_media(
            self.vetor_consumo
        )

        # ==========================================
        # TEMPERATURA
        # ==========================================

        if media_temp > 35:

            self.estado_colonia[
                "temperatura"
            ] = "CRÍTICA"

        elif media_temp > 28:

            self.estado_colonia[
                "temperatura"
            ] = "ALERTA"

        else:

            self.estado_colonia[
                "temperatura"
            ] = "NORMAL"

        # ==========================================
        # ENERGIA
        # ==========================================

        if media_consumo > 3000:

            self.estado_colonia[
                "energia"
            ] = "SOBRECARGA"

        elif media_consumo > 1800:

            self.estado_colonia[
                "energia"
            ] = "ALERTA"

        else:

            self.estado_colonia[
                "energia"
            ] = "ESTÁVEL"

        tabela = Table(
            title="Estado Atual da Colônia",
            box=box.DOUBLE
        )

        tabela.add_column("Subsystem")
        tabela.add_column("Status")

        for chave, valor in (
            self.estado_colonia.items()
        ):

            cor = "green"

            if valor in [
                "ALERTA",
                "SOBRECARGA"
            ]:
                cor = "yellow"

            if valor == "CRÍTICA":
                cor = "red"

            tabela.add_row(
                chave.upper(),
                f"[{cor}]{valor}[/{cor}]"
            )

        console.print(tabela)

    # =====================================================
    # INGESTÃO
    # =====================================================

    def adicionar_registro(
        self,
        sensor_id: str,
        tipo: str,
        valor: float
    ):

        UI.secao(
            "INGESTÃO DE TELEMETRIA"
        )

        registro = RegistroProcessado(
            sensor_id=sensor_id,
            tipo=tipo,
            valor=valor,
            timestamp=datetime.now()
        )

        if not self.validar_dados(registro):

            UI.erro(
                "Registro descartado"
            )

            return

        self.dados_processados.append(
            registro
        )

        # ==========================================
        # Vetores especializados
        # ==========================================

        if "temperatura" in tipo:

            self.vetor_temperaturas = np.append(
                self.vetor_temperaturas,
                valor
            )

        if "consumo" in tipo:

            self.vetor_consumo = np.append(
                self.vetor_consumo,
                valor
            )

        painel = Panel.fit(
            (
                f"[bold green]"
                f"{sensor_id}"
                f"[/bold green]\n\n"
                f"Tipo: {tipo}\n"
                f"Valor: {valor:.2f}\n"
                f"Timestamp: "
                f"{registro.timestamp.strftime('%H:%M:%S')}"
            ),
            title="Registro Processado",
            border_style="green"
        )

        console.print(painel)


# =========================================================
# EXEMPLO DE UTILIZAÇÃO
# =========================================================

UI.titulo(
    "AURORA PROCESSING ENGINE"
)

engine = ProcessingEngine()

# =========================================================
# REGISTROS
# =========================================================

engine.adicionar_registro(
    "TEMP-INT-01",
    "temperatura_interna",
    24.8
)

engine.adicionar_registro(
    "TEMP-INT-02",
    "temperatura_interna",
    29.3
)

engine.adicionar_registro(
    "ENERGIA-01",
    "consumo_energetico",
    2100
)

engine.adicionar_registro(
    "ENERGIA-02",
    "consumo_energetico",
    3200
)

# =========================================================
# MÉDIA
# =========================================================

engine.calcular_media(
    engine.vetor_temperaturas
)

# =========================================================
# MATRIZ
# =========================================================

engine.atualizar_matriz(
    modulo=1,
    horario=14,
    valor=88.7
)

# =========================================================
# ESTATÍSTICAS
# =========================================================

engine.processar_estatisticas()

# =========================================================
# AGREGAÇÕES
# =========================================================

engine.executar_agregacoes(
    engine.dados_processados
)

# =========================================================
# ESTADOS
# =========================================================

engine.atualizar_estados()

UI.titulo(
    "PROCESSAMENTO FINALIZADO"
)