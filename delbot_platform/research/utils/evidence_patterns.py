# =====================================
# TECHNOLOGY PATTERNS
# =====================================

TECHNOLOGY_PATTERNS = {
    # -- Deep Learning: NLP & Transformers --
    "bert": [
        "bert", "indobert", "roberta", "distilbert",
        "sentence-bert", "sentence bert", "bertweet"
    ],
    "transformer": [
        "transformer", "vision transformer", "vit",
        "attention mechanism", "multi-head attention"
    ],
    "llm": [
        "llm", "large language model", "language model", "foundation model"
    ],
    "rag": [
        "rag", "retrieval augmented generation", "retrieval-augmented generation"
    ],
    "langchain": [
        "langchain", "lang chain", "llamaindex", "llama index"
    ],
    "fine_tuning": [
        "fine tuning", "fine-tuning", "finetuning",
        "lora", "qlora", "peft", "instruction tuning"
    ],
    "prompt_engineering": [
        "prompt engineering", "zero-shot", "zero shot",
        "few-shot", "few shot", "chain of thought", "chain-of-thought", "cot"
    ],
    "gpt": [
        "gpt", "gpt-4", "gpt-3", "chatgpt", "openai", "gpt4", "gpt3"
    ],
    "gemini": ["gemini"],
    "ollama": ["ollama"],
    # -- Deep Learning: Recurrent --
    "lstm": [
        "lstm", "long short term memory", "bi-lstm", "bilstm"
    ],
    "gru": ["gru", "gated recurrent unit"],
    # -- Computer Vision --
    "cnn": [
        "cnn", "convolutional neural network", "convolution neural network"
    ],
    "yolo": [
        "yolo", "yolov5", "yolov7", "yolov8", "yolov9", "yolov10", "yolov11"
    ],
    "resnet": ["resnet", "resnet50", "resnet101", "resnet152"],
    "mobilenet": ["mobilenet", "mobilenetv2", "mobilenetv3"],
    "vgg": ["vgg", "vgg16", "vgg19"],
    "efficientnet": [
        "efficientnet", "efficientnetb0", "efficientnetb4", "efficientnetb7"
    ],
    "sam": ["sam", "segment anything", "segment anything model"],
    "ocr": ["ocr", "optical character recognition", "tesseract", "easyocr"],
    "face_recognition": [
        "face recognition", "face detection", "face verification",
        "facial recognition", "pengenalan wajah"
    ],
    "object_detection": [
        "object detection", "deteksi objek", "bounding box", "instance segmentation"
    ],
    "image_classification": [
        "image classification", "klasifikasi gambar", "klasifikasi citra"
    ],
    # -- Classical ML --
    "random_forest": ["random forest"],
    "xgboost": ["xgboost", "xgb"],
    "decision_tree": ["decision tree", "pohon keputusan"],
    "svm": ["svm", "support vector machine"],
    "naive_bayes": ["naive bayes", "naive bayes", "naive bayesian"],
    "knn": ["knn", "k-nearest neighbor", "k nearest neighbor"],
    "kmeans": ["kmeans", "k-means", "k means clustering"],
    # -- ML Frameworks --
    "tensorflow": ["tensorflow", "tf"],
    "pytorch": ["pytorch", "torch"],
    "keras": ["keras"],
    "scikit_learn": ["scikit-learn", "sklearn", "scikit learn"],
    "huggingface": ["huggingface", "hugging face", "transformers library"],
    # -- MLOps & Deployment --
    "docker": ["docker", "container", "containerization", "dockerfile"],
    "kubernetes": ["kubernetes", "k8s", "orchestration"],
    "fastapi": ["fastapi", "fast api"],
    "flask": ["flask"],
    "streamlit": ["streamlit"],
    "mlflow": ["mlflow", "ml flow"],
    "airflow": ["airflow", "apache airflow"],
    "kafka": [
        "kafka", "apache kafka", "message broker", "message queue"
    ],
    # -- Web Backend --
    "laravel": ["laravel"],
    "django": ["django"],
    "spring": ["spring boot", "springboot", "spring framework"],
    "nodejs": ["nodejs", "node.js", "express", "expressjs"],
    "golang": ["golang", "go lang", "go programming"],
    "grpc": ["grpc", "grpc protocol", "protocol buffers", "protobuf"],
    "graphql": ["graphql", "graph ql"],
    # -- Web Frontend & Mobile --
    "react": ["react", "reactjs", "react.js"],
    "vue": ["vue", "vuejs", "vue.js"],
    "nextjs": ["nextjs", "next.js", "next js"],
    "angular": ["angular", "angularjs"],
    "flutter": ["flutter"],
    "react_native": ["react native", "react-native"],
    "kotlin": ["kotlin"],
    "swift": ["swift", "swiftui"],
    # -- Legacy Web --
    "php": ["php"],
    "java": ["java"],
    "python": ["python"],
    # -- Database --
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "mongodb": ["mongodb", "mongo"],
    "redis": ["redis"],
    "elasticsearch": ["elasticsearch", "elastic search"],
    "firebase": ["firebase", "firestore"],
    "sqlite": ["sqlite", "sqlite3"],
    # -- API & Architecture --
    "api": ["api", "rest api", "restful api", "rest"],
    "microservices": ["microservices", "microservice", "micro services"],
    "soa": ["soa", "service oriented architecture"],
    "web_service": ["web service", "web services"],
    "cqrs": ["cqrs", "command query responsibility segregation"],
    "event_driven": ["event driven", "event-driven", "eda"],
    # -- IoT & Embedded --
    "arduino": ["arduino"],
    "esp32": ["esp32", "esp8266", "nodemcu"],
    "raspberry_pi": ["raspberry pi", "raspberrypi", "raspi"],
    "mqtt": ["mqtt", "mqtt protocol"],
    "lora": ["lora", "lorawan", "lora wan"],
    "zigbee": ["zigbee", "zigbee protocol"],
    "modbus": ["modbus"],
    "plc": ["plc", "programmable logic controller"],
    "scada": ["scada", "supervisory control"],
    "pid": ["pid", "pid controller", "proportional integral derivative"],
    # -- Enterprise & ERP --
    "odoo": ["odoo"],
    "erp": ["erp", "enterprise resource planning"],
    "dashboard": ["dashboard"],
    "website": ["website", "web"],
    # -- Cloud & DevOps --
    "aws": ["aws", "amazon web services", "amazon s3", "ec2"],
    "gcp": ["gcp", "google cloud", "google cloud platform"],
    "azure": ["azure", "microsoft azure"],
    "ci_cd": [
        "ci/cd", "continuous integration", "continuous deployment",
        "github actions", "gitlab ci"
    ],
}


