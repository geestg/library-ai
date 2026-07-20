from delbot_platform.document.parser.pdf_parser import PDFParser
from delbot_platform.document.chunking.chunker import ChunkBuilder


class DocumentPipeline:


    def __init__(self):

        self.parser=PDFParser()
        self.chunker=ChunkBuilder()



    def process(
        self,
        pdf:str,
    ):


        pages=self.parser.extract(
            pdf
        )


        chunks=self.chunker.build(
            pages
        )


        return {

            "pages":len(pages),

            "chunks":len(chunks),

            "data":chunks

        }
