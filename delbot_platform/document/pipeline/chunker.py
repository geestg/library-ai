from __future__ import annotations



class DocumentChunker:


    def __init__(
        self,
        size:int=500,
    ):

        self.size=size



    def chunk(
        self,
        pages:list,
    ):


        chunks=[]


        for page in pages:


            text=page["text"]


            words=text.split()


            for i in range(
                0,
                len(words),
                self.size
            ):

                chunk=" ".join(
                    words[i:i+self.size]
                )


                if chunk.strip():

                    chunks.append(
                        {
                            "page":page["page"],
                            "text":chunk,
                        }
                    )


        return chunks
