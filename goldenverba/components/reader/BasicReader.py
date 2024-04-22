import base64
import json
from datetime import datetime
import time
import io

from wasabi import msg

from goldenverba.components.document import Document
from goldenverba.components.interfaces import Reader
from goldenverba.components.types import FileData

try:
    from pypdf import PdfReader
except Exception:
    msg.warn("pypdf not installed, your base installation might be corrupted.")


class BasicReader(Reader):
    """
    The BasicReader reads .txt, .md, .mdx, .json and .pdf files. 
    """

    def __init__(self):
        super().__init__()
        self.name = "BasicReader"
        self.description = "Use this light-weight reader for normal text, PDF, markdown, and json files."
        self.requires_library = ["pypdf"]

    def load(
        self,
        fileData: list[FileData],
        config: dict
    ) -> tuple[list[Document], list[str]]:

        start_time = time.time()  # Start timing
        documents = []
        logging = []
        logging.append(["INFO",f"Starting loading in {len(fileData)} files"])

        for _config in self.config:
            if _config in config and self.config[_config] != config[_config]:
                msg.info(f"Updating BasicReader Config {_config} : {self.config[_config]} -> {config[_config]}")
                logging.append(["INFO",f"Updating BasicReader Config {_config} : {self.config[_config]} -> {config[_config]}"])
                self.config[_config] = config[_config]

        for file in fileData:
            msg.info(f"Loading in {file.filename}")
            logging.append(["INFO",f"Loading in {file.filename}"])

            decoded_bytes = base64.b64decode(file.content)

            if file.extension in ["txt","md","mdx"]:
                try:
                    original_text = decoded_bytes.decode("utf-8")
                    document = Document(
                        name=file.filename,
                        text=original_text,
                        type=self.config["document_type"],
                        timestamp=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                        reader=self.name,
                    )
                    documents.append(document)

                except Exception as e:
                    msg.warn(f"Failed to load {file.filename} : {str(e)}")
                    logging.append(["WARNING",f"Failed to load {file.filename} : {str(e)}"])

            elif file.extension == "json":
                try:
                    decoded_bytes = base64.b64decode(file.content)
                    original_text = decoded_bytes.decode("utf-8")
                    json_obj = json.loads(original_text)
                    document = Document.from_json(json_obj)
                    documents.append(document)

                except Exception as e:
                    msg.warn(f"Failed to load {file.filename} : {str(e)}")
                    logging.append(["WARNING",f"Failed to load {file.filename} : {str(e)}"])

            elif file.extension == "pdf":
                try:
                    pdf_bytes = io.BytesIO(base64.b64decode(file.content))

                    full_text = ""
                    reader = PdfReader(pdf_bytes)

                    for page in reader.pages:
                        full_text += page.extract_text() + "\n\n"

                    document = Document(
                            name=file.filename,
                            text=full_text,
                            type=self.config["document_type"],
                            timestamp=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                            reader=self.name,
                        )
                    documents.append(document)
                except Exception as e:
                    msg.warn(f"Failed to load {file.filename} : {str(e)}")
                    logging.append(["WARNING",f"Failed to load {file.filename} : {str(e)}"])
        
            else:
                msg.warn(f"{file.filename} with extension {file.extension} not supported by BasicReader.")
                logging.append(["WARNING",f"{file.filename} with extension {file.extension} not supported by BasicReader."])


        elapsed_time = round(time.time() - start_time , 2) # Calculate elapsed time
        msg.good(f"Loaded {len(documents)} documents in {elapsed_time}s")
        logging.append(["SUCCESS",f"Loaded {len(documents)} documents in {elapsed_time}s"])

        return documents, logging

   