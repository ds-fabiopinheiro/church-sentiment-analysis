from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Optional

MIN_MEASURABLE_HEIGHT_PX = 64   # abaixo disso não medimos expressão
DETECTION_FLOOR_PX = 24         # abaixo disso nenhum motor detecta com confiança
K_MIN = 10                      # rostos mensuráveis por janela para emitir números
WINDOW_S = 30
TRECHO_AUSENTE = "(sem transcrição nesta janela)"   # marcador: não é trecho citado, o lint rejeita


@dataclass
class FaceObservation:
    """Uma observação de rosto em um quadro. Nunca contém vetor de identidade facial, id persistente ou recorte."""
    t: float
    x: int
    y: int
    w: int
    h: int
    conf: float
    yaw: Optional[float] = None
    pitch: Optional[float] = None
    p_smile: Optional[float] = None
    expressiveness: Optional[float] = None
    eyes_closed: Optional[bool] = None

    @property
    def measurable(self) -> bool:
        return self.h >= MIN_MEASURABLE_HEIGHT_PX

    @property
    def facing(self) -> Optional[bool]:
        if self.yaw is None or self.pitch is None:
            return None
        return abs(self.yaw) < 30 and abs(self.pitch) < 25


@dataclass
class WindowAggregate:
    culto: str
    fonte: str
    t_ini: float
    t_fim: float
    quadros: int
    quadros_com_plateia: int
    n_total: int
    n_mensuravel: int
    insuficiente: bool
    pct_voltados: Optional[float] = None
    pct_sorrindo: Optional[float] = None
    expressividade: Optional[float] = None
    pct_olhos_fechados: Optional[float] = None
    altura_mediana_px: Optional[float] = None

    def to_row(self) -> dict:
        return asdict(self)


@dataclass
class Segment:
    t_ini: float
    t_fim: float
    texto: str


@dataclass
class Moment:
    nome: str
    t_ini: float
    t_fim: float


@dataclass
class Event:
    tipo: str
    t_ini: float
    t_fim: float
    sinal: str
    magnitude_pp: float
    cobertura_min: int
    momento: str = ""


@dataclass
class Insight:
    minuto: str
    momento: str
    trecho: str
    texto: str
    sinais: list[str] = field(default_factory=list)
    evento: Optional[str] = None