# =====================================
# METHODOLOGY PATTERNS
# =====================================
METHODOLOGY_PATTERNS = {
    # -- SDLC Models --
    "waterfall": ["waterfall"],
    "agile": ["agile", "scrum"],
    "prototype": ["prototype", "prototyping"],
    "spiral": ["spiral"],
    "rad": ["rad", "rapid application development"],
    "sdlc": ["sdlc"],
    # -- Testing --
    "black_box": ["black box", "blackbox testing"],
    "white_box": ["white box", "whitebox testing"],
    "tdd": ["tdd", "test driven development", "test-driven"],
    # -- Architecture --
    "mvc": ["mvc", "model view controller"],
    "design_pattern": ["design pattern", "pola desain"],
    "ddd": ["ddd", "domain driven design", "domain-driven design"],
    "ci_cd_method": ["ci/cd pipeline", "devops pipeline", "continuous integration"],
    "event_sourcing": ["event sourcing", "event-driven architecture", "event driven"],
    # -- ML Methodologies --
    "cross_validation": ["cross validation", "k-fold", "kfold"],
    "transfer_learning": ["transfer learning"],
    "crisp_dm": ["crisp-dm", "crisp dm", "cross industry standard process"],
    "benchmark": ["benchmark", "benchmarking"],
    "a_b_testing": ["a/b testing", "ab test", "split testing"],
    # -- Research Design --
    "qualitative": ["qualitative", "kualitatif"],
    "quantitative": ["quantitative", "kuantitatif"],
    "descriptive": ["deskriptif", "descriptive"],
    "experimental": ["eksperimental", "experimental research", "laboratory experiment"],
    "action_research": ["action research", "penelitian tindakan"],
    "case_study": ["case study", "studi kasus"],
    "design_thinking": ["design thinking"],
    # -- Engineering & Industry --
    "dmaic": ["dmaic", "six sigma dmaic"],
    "ahp": ["ahp", "analytical hierarchy process"],
    "topsis": ["topsis"],
    "rsm": ["rsm", "response surface methodology"],
    "simulation": ["simulasi", "simulation", "monte carlo"],
    # -- Modeling --
    "uml": ["uml", "unified modeling language"],
    "erd": ["erd", "entity relationship diagram", "entity relationship"],
    "bpmn": ["bpmn", "business process model", "business process notation"],
    "use_case": ["use case", "use-case diagram"],
}

