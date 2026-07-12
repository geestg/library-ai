def build_method_summary(
    sorted_methods: list
):

    dominant_method = (
        sorted_methods[0][0]
    )

    return f"""
Metode yang paling sering muncul
dalam hasil retrieval adalah
{dominant_method}.

Perbandingan dilakukan berdasarkan
frekuensi kemunculan, kompleksitas,
interpretabilitas, kelebihan,
kekurangan, dan skenario penggunaan.
""".strip()

