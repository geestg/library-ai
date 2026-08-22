from __future__ import annotations

from app.services.research.gap.gap_utils import (
    DOMINANT_THRESHOLD, RECENT_YEAR_THRESHOLD, LONG_SPAN_THRESHOLD,
    get_dominant_items, get_emerging_items, get_rare_items,
    get_top_item, get_sorted_items, unique_keep_order
)

def detect_dominant_topics(tech_freq, method_freq, domain_freq) -> list:
    dominant_topics = []
    for freq in [tech_freq, method_freq, domain_freq]:
        dominant_topics.extend(get_dominant_items(freq))
    return unique_keep_order(dominant_topics)

def detect_emerging_topics(tech_freq, method_freq, domain_freq) -> list:
    emerging_topics = []
    for freq in [tech_freq, method_freq, domain_freq]:
        emerging_topics.extend(get_emerging_items(freq))
    return unique_keep_order(emerging_topics)

def detect_rare_topics(tech_freq, method_freq, domain_freq) -> list:
    rare_topics = []
    for freq in [tech_freq, method_freq, domain_freq]:
        rare_topics.extend(get_rare_items(freq))
    return unique_keep_order(rare_topics)

def detect_method_gap(methodology_frequency) -> list:
    if not methodology_frequency:
        return ["Informasi metodologi penelitian belum mencukupi untuk dianalisis."]
        
    sorted_methods = get_sorted_items(methodology_frequency)
    top_method = get_top_item(methodology_frequency)
    
    if top_method is None:
        return ["Informasi metodologi penelitian belum mencukupi untuk dianalisis."]
        
    dominant_count = top_method[1]
    gaps = []
    
    if dominant_count < DOMINANT_THRESHOLD:
        gaps.append(
            "Belum terdapat metodologi yang benar-benar dominan sehingga masih terbuka peluang eksplorasi berbagai pendekatan penelitian."
        )
        
    for method, count in sorted_methods:
        if count == 1:
            gaps.append(
                f"Metodologi '{method}' masih sangat jarang digunakan sehingga memiliki peluang untuk dieksplorasi lebih lanjut."
            )      
    return gaps


def detect_dataset_gap(dataset_frequency) -> list:
    if not dataset_frequency:
        return ["Bukti penggunaan dataset masih sangat terbatas."]
        
    sorted_datasets = get_sorted_items(dataset_frequency)
    top_dataset = get_top_item(dataset_frequency)
    gaps = []
    
    if top_dataset is None or top_dataset[1] < DOMINANT_THRESHOLD:
        gaps.append(
            "Belum terdapat dataset yang benar-benar dominan sehingga eksplorasi dataset alternatif masih sangat terbuka."
        )
        
    for dataset, count in sorted_datasets:
        if count == 1:
            gaps.append(
                f"Dataset '{dataset}' masih sangat jarang digunakan sehingga memiliki peluang penelitian lebih lanjut."
            )
            
    return gaps


def detect_temporal_gap(year_frequency: dict) -> list:
    if not year_frequency:
        return ["Informasi tahun penelitian belum mencukupi untuk analisis tren temporal."]
        
    years = sorted(int(year) for year in year_frequency.keys() if str(year).isdigit())
    if not years:
        return ["Informasi tahun penelitian belum mencukupi untuk analisis tren temporal."]
        
    gaps = []
    oldest_year = years[0]
    latest_year = years[-1]
    latest_count = year_frequency.get(str(latest_year), 0)
    
    if latest_count <= RECENT_YEAR_THRESHOLD:
        gaps.append(
            f"Jumlah penelitian pada tahun {latest_year} masih rendah sehingga peluang penelitian terbaru masih terbuka."
        )
        
    for year in range(oldest_year, latest_year + 1):
        if str(year) not in year_frequency:
            gaps.append(
                f"Tidak ditemukan penelitian pada tahun {year}, sehingga perkembangan pada periode tersebut belum terdokumentasi."
            )
            
    if latest_year - oldest_year >= LONG_SPAN_THRESHOLD:
        gaps.append(
            f"Rentang penelitian ({oldest_year}-{latest_year}) cukup panjang sehingga diperlukan validasi terhadap perkembangan teknologi terbaru."
        )
        
    if len(years) >= 2:
        previous_year = years[-2]
        previous_count = year_frequency.get(str(previous_year), 0)
        if previous_count > latest_count and latest_count <= RECENT_YEAR_THRESHOLD:
            gaps.append(
                "Jumlah penelitian menunjukkan penurunan pada periode terbaru sehingga diperlukan eksplorasi lanjutan."
            )
    return gaps

def detect_evaluation_gap(evaluation_frequency: dict) -> list:
    gaps = []
    if not evaluation_frequency:
        return ["Sebagian besar penelitian tidak menyebutkan metrik evaluasi secara eksplisit."]
        
    metric_count = len(evaluation_frequency)
    if metric_count <= 2:
        gaps.append(
            "Variasi metrik evaluasi masih terbatas sehingga peluang evaluasi yang lebih komprehensif masih terbuka."
        )
        
    metric_names = {metric.lower() for metric in evaluation_frequency.keys()}
    if "accuracy" in metric_names and len(metric_names) == 1:
        gaps.append(
            "Mayoritas penelitian hanya menggunakan Accuracy tanpa metrik tambahan seperti Precision, Recall, atau F1-Score."
        )
    return gaps


def detect_novelty_opportunities(rare_topics, emerging_topics, dataset_frequency) -> list:
    novelty = []
    for topic in rare_topics:
        novelty.append(
            f"Topik '{topic}' masih sangat jarang diteliti sehingga berpotensi menjadi kontribusi penelitian yang lebih baru."
        )
        
    for dataset, count in dataset_frequency.items():
        if count == 1:
            novelty.append(
                f"Pemanfaatan dataset '{dataset}' masih sangat terbatas sehingga layak dieksplorasi lebih lanjut."
            )
            
    if emerging_topics:
        novelty.append(
            "Kombinasi topik emerging " + ", ".join(emerging_topics[:5]) + " memiliki potensi menghasilkan penelitian yang lebih inovatif."
        )
        
    if not novelty:
        novelty.append(
            "Belum ditemukan peluang novelty yang kuat berdasarkan evidence penelitian yang tersedia."
        )
        
    return unique_keep_order(novelty)


def calculate_gap_score(method_gap, dataset_gap, temporal_gap, evaluation_gap) -> int:
    return min(
        100,
        (
            len(method_gap) * 10
            + len(dataset_gap) * 10
            + len(temporal_gap) * 15
            + len(evaluation_gap) * 20
        )
    )
