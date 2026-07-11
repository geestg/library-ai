# =====================================
# TEMPORAL GAP DETECTOR
# =====================================

RECENT_YEAR_THRESHOLD = 1

LONG_SPAN_THRESHOLD = 5


def detect_temporal_gap(
    year_frequency: dict
):

    if not year_frequency:

        return [
            "Informasi tahun penelitian belum mencukupi untuk analisis tren temporal."
        ]

    years = sorted(

        int(year)

        for year in year_frequency.keys()

        if str(year).isdigit()
    )

    if not years:

        return [
            "Informasi tahun penelitian belum mencukupi untuk analisis tren temporal."
        ]

    gaps = []

    oldest_year = years[0]

    latest_year = years[-1]

    latest_count = year_frequency.get(
        str(latest_year),
        0
    )

    # =================================
    # RECENT RESEARCH
    # =================================

    if latest_count <= RECENT_YEAR_THRESHOLD:

        gaps.append(

            f"Jumlah penelitian pada tahun {latest_year} masih rendah sehingga peluang penelitian terbaru masih terbuka."
        )

    # =================================
    # MISSING YEARS
    # =================================

    for year in range(

        oldest_year,

        latest_year + 1

    ):

        if str(year) not in year_frequency:

            gaps.append(

                f"Tidak ditemukan penelitian pada tahun {year}, sehingga perkembangan pada periode tersebut belum terdokumentasi."
            )

    # =================================
    # LONG TIME SPAN
    # =================================

    if (

        latest_year - oldest_year

        >= LONG_SPAN_THRESHOLD

    ):

        gaps.append(

            f"Rentang penelitian ({oldest_year}-{latest_year}) cukup panjang sehingga diperlukan validasi terhadap perkembangan teknologi terbaru."
        )

    # =================================
    # TREND DECLINE
    # =================================

    if len(years) >= 2:

        previous_year = years[-2]

        previous_count = year_frequency.get(

            str(previous_year),

            0
        )

        if (

            previous_count > latest_count

            and

            latest_count <= RECENT_YEAR_THRESHOLD

        ):

            gaps.append(

                "Jumlah penelitian menunjukkan penurunan pada periode terbaru sehingga diperlukan eksplorasi lanjutan."
            )

    return gaps
