"""Regressions for ambiguous law names in case citations."""

import unittest

from link_obsidian_connections import Linker


IRR_TARGET = "laws/implementing-rules-and-regulations-of-the-data-privacy-act-of-2012"


class IrrCitationTests(unittest.TestCase):
    def setUp(self):
        self.linker = Linker({}, {}, None)

    def test_building_code_irr_is_not_linked_even_in_a_dpa_case(self):
        facts = (
            "Complainant alleged that the Respondent is a regulatory body primarily "
            "responsible for the enforcement of the National Building Code of the "
            "Philippines (NBCP) pursuant to Presidential Decree No. 1096, as well as "
            "its Internal Rules and Regulations (IRR) and is charged with the duty "
            "of issuing building permits."
        )
        body = "This complaint concerns the Data Privacy Act.\n\n" + facts
        linked, _ = self.linker.link_body(body, "decisions/2025/example")
        self.assertIn(facts, linked)
        self.assertNotIn(IRR_TARGET, linked)
        self.assertIn("[[laws/data-privacy-act-of-2012|", linked)

    def test_unqualified_irr_sections_and_expansions_remain_unlinked(self):
        body = "Section 18 of the IRR. The Implementing Rules and Regulations apply."
        linked, count = self.linker.link_body(body, "decisions/2025/example")
        self.assertEqual(linked, body)
        self.assertEqual(count, 0)

    def test_explicit_dpa_irr_phrases_link_without_nested_wikilinks(self):
        for phrase in (
            "DPA IRR",
            "IRR of the DPA",
            "Implementing Rules and Regulations of the Data Privacy Act of 2012",
            "Implementing Rules and Regulations (IRR) of Republic Act No. 10173",
        ):
            with self.subTest(phrase=phrase):
                linked, count = self.linker.link_body(phrase, "decisions/2025/example")
                self.assertEqual(linked, f"[[{IRR_TARGET}|{phrase}]]")
                self.assertEqual(count, 1)
                self.assertEqual(self.linker.link_body(linked, "decisions/2025/example"), (linked, 0))

    def test_explicit_irr_section_is_not_mistaken_for_a_dpa_section(self):
        for phrase in ("Section 18 of the DPA IRR", "Section 18 of the IRR of the DPA"):
            with self.subTest(phrase=phrase):
                linked, count = self.linker.link_body(phrase, "decisions/2025/example")
                self.assertTrue(linked.startswith(f"[[{IRR_TARGET}#section-18"))
                self.assertTrue(linked.endswith(f"|{phrase}]]"))
                self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
