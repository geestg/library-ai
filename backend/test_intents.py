import sys
sys.path.insert(0, r'd:\DEL\library-ai\backend')
from app.orchestration.intent_classifier import classify_intent

tests = [
    # title_generation
    ("ide ta untuk informatika", "title_generation"),
    ("skripsi bidang LLM untuk si", "title_generation"),
    ("mau skripsi tentang iot", "title_generation"),
    ("cari judul penelitian", "title_generation"),
    ("thesis topic deep learning", "title_generation"),
    ("rekomendasikan topik trpl", "title_generation"),
    # methodology_comparison
    ("bandingkan CNN vs BERT", "methodology_comparison"),
    ("perbandingan YOLO dan ResNet", "methodology_comparison"),
    ("mana yang lebih baik LSTM atau GRU", "methodology_comparison"),
    # topic_exploration
    ("tren riset AI 2025", "topic_exploration"),
    ("topik populer informatika", "topic_exploration"),
    ("penelitian terkini NLP", "topic_exploration"),
    # research_gap
    ("celah penelitian NLP", "research_gap"),
    ("research gap computer vision", "research_gap"),
    ("kebaruan penelitian iot", "research_gap"),
    # literature
    ("tinjauan pustaka computer vision", "literature"),
    ("kajian literatur deep learning", "literature"),
    # methodology
    ("metode penelitian apa yang cocok", "methodology"),
    ("alur penelitian untuk skripsi AI", "methodology"),
    # technical
    ("fine-tuning llm dengan lora", "technical"),
    ("esp32 iot monitoring suhu", "technical"),
    ("yolov8 object detection", "technical"),
    ("langchain rag application", "technical"),
]

print("INTENT CLASSIFIER TEST")
print("=" * 65)
passed = 0
failed = 0
for query, expected in tests:
    result = classify_intent(query)
    status = "PASS" if result == expected else "FAIL"
    if status == "PASS":
        passed += 1
    else:
        failed += 1
    mark = "V" if status == "PASS" else "X"
    print(f"[{mark}] [{status}] \"{query}\"")
    if status == "FAIL":
        print(f"       Expected: {expected}, Got: {result}")

print("=" * 65)
print(f"Result: {passed}/{len(tests)} PASS | {failed} FAIL")
