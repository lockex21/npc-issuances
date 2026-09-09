"""Offline regression checks for incremental case imports."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import build_npc_decisions_resolutions as importer


class IncrementalImportTests(unittest.TestCase):
    def test_new_only_preserves_old_source_without_cache_and_reserves_its_slug(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with (
                patch.object(importer, "ROOT", root),
                patch.object(importer, "DATA_DIR", root / "data"),
                patch.object(importer, "CACHE_DIR", root / "cache"),
                patch.object(importer, "CONTENT_DIR", root / "content"),
            ):
                config = importer.CORPORA["resolutions"]
                title = importer.build_display_title("NPC 25-001", "Example")
                slug = importer.core.slugify(title)
                old = importer.CaseRecord(
                    title=title, short_title="Example", reference_label="NPC 25-001",
                    source_url="http://privacy.gov.ph/old.pdf", source_tags_raw="Curated",
                    source_tags=["Curated"], issue_date="October 30, 2025",
                    issue_date_iso="2025-10-30", published_time=None, published_time_iso=None,
                    page_count=12, year="2025", slug=slug,
                    raw_text_path="cache/resolutions/text_raw/absent.md",
                    text_path="cache/resolutions/text/absent.txt",
                    markdown_path=f"content/resolutions/2025/{slug}.md", excerpt="Curated excerpt",
                )
                config.data_path.parent.mkdir(parents=True)
                config.data_path.write_text(json.dumps({"records": [old.as_dict()]}))
                old_page = root / old.markdown_path
                old_page.parent.mkdir(parents=True)
                old_page.write_text("Curated Markdown with [[laws/example|links]].\n")
                entries = [
                    importer.SourceEntry("NPC 25-001", "Example", "https://privacy.gov.ph/new.pdf", "", []),
                    # A scheme change must not turn an old PDF into a new document.
                    importer.SourceEntry("NPC 25-001", "Example", "https://privacy.gov.ph/old.pdf", "Changed", []),
                ]
                fetched = []

                def fetch(url):
                    fetched.append(url)
                    if url == config.mirror_url:
                        return "Markdown Content:\nRESOLUTIONS\n"
                    if url == importer.mirror_url(entries[0].source_url):
                        return "Number of Pages: 2\nMarkdown Content:\nResolution\n30 January 2026\nNew text.\n"
                    self.fail(f"Unexpected fetch of an existing source: {url}")

                with (
                    patch.object(importer, "parse_index_entries", return_value=entries),
                    patch.object(importer, "fetch_text_with_retries", side_effect=fetch),
                ):
                    records = importer.build_records(config, refresh=True, new_only=True)
                    self.assertEqual(len(records), 2)
                    preserved = next(record for record in records if record.source_url == old.source_url)
                    self.assertEqual(preserved.as_dict(), old.as_dict())
                    added = next(record for record in records if record is not preserved)
                    self.assertEqual(added.slug, slug + "-2")
                    self.assertNotEqual(added.markdown_path, old.markdown_path)
                    self.assertTrue((root / added.markdown_path).is_file())
                    self.assertEqual(old_page.read_text(), "Curated Markdown with [[laws/example|links]].\n")
                    self.assertEqual(len(fetched), 2)
                    self.assertFalse((root / old.raw_text_path).exists())

                    # A later index omitting the old document must retain it locally.
                    importer.write_json(config, records)
                    entries[:] = entries[:1]
                    fetched.clear()
                    rerun = importer.build_records(config, refresh=True, new_only=True)
                    self.assertEqual([record.as_dict() for record in rerun], [record.as_dict() for record in records])
                    self.assertEqual(fetched, [config.mirror_url])


if __name__ == "__main__":
    unittest.main()
