from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from openpyxl import load_workbook


def cell_text(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def slugify(text: str) -> str:
    safe = []
    for ch in text.lower():
        if ch.isalnum():
            safe.append(ch)
        elif ch in {" ", "-", "_", "/"}:
            safe.append("-")
    slug = "".join(safe).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "item"


def workbook_to_items(source: Path) -> list[dict[str, object]]:
    workbook = load_workbook(source, data_only=True)
    sheet = workbook[workbook.sheetnames[0]]
    headers = [cell_text(cell.value) for cell in sheet[1]]

    items: list[dict[str, object]] = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if not any(cell_text(value) for value in row):
            continue

        values = dict(zip(headers, row))
        item = {
            "id": f"skill-{int(values['序号'])}",
            "order": int(values["序号"]),
            "name": cell_text(values["skill名称"]),
            "summary": cell_text(values["skill能力描述"]),
            "owner": cell_text(values["填写人"]),
            "package": cell_text(values["所属Skill包"]),
            "roles": cell_text(values["目标岗位/职能"]),
            "category": cell_text(values["类型"]),
            "mainstreamPriority": cell_text(values["主流媒体优先级"]),
            "emergingPriority": cell_text(values["新兴媒体优先级"]),
            "downloadUrl": "",
            "slug": slugify(cell_text(values["skill名称"])),
        }
        items.append(item)

    return items


def build_payload(source: Path) -> dict[str, object]:
    items = workbook_to_items(source)
    categories = sorted({item["category"] for item in items})
    packages = sorted({item["package"] for item in items})

    return {
        "meta": {
            "title": "行业 Skill 资源库",
            "sourceFile": source.name,
            "generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "totalSkills": len(items),
            "categories": categories,
            "packages": packages,
        },
        "items": items,
    }


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python sync_skills_from_excel.py <source.xlsx> <output.js>")
        return 1

    source = Path(sys.argv[1]).expanduser().resolve()
    output = Path(sys.argv[2]).expanduser().resolve()

    payload = build_payload(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "window.SKILL_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
