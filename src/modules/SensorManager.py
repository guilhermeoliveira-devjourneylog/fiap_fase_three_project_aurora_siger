from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
import random

# =========================================================
# RICH TERMINAL UI
# =========================================================

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule
from rich.text import Text
from rich.columns import Columns
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
# MODELO
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

        self.ultima_leitura: Optional[
            LeituraSensor
        ] = None

    # =====================================================
    # LEITURA
    # =====================================================

    def gerar_leitura(self) -> float:

        faixa = {

            TipoSensor.TEMPERATURA_INTERNA:
                (18, 32),

            TipoSensor.TEMPERATURA_EXTERNA:
                (-80, 40),

            TipoSensor.VELOCIDADE_VENTO:
                (0, 180),

            TipoSensor.GERACAO_SOLAR:
                (0, 1000),

            TipoSensor.GERACAO_EOLICA:
                (0, 700),

            TipoSensor.CONSUMO_ENERGETICO:
                (50, 1200),

            TipoSensor.ESTADO_MODULOS:
                (0, 100),

            TipoSensor.INTEGRIDADE_ESTRUTURAL:
                (0, 100)
        }

        minimo, maximo = faixa[self.tipo]

        return round(
            random.uniform(minimo, maximo),
            2
        )


# =========================================================
# SENSOR MANAGER
# =========================================================

