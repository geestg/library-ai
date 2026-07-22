from __future__ import annotations


import fitz

import numpy as np

from PIL import Image


from paddleocr import PaddleOCR



class OCRLoader:



    def __init__(self):

        self.ocr = PaddleOCR(
            lang="en",
            use_angle_cls=True
        )



    def load(
        self,
        path:str
    ):


        document = fitz.open(
            path
        )


        pages=[]



        for index,page in enumerate(document):


            pix = page.get_pixmap(
                dpi=200
            )


            image = Image.frombytes(
                "RGB",
                [
                    pix.width,
                    pix.height
                ],
                pix.samples
            )


            image_np=np.array(
                image
            )



            result=self.ocr.ocr(
                image_np,
                cls=True
            )



            texts=[]


            if result:

                for line in result:


                    if line:


                        for item in line:


                            texts.append(
                                item[1][0]
                            )



            text="\n".join(
                texts
            )


            if text.strip():


                pages.append(
                    {
                        "page":index+1,
                        "text":text
                    }
                )



        document.close()


        return pages
