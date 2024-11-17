from typing import List, Optional
from pydantic import BaseModel

class Corpus(BaseModel):
    """ class Corpus 
    
    Attributes:
    list_documents: List[str] -> documents in the corpus
    nombre_documents: int -> number of documents in the corpus
    """
    list_documents: Optional[List[str]] = []
    
    @property
    def nombre_documents(self) -> int:
        return len(self.list_documents)
    
    def add_document(self, document: str) -> None:
        self.list_documents.append(document)