# =====================================
# DOMAIN PATTERNS
# =====================================
DOMAIN_PATTERNS = {
    "academic_admission": ["penerimaan mahasiswa baru", "pmb", "spmb"],
    "information_system": ["sistem informasi"],
    "machine_learning": ["machine learning"],
    "deep_learning": ["deep learning"],
    "computer_vision": ["computer vision", "visi komputer"],
    "nlp": [
        "natural language processing", "nlp", "sentiment analysis",
        "text classification", "named entity recognition", "ner"
    ],
    "iot": ["internet of things", "iot", "smart home", "smart city"],
    "cyber_security": [
        "cyber security", "cybersecurity", "keamanan jaringan", "network security"
    ],
    "blockchain": ["blockchain", "smart contract"],
    "recommender_system": [
        "recommender system", "sistem rekomendasi",
        "collaborative filtering", "content based filtering"
    ],
    "generative_ai": [
        "generative ai", "generative model", "llm",
        "large language model", "text generation", "image generation"
    ],
    "data_science": ["data science", "data analytics", "big data", "data mining"],
    "cloud_computing": ["cloud computing", "cloud native", "serverless"],
    "supply_chain": ["supply chain", "logistik", "logistics"],
}


# =====================================
# DATASET PATTERNS
# =====================================
DATASET_PATTERNS = {
    # -- Classic CV Benchmarks --
    "mnist": ["mnist", "fashion-mnist"],
    "cifar": ["cifar", "cifar10", "cifar-10", "cifar-100"],
    "imagenet": ["imagenet"],
    "coco": ["coco", "ms coco"],
    "pascal_voc": ["pascal voc", "voc dataset"],
    # -- Cybersecurity --
    "kdd": ["kdd", "nsl-kdd", "kdd cup"],
    "unsw_nb15": ["unsw-nb15", "unsw nb15"],
    # -- Classic ML --
    "iris": ["iris", "iris dataset"],
    "uci": ["uci", "uci repository"],
    "kaggle": ["kaggle", "kaggle dataset"],
    # -- Indonesian NLP Datasets --
    "idner": ["idner", "indonesian ner dataset"],
    "indonlu": ["indonlu", "indo nlu"],
    "nusax": ["nusax", "nusa x"],
    "smsa": ["smsa", "sentiment indonesian"],
    "indosum": ["indosum", "indo sum"],
    # -- Social Media --
    "twitter_data": ["twitter data", "tweet dataset", "data tweet", "twitter api"],
    "news_dataset": ["news dataset", "data berita", "dataset berita"],
    # -- Medical --
    "chest_xray": ["chest x-ray", "chest xray", "chest radiograph"],
    "ecg_dataset": ["ecg", "electrocardiogram", "ekg"],
    # -- IoT / Time Series --
    "sensor_data": ["sensor data", "data sensor", "iot data"],
    "time_series": ["time series", "time-series", "data temporal", "data berkala"],
    "log_data": ["log data", "data log", "system log", "log sistem"],
    # -- Enterprise / Business --
    "academic_dataset": ["data mahasiswa", "data akademik", "data nilai", "data alumni"],
    "sales_dataset": ["data penjualan", "sales data"],
    "customer_dataset": ["data pelanggan", "customer data"],
    "inventory_dataset": ["data inventaris", "inventory data", "stok barang"],
    "hr_dataset": ["data pegawai", "data karyawan", "employee data"],
    "financial_dataset": ["data keuangan", "financial data", "data transaksi keuangan"],
}

# =====================================
# METRIC PATTERNS
# =====================================
METRIC_PATTERNS = {
    # -- Classification --
    "accuracy": ["accuracy", "akurasi"],
    "precision": ["precision", "presisi"],
    "recall": ["recall"],
    "f1_score": ["f1", "f1-score", "f1 score"],
    "auc": ["auc", "area under curve"],
    "roc": ["roc", "roc curve"],
    # -- Regression --
    "mae": ["mae", "mean absolute error"],
    "mse": ["mse", "mean squared error"],
    "rmse": ["rmse", "root mean squared error"],
    "r2": ["r2", "r-squared", "coefficient of determination"],
    # -- NLP --
    "bleu": ["bleu", "bleu score"],
    "rouge": ["rouge", "rouge score"],
    "meteor": ["meteor"],
    "perplexity": ["perplexity"],
    # -- Retrieval / Ranking --
    "map": ["map", "mean average precision"],
    "ndcg": ["ndcg", "normalized discounted cumulative gain"],
    "hit_rate": ["hit rate", "hit@k"],
    "mrr": ["mrr", "mean reciprocal rank"],
    # -- Speech --
    "wer": ["wer", "word error rate"],
    "cer": ["cer", "character error rate"],
    # -- Vision --
    "iou": ["iou", "intersection over union"],
    "dice": ["dice", "dice score", "dice coefficient"],
    "psnr": ["psnr", "peak signal to noise ratio"],
    "ssim": ["ssim", "structural similarity"],
    # -- Clustering --
    "silhouette_score": ["silhouette score", "silhouette"],
    "ari": ["ari", "adjusted rand index"],
    "nmi": ["nmi", "normalized mutual information"],
    # -- System Performance --
    "sus_score": ["sus", "system usability scale", "sus score"],
    "latency": ["latency", "latensi", "response time", "waktu respons"],
    "throughput": ["throughput"],
    "hallucination_rate": ["hallucination rate", "faithfulness", "tingkat halusinasi"],
}
