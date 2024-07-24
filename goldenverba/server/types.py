from pydantic import BaseModel
from enum import Enum


class QueryPayload(BaseModel):
    query: str


class ConversationItem(BaseModel):
    type: str
    content: str


class GeneratePayload(BaseModel):
    query: str
    context: str
    conversation: list[ConversationItem]


class SearchQueryPayload(BaseModel):
    query: str
    labels: list[str]
    page: int
    pageSize: int

class ChunksPayload(BaseModel):
    uuid: str
    page: int
    pageSize: int


class GetDocumentPayload(BaseModel):
    uuid: str

class GetVectorPayload(BaseModel):
    uuid: str
    showAll: bool


class ResetPayload(BaseModel):
    resetMode: str


class LoadPayload(BaseModel):
    reader: str
    chunker: str
    embedder: str
    fileBytes: list[str]
    fileNames: list[str]
    filePath: str
    document_type: str
    chunkUnits: int
    chunkOverlap: int


class ImportPayload(BaseModel):
    data: list
    textValues: list[str]
    config: dict    

class ConfigPayload(BaseModel):
    config: dict


class GetComponentPayload(BaseModel):
    component: str


class SetComponentPayload(BaseModel):
    component: str
    selected_component: str



# Import
    
class FileStatus(str, Enum):
    READY = "READY"
    STARTING = "STARTING"
    LOADING = "LOADING"
    CHUNKING = "CHUNKING"
    EMBEDDING = "EMBEDDING"
    INGESTING = "INGESTING"
    NER = "NER"
    EXTRACTION = "EXTRACTION"
    SUMMARIZING = "SUMMARIZING"
    DONE = "DONE"
    ERROR = "ERROR"

class ConfigSetting(BaseModel):
    type: str
    value: str | int
    description: str
    values: list[str]

class RAGComponentConfig(BaseModel):
    name: str
    variables: list[str]
    library: list[str]
    description: str
    config: dict[str, ConfigSetting]
    type: str
    available: bool

class RAGComponentClass(BaseModel):
    selected: str
    components: dict[str, RAGComponentConfig]

class StatusReport(BaseModel):
    fileID: str
    status: str
    message: str
    took: float

class FileConfig(BaseModel):
    fileID: str
    filename: str
    isURL: bool
    overwrite: bool
    extension: str
    source: str
    content: str
    labels: list[str]
    rag_config: dict[str, RAGComponentClass]
    file_size: int
    status: FileStatus
    status_report: dict

class ImportStreamPayload(BaseModel):
    fileMap: dict[str, FileConfig]




