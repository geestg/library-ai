from __future__ import annotations

from pathlib import Path

from tools.architecture.pipeline import ArchitecturePipeline


def write(
    root: Path,
    relative: str,
    content: str,
) -> None:

    file = root / relative

    file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file.write_text(
        content,
        encoding="utf-8",
    )


def test_pipeline_without_cycle(
    tmp_path: Path,
) -> None:

    project = tmp_path / "sample"

    write(
        project,
        "__init__.py",
        "",
    )

    write(
        project,
        "a.py",
        "import sample.b\n",
    )

    write(
        project,
        "b.py",
        "",
    )

    report = ArchitecturePipeline().analyze(
        project,
    )

    assert len(report.dependency.modules) == 3
    assert len(report.circular.cycles) == 0
    assert len(report.metrics.modules) == 3
    assert len(report.layer.violations) == 0


def test_pipeline_with_cycle(
    tmp_path: Path,
) -> None:

    project = tmp_path / "sample"

    write(
        project,
        "__init__.py",
        "",
    )

    write(
        project,
        "a.py",
        "import sample.b\n",
    )

    write(
        project,
        "b.py",
        "import sample.a\n",
    )

    report = ArchitecturePipeline().analyze(
        project,
    )

    assert len(report.circular.cycles) == 1


def test_pipeline_layer_violation(
    tmp_path: Path,
) -> None:

    project = tmp_path / "sample"

    write(
        project,
        "__init__.py",
        "",
    )

    write(
        project,
        "api.py",
        "import sample.domain\n",
    )

    write(
        project,
        "domain.py",
        "",
    )

    report = ArchitecturePipeline().analyze(
        project,
        module_layers={
            "sample.api": "api",
            "sample.domain": "domain",
        },
        allowed_dependencies={
            "api": set(),
            "domain": set(),
        },
    )

    assert len(report.layer.violations) == 1
