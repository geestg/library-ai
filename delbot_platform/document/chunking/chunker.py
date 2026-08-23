class ChunkBuilder:


    def build(
        self,
        pages:list[dict],
        size:int = 800,
    ):

        chunks=[]


        for page in pages:

            text = page["text"]

            if not text:
                continue


            words=text.split()

            for i in range(
                0,
                len(words),
                size
            ):

                chunk=" ".join(
                    words[i:i+size]
                )


                chunks.append(
                    {
                        "page":page["page"],
                        "text":chunk,
                    }
                )


        return chunks
