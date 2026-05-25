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
from rich.columns import Columns
from rich.rule import Rule
from rich import box

console = Console()

# =========================================================
# MODELO
# =========================================================

@dataclass
class RegistroProcessado:
    """
    Estrutura responsável por representar um registro
    processado pelo Processing Engine.

    Atributos:
        sensor_id:
            Identificador único do sensor.

        tipo:
            Categoria operacional do sensor.

        valor:
            Valor numérico capturado.

        timestamp:
            Momento exato da ingestão.
    """

    sensor_id: str

    tipo: str

    valor: float

    timestamp: datetime


# =========================================================
# UI AUXILIAR
# =========================================================

class UI:
    """
    Camada utilitária responsável pela renderização
    visual no terminal utilizando Rich.

    Responsabilidades:
    - títulos;
    - seções;
    - mensagens operacionais;
    - painéis;
    - alertas;
    - feedback visual.
    """

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
    Motor analítico responsável pelo processamento
    operacional da Colônia Aurora.

    =====================================================
    RESPONSABILIDADES
    =====================================================

    - ingestão de telemetria;
    - limpeza de dados;
    - validação operacional;
    - cálculos estatísticos;
    - agregações analíticas;
    - atualização matricial;
    - monitoramento de estados;
    - geração de métricas globais.

    =====================================================
    PIPELINE ANALÍTICO
    =====================================================

    Sensores
        ↓
    Validação
        ↓
    Limpeza
        ↓
    Vetorização NumPy
        ↓
    Estatísticas
        ↓
    Estados Operacionais

    =====================================================
    RECURSOS IMPLEMENTADOS
    =====================================================

    - média;
    - desvio padrão;
    - mínimo;
    - máximo;
    - mediana;
    - percentis;
    - agregações;
    - matriz operacional;
    - estados dinâmicos.

    =====================================================
    MELHORIAS PRIORITÁRIAS IMPLEMENTADAS
    =====================================================

    ✔ Correção de vetores vazios
    ✔ Percentis operacionais
    ✔ Mediana
    ✔ Variância
    ✔ Índice de estabilidade
    ✔ Proteção contra índices inválidos
    ✔ Correção de classificação crítica
    ✔ Estatísticas completas
    ✔ Diagnóstico energético
    ✔ Diagnóstico térmico
    """

    def __init__(self):

        # =================================================
        # HISTÓRICO PROCESSADO
        # =================================================

        self.dados_processados: List[
            RegistroProcessado
        ] = []

        # =================================================
        # VETORES NUMPY
        # =================================================

        self.vetor_temperaturas = np.array([])

        self.vetor_consumo = np.array([])

        self.vetor_solar = np.array([])

        self.vetor_eolico = np.array([])

        # =================================================
        # MATRIZ OPERACIONAL
        # =================================================

        self.matriz_operacional = np.zeros(
            (5, 24)
        )

        # =================================================
        # ESTATÍSTICAS
        # =================================================

        self.estatisticas: Dict[
            str,
            Dict
        ] = {}

        # =================================================
        # ESTADOS
        # =================================================

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
        """
        Remove registros inválidos do pipeline.

        Regras:
        - valores None são descartados;
        - NaN é descartado;
        - infinitos são descartados.

        Retorna:
            Lista contendo apenas registros válidos.
        """

        UI.secao(
            "LIMPEZA DE DADOS"
        )

        dados_limpos = []

        for registro in registros:

            if registro.valor is None:
                continue

            if np.isnan(registro.valor):
                continue

            if np.isinf(registro.valor):
                continue

            dados_limpos.append(
                registro
            )

        tabela = Table(
            title="Resultado da Limpeza",
            box=box.ROUNDED
        )

        tabela.add_column(
            "Recebidos",
            justify="center"
        )

        tabela.add_column(
            "Válidos",
            justify="center"
        )

        tabela.add_row(
            str(len(registros)),
            str(len(dados_limpos))
        )

        console.print(tabela)

        return dados_limpos

    # =====================================================
    # VALIDAÇÃO
    # =====================================================

    def validar_dados(
        self,
        registro: RegistroProcessado
    ) -> bool:
        """
        Realiza validação operacional.

        Critérios:
        - tipo conhecido;
        - valor dentro da faixa operacional.

        Retorna:
            True caso válido.
        """

        limites = {

            "temperatura_interna":
                (-20, 50),

            "temperatura_externa":
                (-150, 80),

            "velocidade_vento":
                (0, 250),

            "geracao_solar":
                (0, 1500),

            "geracao_eolica":
                (0, 1200),

            "consumo_energetico":
                (0, 5000),

            "integridade_estrutural":
                (0, 100)
        }

        if registro.tipo not in limites:

            UI.erro(
                f"Tipo desconhecido -> "
                f"{registro.tipo}"
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
        """
        Calcula média aritmética.

        Retorna:
            Média do vetor.
        """

        UI.secao(
            "CÁLCULO DE MÉDIA"
        )

        if vetor.size == 0:

            UI.warning(
                "Vetor vazio"
            )

            return 0.0

        media = float(
            np.mean(vetor)
        )

        painel = Panel.fit(

            f"[bold cyan]{media:.2f}[/bold cyan]",

            title="Média",

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
        """
        Atualiza matriz operacional.

        Args:
            modulo:
                Índice do módulo.

            horario:
                Índice horário.

            valor:
                Valor operacional.
        """

        if not (0 <= modulo < 5):

            UI.erro(
                "Módulo inválido"
            )

            return

        if not (0 <= horario < 24):

            UI.erro(
                "Horário inválido"
            )

            return

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
        """
        Processa estatísticas globais.

        Métricas:
        - média;
        - mediana;
        - máximo;
        - mínimo;
        - desvio padrão;
        - variância;
        - percentil 90.
        """

        UI.titulo(
            "PROCESSAMENTO ESTATÍSTICO"
        )

        self.estatisticas = {}

        datasets = {

            "temperaturas":
                self.vetor_temperaturas,

            "consumo":
                self.vetor_consumo,

            "solar":
                self.vetor_solar,

            "eolico":
                self.vetor_eolico
        }

        for nome, vetor in datasets.items():

            if vetor.size == 0:
                continue

            self.estatisticas[nome] = {

                "media":
                    float(np.mean(vetor)),

                "mediana":
                    float(np.median(vetor)),

                "maximo":
                    float(np.max(vetor)),

                "minimo":
                    float(np.min(vetor)),

                "desvio_padrao":
                    float(np.std(vetor)),

                "variancia":
                    float(np.var(vetor)),

                "percentil_90":
                    float(
                        np.percentile(
                            vetor,
                            90
                        )
                    )
            }

        for categoria, valores in (
            self.estatisticas.items()
        ):

            tabela = Table(
                title=categoria.upper(),
                box=box.ROUNDED
            )

            tabela.add_column(
                "Métrica"
            )

            tabela.add_column(
                "Valor"
            )

            for chave, valor in (
                valores.items()
            ):

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
        """
        Executa agregações analíticas.

        Produz:
        - média;
        - soma;
        - quantidade;
        - máximo;
        - mínimo.
        """

        UI.titulo(
            "AGREGAÇÕES ANALÍTICAS"
        )

        agregacoes = {}

        for registro in registros:

            agregacoes.setdefault(
                registro.tipo,
                []
            ).append(
                registro.valor
            )

        tabela = Table(
            title="Resultado das Agregações",
            box=box.HEAVY
        )

        tabela.add_column("Tipo")

        tabela.add_column("Média")

        tabela.add_column("Soma")

        tabela.add_column("Máximo")

        tabela.add_column("Mínimo")

        tabela.add_column("Qtd")

        for tipo, valores in (
            agregacoes.items()
        ):

            tabela.add_row(

                tipo,

                f"{np.mean(valores):.2f}",

                f"{np.sum(valores):.2f}",

                f"{np.max(valores):.2f}",

                f"{np.min(valores):.2f}",

                str(len(valores))
            )

        console.print(tabela)

    # =====================================================
    # ESTADOS
    # =====================================================

    def atualizar_estados(self):
        """
        Atualiza estados operacionais.

        Estados:
        - NORMAL;
        - ALERTA;
        - CRÍTICA;
        - SOBRECARGA.
        """

        UI.titulo(
            "ATUALIZAÇÃO DOS ESTADOS"
        )

        media_temp = self.calcular_media(
            self.vetor_temperaturas
        )

        media_consumo = self.calcular_media(
            self.vetor_consumo
        )

        # =================================================
        # TEMPERATURA
        # =================================================

        if media_temp >= 35:

            self.estado_colonia[
                "temperatura"
            ] = "CRÍTICA"

        elif media_temp >= 28:

            self.estado_colonia[
                "temperatura"
            ] = "ALERTA"

        else:

            self.estado_colonia[
                "temperatura"
            ] = "NORMAL"

        # =================================================
        # ENERGIA
        # =================================================

        if media_consumo >= 3000:

            self.estado_colonia[
                "energia"
            ] = "SOBRECARGA"

        elif media_consumo >= 1800:

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

        tabela.add_column(
            "Subsystem"
        )

        tabela.add_column(
            "Status"
        )

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
    # ESTABILIDADE
    # =====================================================

    def calcular_estabilidade_energetica(self):
        """
        Calcula índice de estabilidade energética.

        Fórmula:

        Quanto menor o desvio padrão,
        maior a estabilidade.
        """

        UI.titulo(
            "ESTABILIDADE ENERGÉTICA"
        )

        if self.vetor_consumo.size == 0:

            UI.warning(
                "Sem dados energéticos"
            )

            return

        media = np.mean(
            self.vetor_consumo
        )

        desvio = np.std(
            self.vetor_consumo
        )

        indice = max(
            0,
            100 - (
                (desvio / media) * 100
            )
        )

        painel = Panel.fit(

            (
                f"[bold green]"
                f"{indice:.2f}%"
                f"[/bold green]\n\n"
                f"Desvio: {desvio:.2f}"
            ),

            title="Índice de Estabilidade",

            border_style="green"
        )

        console.print(painel)

    # =====================================================
    # INGESTÃO
    # =====================================================

    def adicionar_registro(
        self,
        sensor_id: str,
        tipo: str,
        valor: float
    ):
        """
        Realiza ingestão operacional.

        Fluxo:
        - validação;
        - armazenamento;
        - vetorização.
        """

        UI.secao(
            "INGESTÃO DE TELEMETRIA"
        )

        registro = RegistroProcessado(

            sensor_id=sensor_id,

            tipo=tipo,

            valor=valor,

            timestamp=datetime.now()
        )

        if not self.validar_dados(
            registro
        ):

            UI.erro(
                "Registro descartado"
            )

            return

        self.dados_processados.append(
            registro
        )

        # =================================================
        # VETORES ESPECIALIZADOS
        # =================================================

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

        if "solar" in tipo:

            self.vetor_solar = np.append(
                self.vetor_solar,
                valor
            )

        if "eolica" in tipo:

            self.vetor_eolico = np.append(
                self.vetor_eolico,
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
    "TEMP-INT-03",
    "temperatura_interna",
    36.1
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

engine.adicionar_registro(
    "SOLAR-01",
    "geracao_solar",
    840
)

engine.adicionar_registro(
    "SOLAR-02",
    "geracao_solar",
    920
)

engine.adicionar_registro(
    "EOLICA-01",
    "geracao_eolica",
    430
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

# =========================================================
# ESTABILIDADE
# =========================================================

engine.calcular_estabilidade_energetica()

# =========================================================
# FINALIZAÇÃO
# =========================================================

UI.titulo(
    "PROCESSAMENTO FINALIZADO"
)