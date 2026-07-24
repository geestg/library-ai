# DELBot Architecture Migration Plan
Status: Accepted
Version: 1.0
Date: 2026-07-24

---

# Purpose

Dokumen ini menjadi source of truth arsitektur DELBot.

Seluruh migrasi repository harus mengacu ke dokumen ini.

Tidak boleh ada folder baru, service baru, atau pipeline baru yang dibuat
tanpa sesuai dengan arsitektur berikut.

---

# High Level Architecture

Frontend
    │
    ▼
Research API
    │
    ▼
Gateway
    │
    ▼
AI Runtime Layer
    │
    ▼
Storage Layer
    │
    ▼
Research Engine

---

# Core Modules

## frontend/

UI dan Dashboard.

Tidak mengetahui AI Runtime.

Tidak mengetahui Vector Database.

---

## gateway/

Gateway hanya melakukan routing.

Tidak boleh ada business logic.

Tanggung jawab:

- Chat
- Embedding
- Reranker
- Vision
- OCR
- Speech

---

## ai/

Seluruh AI Runtime.

Submodule:

- chat
- embedding
- reranker
- vision
- speech
- runtime
- providers
- launcher

---

## documents/

Pipeline dokumen.

Submodule:

- repository
- parser
- ocr
- layout
- section
- chunk
- metadata
- ingestion

---

## vectorstore/

Source of truth seluruh vector database.

Target implementasi:

- base.py
- repository.py
- qdrant/
- pgvector/
- milvus/

Tidak ada module lain yang boleh mengakses Qdrant secara langsung.

---

## knowledge/

Knowledge Layer.

Berisi:

- Knowledge Graph
- Entity
- Relation
- Citation
- Ontology

Knowledge menggunakan VectorRepository.

Knowledge bukan implementasi Vector Database.

---

## research/

Research Operating System.

Berisi:

- Workspace
- Session
- Planner
- Memory
- Pipeline
- Reasoning
- Citation Manager

---

## platform/

Platform Runtime.

Berisi:

- launcher
- runtime
- recovery
- controller
- monitor
- boot

---

# Source Of Truth

AI Runtime
    -> ai/

Gateway
    -> gateway/

Document Processing
    -> documents/

Vector Database
    -> vectorstore/

Knowledge
    -> knowledge/

Research
    -> research/

Platform
    -> platform/

---

# Transitional Modules

Masih dipertahankan selama proses migrasi.

Status:

- launcher/infinity.py
- ai/runtime/infinity.py
- knowledge/vector/*
- document/storage/*
- gateway/routers/v1/*

Seluruh modul di atas akan dihapus setelah migrasi selesai.

---

# Legacy Policy

Modul legacy:

- tidak menerima feature baru
- hanya menerima bugfix
- akan dihapus setelah seluruh dependency dipindahkan

---

# Engineering Rules

1. Repository First
2. Architecture First
3. Minimal Refactor
4. Backward Compatible
5. No Duplicate Responsibility
6. One Source Of Truth
7. Composition over Duplication

---

# Migration Phases

Phase 1
- Freeze Architecture
- Audit Dependency
- Tentukan Source Of Truth

Phase 2
- Migrasi AI Runtime
- Migrasi Gateway
- Migrasi VectorStore

Phase 3
- Migrasi Document Pipeline
- Migrasi Knowledge Layer

Phase 4
- Cleanup Legacy

Phase 5
- Production Hardening
