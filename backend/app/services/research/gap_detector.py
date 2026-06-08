from collections import Counter


# =====================================
# HELPERS
# =====================================

def get_dominant_items(
    frequency_dict: dict,
    threshold: int = 3
):

    return [

        name

        for name, count

        in frequency_dict.items()

        if count >= threshold
    ]


def get_emerging_items(
    frequency_dict: dict
):

    return [

        name

        for name, count

        in frequency_dict.items()

        if count == 2
    ]


def get_rare_items(
    frequency_dict: dict
):

    return [

        name

        for name, count

        in frequency_dict.items()

        if count == 1
    ]


def unique_keep_order(items):

    seen = set()

    result = []

    for item in items:

        if item in seen:
            continue

        seen.add(item)

        result.append(item)

    return result


# =====================================
# GAP DETECTOR V3
# =====================================

def detect_research_gaps(
    evidence_matrix: dict
):

    technology_frequency = (
        evidence_matrix.get(
            "technology_frequency",
            {}
        )
    )

    methodology_frequency = (
        evidence_matrix.get(
            "methodology_frequency",
            {}
        )
    )

    domain_frequency = (
        evidence_matrix.get(
            "domain_frequency",
            {}
        )
    )

    dataset_frequency = (
        evidence_matrix.get(
            "dataset_frequency",
            {}
        )
    )

    evaluation_frequency = (
        evidence_matrix.get(
            "evaluation_frequency",
            {}
        )
    )

    year_frequency = (
        evidence_matrix.get(
            "year_frequency",
            {}
        )
    )

    # =================================
    # DOMINANT / EMERGING / RARE
    # =================================

    dominant_topics = []

    emerging_topics = []

    rare_topics = []

    all_frequencies = [

        technology_frequency,

        methodology_frequency,

        domain_frequency
    ]

    for frequency_dict in all_frequencies:

        dominant_topics.extend(

            get_dominant_items(
                frequency_dict
            )
        )

        emerging_topics.extend(

            get_emerging_items(
                frequency_dict
            )
        )

        rare_topics.extend(

            get_rare_items(
                frequency_dict
            )
        )

    dominant_topics = unique_keep_order(
        dominant_topics
    )

    emerging_topics = unique_keep_order(
        emerging_topics
    )

    rare_topics = unique_keep_order(
        rare_topics
    )

    # =================================
    # METHOD GAP
    # =================================

    method_gap = []

    if methodology_frequency:

        sorted_methods = sorted(

            methodology_frequency.items(),

            key=lambda x: x[1],

            reverse=True
        )

        dominant_method = (
            sorted_methods[0][0]
        )

        for method, count in sorted_methods[1:]:

            if count <= 1:

                method_gap.append(

                    f"Metodologi '{method}' masih jarang digunakan dibandingkan metodologi dominan '{dominant_method}'."
                )

    else:

        method_gap.append(

            "Informasi metodologi penelitian belum mencukupi untuk dianalisis."
        )

    # =================================
    # DATASET GAP
    # =================================

    dataset_gap = []

    if dataset_frequency:

        sorted_datasets = sorted(

            dataset_frequency.items(),

            key=lambda x: x[1],

            reverse=True
        )

        dominant_dataset = (
            sorted_datasets[0][0]
        )

        for dataset, count in sorted_datasets:

            if count == 1:

                dataset_gap.append(

                    f"Dataset '{dataset}' masih sangat sedikit digunakan dibandingkan dataset dominan '{dominant_dataset}'."
                )

    else:

        dataset_gap.append(

            "Bukti penggunaan dataset masih sangat terbatas."
        )

    # =================================
    # TEMPORAL GAP
    # =================================

    temporal_gap = []

    years = []

    for year in year_frequency.keys():

        try:

            years.append(
                int(year)
            )

        except Exception:
            pass

    if years:

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

            temporal_gap.append(

                f"Jumlah penelitian pada tahun {latest_year} masih rendah sehingga terdapat peluang penelitian terbaru pada periode tersebut."
            )

        if (
            latest_year - oldest_year
        ) >= 4:

            temporal_gap.append(

                f"Terdapat rentang waktu penelitian yang cukup panjang ({oldest_year}-{latest_year}) sehingga diperlukan validasi terhadap perkembangan teknologi terbaru."
            )

    else:

        temporal_gap.append(

            "Informasi tahun penelitian belum mencukupi untuk analisis tren temporal."
        )

    # =================================
    # EVALUATION GAP
    # =================================

    evaluation_gap = []

    if not evaluation_frequency:

        evaluation_gap.append(

            "Sebagian besar penelitian tidak menyebutkan metrik evaluasi secara eksplisit."
        )

    else:

        metric_count = len(
            evaluation_frequency
        )

        if metric_count <= 2:

            evaluation_gap.append(

                "Variasi metrik evaluasi masih terbatas sehingga peluang evaluasi yang lebih komprehensif masih terbuka."
            )

        metric_names = {

            metric.lower()

            for metric

            in evaluation_frequency.keys()
        }

        if (

            "accuracy" in metric_names

            and len(metric_names) == 1

        ):

            evaluation_gap.append(

                "Mayoritas penelitian hanya menggunakan Accuracy tanpa metrik tambahan seperti Precision, Recall, atau F1-Score."
            )

    # =================================
    # NOVELTY OPPORTUNITIES
    # =================================

    novelty_opportunities = []

    for topic in rare_topics:

        novelty_opportunities.append(

            f"Eksplorasi lebih lanjut pada topik '{topic}' berpotensi menghasilkan kontribusi penelitian yang lebih baru dibandingkan area yang sudah dominan."
        )

    for dataset, count in dataset_frequency.items():

        if count == 1:

            novelty_opportunities.append(

                f"Penggunaan dataset '{dataset}' dapat menjadi peluang novelty karena masih jarang ditemukan."
            )

    if emerging_topics:

        novelty_opportunities.append(

            f"Kombinasi topik emerging seperti {', '.join(emerging_topics[:3])} berpotensi menghasilkan kontribusi penelitian yang lebih unik."
        )

    novelty_opportunities = unique_keep_order(
        novelty_opportunities
    )

    # =================================
    # GAP SCORE
    # =================================

    gap_score = min(

        100,

        (
            len(method_gap) * 10
            +
            len(dataset_gap) * 10
            +
            len(temporal_gap) * 15
            +
            len(evaluation_gap) * 20
        )
    )

    # =================================
    # DEBUG
    # =================================

    print("\n")
    print("=" * 80)
    print("GAP DETECTOR V3")
    print("=" * 80)

    print(
        "DOMINANT:",
        dominant_topics
    )

    print(
        "EMERGING:",
        emerging_topics
    )

    print(
        "RARE:",
        rare_topics
    )

    print(
        "METHOD GAP:",
        method_gap
    )

    print(
        "DATASET GAP:",
        dataset_gap
    )

    print(
        "TEMPORAL GAP:",
        temporal_gap
    )

    print(
        "EVALUATION GAP:",
        evaluation_gap
    )

    print(
        "NOVELTY:",
        novelty_opportunities
    )

    print(
        "GAP SCORE:",
        gap_score
    )

    # =================================
    # RETURN
    # =================================

    return {

        "dominant_topics":
        dominant_topics,

        "emerging_topics":
        emerging_topics,

        "rare_topics":
        rare_topics,

        "method_gap":
        method_gap,

        "dataset_gap":
        dataset_gap,

        "temporal_gap":
        temporal_gap,

        "evaluation_gap":
        evaluation_gap,

        "novelty_opportunities":
        novelty_opportunities,

        "gap_score":
        gap_score
    }