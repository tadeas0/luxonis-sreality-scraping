from dataclasses import dataclass


@dataclass
class Image:
    id: str
    url: str


@dataclass
class Estate:
    id: int
    sreality_id: int
    name: str
    images: list[Image]


@dataclass
class ImageCreationDTO:
    url: str


@dataclass
class EstateCreationDTO:
    sreality_id: int
    name: str
    images: list[ImageCreationDTO]