class SensorManager:
    """
    Camada responsável pelo gerenciamento completo da
    infraestrutura sensorial da Colônia Aurora.

    Objetivos:
    ----------
    - registrar sensores operacionais;
    - coletar telemetria em tempo real;
    - validar leituras;
    - monitorar integridade dos sensores;
    - detectar falhas operacionais;
    - armazenar histórico de leituras;
    - emitir alertas automáticos.

    Fluxo Operacional:
    ------------------
    Registro de Sensores
            ↓
    Coleta de Dados
            ↓
    Validação Operacional
            ↓
    Monitoramento de Integridade
            ↓
    Geração de Alertas

    Estruturas Internas:
    --------------------
    sensores:
        Dicionário contendo todos os sensores ativos.

    historico:
        Lista com todas as leituras coletadas.

    alertas:
        Lista textual contendo alertas operacionais.

    Funcionalidades:
    ----------------
    registrar_sensor()
        Registra sensores na infraestrutura.

    coletar_dados()
        Realiza aquisição de telemetria.

    validar_dados()
        Verifica leituras fora da faixa operacional.

    monitorar_integridade()
        Exibe status operacional dos sensores.

    exibir_alertas()
        Mostra a central de alertas ativa.

    Características Técnicas:
    -------------------------
    - arquitetura orientada a objetos;
    - utilização de dataclasses;
    - enumeração tipada;
    - persistência em memória;
    - interface Rich para terminal;
    - monitoramento em tempo real;
    - validação operacional automatizada.

    Sensores Suportados:
    --------------------
    - temperatura interna;
    - temperatura externa;
    - velocidade do vento;
    - geração solar;
    - geração eólica;
    - consumo energético;
    - estado dos módulos;
    - integridade estrutural.

    Status Operacionais:
    --------------------
    ONLINE
        Sensor operando normalmente.

    OFFLINE
        Sensor sem comunicação.

    ALERTA
        Valor fora da faixa operacional.

    FALHA
        Sensor comprometido criticamente.
    """

    def __init__(self):

        self.sensores: Dict[
            str,
            Sensor
        ] = {}

        self.historico: List[
            LeituraSensor
        ] = []

        self.alertas: List[str] = []

        UI.titulo(
            "SENSOR MANAGER INICIALIZADO"
        )

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
        """
        Registra um novo sensor operacional.

        Parâmetros:
        -----------
        sensor_id:
            Identificador único do sensor.

        tipo:
            Tipo operacional do sensor.

        limite_min:
            Valor mínimo permitido.

        limite_max:
            Valor máximo permitido.

        Processo:
        ---------
        1. Instancia o sensor.
        2. Adiciona ao dicionário operacional.
        3. Exibe confirmação visual.
        """

        sensor = Sensor(
            sensor_id,
            tipo,
            limite_min,
            limite_max
        )

        self.sensores[sensor_id] = sensor

        tabela = Table(
            title="Novo Sensor Registrado",
            box=box.ROUNDED
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

        tabela.add_row(
            sensor_id,
            tipo.value,
            f"{limite_min} → {limite_max}"
        )

        console.print(tabela)

    # =====================================================
    # COLETA
    # =====================================================

    def coletar_dados(self):
        """
        Executa a coleta completa de telemetria.

        Funcionamento:
        ---------------
        - percorre todos os sensores registrados;
        - gera leituras simuladas;
        - cria objetos de telemetria;
        - atualiza histórico operacional;
        - armazena última leitura do sensor.

        Resultado:
        ----------
        Todas as leituras ficam disponíveis para:
        - validação;
        - processamento;
        - análise preditiva;
        - geração de alertas.
        """

        UI.titulo(
            "COLETA DE TELEMETRIA"
        )

        tabela = Table(
            title="Leituras dos Sensores",
            box=box.HEAVY_EDGE,
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
            "Valor",
            justify="right"
        )

        tabela.add_column(
            "Timestamp",
            style="green"
        )

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

            tabela.add_row(
                sensor.sensor_id,
                sensor.tipo.value,
                f"{valor:.2f}",
                leitura.timestamp.strftime(
                    "%H:%M:%S"
                )
            )

        console.print(tabela)

        UI.sucesso(
            "Coleta concluída"
        )

    # =====================================================
    # VALIDAÇÃO
    # =====================================================

    def validar_dados(self):
        """
        Valida todas as leituras operacionais.

        Regras:
        -------
        - compara leitura atual com limites definidos;
        - atualiza status do sensor;
        - registra alertas automáticos.

        Status possíveis:
        -----------------
        ONLINE:
            Valor dentro da faixa operacional.

        ALERTA:
            Valor fora da faixa permitida.
        """

        UI.titulo(
            "VALIDAÇÃO OPERACIONAL"
        )

        tabela = Table(
            title="Status dos Sensores",
            box=box.DOUBLE_EDGE,
            show_lines=True
        )

        tabela.add_column(
            "Sensor",
            style="cyan"
        )

        tabela.add_column(
            "Valor",
            justify="right"
        )

        tabela.add_column(
            "Faixa",
            style="yellow"
        )

        tabela.add_column(
            "Status",
            justify="center"
        )

        for sensor in self.sensores.values():

            leitura = sensor.ultima_leitura

            if leitura is None:
                continue

            valor = leitura.valor

            faixa = (
                f"{sensor.limite_min}"
                f" → "
                f"{sensor.limite_max}"
            )

            # =========================================
            # SENSOR OK
            # =========================================

            if sensor.limite_min <= valor <= sensor.limite_max:

                sensor.status = StatusSensor.ONLINE

                status = (
                    "[green]ONLINE[/green]"
                )

            # =========================================
            # ALERTA
            # =========================================

            else:

                sensor.status = StatusSensor.ALERTA

                status = (
                    "[red]ALERTA[/red]"
                )

                alerta = (
                    f"{sensor.sensor_id} "
                    f"fora da faixa operacional "
                    f"({valor:.2f})"
                )

                self.alertas.append(alerta)

            tabela.add_row(
                sensor.sensor_id,
                f"{valor:.2f}",
                faixa,
                status
            )

        console.print(tabela)

    # =====================================================
    # MONITORAMENTO
    # =====================================================

    def monitorar_integridade(self):
        """
        Exibe o monitoramento visual da integridade
        de todos os sensores registrados.

        Indicadores:
        ------------
        Verde:
            Sensor operacional.

        Amarelo:
            Sensor em alerta.

        Vermelho:
            Sensor offline.
        """

        UI.titulo(
            "MONITORAMENTO DA INTEGRIDADE"
        )

        paineis = []

        for sensor in self.sensores.values():

            leitura = sensor.ultima_leitura

            if leitura is None:

                sensor.status = StatusSensor.OFFLINE

            cor = "green"

            if sensor.status == StatusSensor.ALERTA:
                cor = "yellow"

            if sensor.status == StatusSensor.OFFLINE:
                cor = "red"

            painel = Panel(

                (
                    f"[bold cyan]{sensor.sensor_id}[/bold cyan]\n\n"

                    f"[white]Tipo:[/white] "
                    f"{sensor.tipo.value}\n"

                    f"[white]Status:[/white] "
                    f"[{cor}]"
                    f"{sensor.status.value}"
                    f"[/{cor}]\n"

                    f"[white]Último Valor:[/white] "
                    f"{leitura.valor if leitura else 'N/A'}"
                ),

                title="Sensor",
                border_style=cor,
                width=35

            )

            paineis.append(painel)

        console.print(
            Columns(paineis)
        )

    # =====================================================
    # ALERTAS
    # =====================================================

    def exibir_alertas(self):
        """
        Exibe todos os alertas operacionais ativos.

        Funcionamento:
        ---------------
        - apresenta alertas em tabela visual;
        - enumera ocorrências;
        - informa falhas operacionais detectadas.

        Caso não existam alertas:
        -------------------------
        Um painel verde de estabilidade é exibido.
        """

        UI.titulo(
            "CENTRAL DE ALERTAS"
        )

        if not self.alertas:

            painel = Panel.fit(
                "[bold green]"
                "Nenhum alerta ativo"
                "[/bold green]",
                border_style="green"
            )

            console.print(painel)

            return

        tabela = Table(
            title="Alertas Operacionais",
            box=box.HEAVY,
            show_lines=True
        )

        tabela.add_column(
            "ID",
            justify="center"
        )

        tabela.add_column(
            "Descrição",
            style="red"
        )

        for i, alerta in enumerate(
            self.alertas,
            start=1
        ):

            tabela.add_row(
                str(i),
                alerta
            )

        console.print(tabela)


# =========================================================
# INICIALIZAÇÃO
# =========================================================

UI.titulo(
    "SISTEMA AURORA - CAMADA SENSORIAL"
)

sensor_manager = SensorManager()

# =========================================================
# REGISTROS
# =========================================================

sensor_manager.registrar_sensor(
    "TEMP-INT-01",
    TipoSensor.TEMPERATURA_INTERNA,
    18,
    30
)

sensor_manager.registrar_sensor(
    "TEMP-EXT-01",
    TipoSensor.TEMPERATURA_EXTERNA,
    -100,
    50
)

sensor_manager.registrar_sensor(
    "VENTO-01",
    TipoSensor.VELOCIDADE_VENTO,
    0,
    150
)

sensor_manager.registrar_sensor(
    "SOLAR-01",
    TipoSensor.GERACAO_SOLAR,
    0,
    1000
)

sensor_manager.registrar_sensor(
    "EOLICA-01",
    TipoSensor.GERACAO_EOLICA,
    0,
    700
)

sensor_manager.registrar_sensor(
    "ENERGIA-01",
    TipoSensor.CONSUMO_ENERGETICO,
    100,
    1000
)

sensor_manager.registrar_sensor(
    "MODULO-01",
    TipoSensor.ESTADO_MODULOS,
    70,
    100
)

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

UI.titulo(
    "MONITORAMENTO FINALIZADO"
)