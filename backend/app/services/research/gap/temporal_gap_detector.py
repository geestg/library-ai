def detect_temporal_gap(
    year_frequency: dict
):

    gaps = []

    years = []

    for year in year_frequency.keys():

        try:

            years.append(
                int(year)
            )

        except Exception:
            pass

    if not years:

        return [

            "Informasi tahun penelitian belum mencukupi untuk analisis tren temporal."
        ]

    years.sort()

    latest_year = max(
        years
    )

    oldest_year = min(
        years
    )

    latest_count = year_frequency.get(
        str(latest_year),
        0
    )

    if latest_count <= 1:

        gaps.append(

            f"Jumlah penelitian pada tahun {latest_year} masih rendah sehingga terdapat peluang penelitian terbaru pada periode tersebut."
        )

    if (

        latest_year - oldest_year

    ) >= 4:

        gaps.append(

            f"Terdapat rentang waktu penelitian yang cukup panjang ({oldest_year}-{latest_year}) sehingga diperlukan validasi terhadap perkembangan teknologi terbaru."
        )

    return gaps