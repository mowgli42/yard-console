#!/usr/bin/env python3
"""
Test suite for YARD Control Plane Omarchy plugin.
Verifies manifest compliance, yard-status CLI JSON output,
YardModel parsing logic, and Quickshell component contracts.
"""

import json
import os
import subprocess
import unittest
from pathlib import Path

PLUGIN_DIR = Path(__file__).resolve().parent.parent
MANIFEST_PATH = PLUGIN_DIR / "manifest.json"
STATUS_BIN = PLUGIN_DIR / "bin" / "yard-status"


class OmarchyPluginVerificationTests(unittest.TestCase):
    def test_omarchy_plugin_validate_cli(self):
        """Runs omarchy plugin validate CLI against plugin directory."""
        res = subprocess.run(
            ["omarchy", "plugin", "validate", str(PLUGIN_DIR)],
            capture_output=True,
            text=True
        )
        self.assertEqual(
            res.returncode, 0,
            f"omarchy plugin validate failed:\n{res.stderr}\n{res.stdout}"
        )

    def test_manifest_structure_and_types(self):
        """Validates all required fields in manifest.json according to Omarchy plugin spec."""
        self.assertTrue(MANIFEST_PATH.is_file(), "manifest.json missing")
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        self.assertEqual(manifest.get("schemaVersion"), 1)
        self.assertEqual(manifest.get("id"), "org.yard.console")
        self.assertFalse(
            manifest["id"].startswith("omarchy."),
            "Third-party plugin ID must not use the reserved omarchy.* namespace"
        )
        self.assertIn("bar-widget", manifest.get("kinds", []))
        self.assertIn("barWidget", manifest.get("entryPoints", {}))

        bar_widget_ep = manifest["entryPoints"]["barWidget"]
        self.assertTrue(
            (PLUGIN_DIR / bar_widget_ep).is_file(),
            f"Entry point file {bar_widget_ep} does not exist"
        )

        bar_widget_meta = manifest.get("barWidget", {})
        self.assertEqual(bar_widget_meta.get("category"), "AI")
        self.assertIn(bar_widget_meta.get("defaultSection"), ["left", "center", "right"])

    def test_status_cli_executable_and_json_schema(self):
        """Verifies bin/yard-status executes cleanly and returns required JSON structure."""
        self.assertTrue(STATUS_BIN.is_file(), "bin/yard-status missing")
        self.assertTrue(os.access(STATUS_BIN, os.X_OK), "bin/yard-status not executable")

        res = subprocess.run([str(STATUS_BIN)], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"bin/yard-status failed:\n{res.stderr}")

        data = json.loads(res.stdout)
        self.assertEqual(data.get("version"), 1)
        self.assertIn("fleet", data)
        self.assertIn("activeCrews", data["fleet"])
        self.assertIn("beads", data)
        self.assertIn("beadsSystem", data)
        self.assertIn("allProjects", data)

        sys_info = data["beadsSystem"]
        self.assertIn("installed", sys_info)
        self.assertIn("adoptedRepos", sys_info)
        self.assertIn("totalRepos", sys_info)
        self.assertIn("adoptionPercent", sys_info)

    def test_qml_files_reference_valid_module_name(self):
        """Ensures QML files declare the exact moduleName matching manifest id."""
        manifest_id = "org.yard.console"
        for qml_name in ["BarWidget.qml", "Panel.qml"]:
            qml_path = PLUGIN_DIR / qml_name
            self.assertTrue(qml_path.is_file(), f"{qml_name} not found")
            content = qml_path.read_text(encoding="utf-8")
            self.assertIn(
                f'moduleName: "{manifest_id}"',
                content,
                f"{qml_name} does not match manifest ID {manifest_id}"
            )

    def test_keyboard_panel_contract(self):
        """Ensures Panel.qml implements KeyboardPanel and PanelKeyCatcher navigation."""
        panel_content = (PLUGIN_DIR / "Panel.qml").read_text(encoding="utf-8")
        self.assertIn("KeyboardPanel {", panel_content)
        self.assertIn("PanelKeyCatcher {", panel_content)
        self.assertIn("switchPanel", panel_content)
        self.assertIn("barIdentity", panel_content)


    def test_web_console_coexistence(self):
        """Ensures index.html exists alongside plugin files for HUD launcher."""
        index_html = PLUGIN_DIR / "index.html"
        self.assertTrue(index_html.is_file(), "index.html missing from plugin repo root")
        content = index_html.read_text(encoding="utf-8")
        self.assertIn("YARD", content)


if __name__ == "__main__":
    unittest.main()
