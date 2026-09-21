import QtQuick
import qs.Commons
import qs.Ui

BarWidget {
  id: root
  moduleName: "org.yard.console"

  readonly property bool opened: panelLoader.item ? panelLoader.item.opened === true : false
  readonly property bool alarming: panelLoader.item ? panelLoader.item.alarming === true : false
  readonly property bool popoutSwitchClosing: panelLoader.item ? panelLoader.item.popoutSwitchClosing === true : false
  readonly property real openPanelIndicatorWidth: button.width
  readonly property real openPanelIndicatorHeight: Math.max(Style.space(10), Math.round(Style.bar.iconSlot * 0.55))

  function injectPanel() {
    var target = panelLoader.item
    if (!target) return
    if ("bar" in target) target.bar = root.bar
    if ("settings" in target) target.settings = root.settings
    if ("anchorItem" in target) target.anchorItem = button
    if ("hostWidget" in target) target.hostWidget = root
  }

  function open() { if (panelLoader.item) panelLoader.item.open() }
  function close() { if (panelLoader.item) panelLoader.item.close() }
  function togglePanel() { if (panelLoader.item) panelLoader.item.toggle() }
  function closeForPopoutSwitch() { if (panelLoader.item) panelLoader.item.closeForPopoutSwitch() }

  implicitWidth: button.implicitWidth
  implicitHeight: button.implicitHeight
  onBarChanged: injectPanel()
  onSettingsChanged: injectPanel()

  Loader {
    id: panelLoader
    active: true
    source: Qt.resolvedUrl("Panel.qml")
    visible: false
    onLoaded: {
      root.injectPanel()
      Qt.callLater(root.injectPanel)
    }
  }

  BarIconButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    text: "󱚣"
    slotSize: Style.bar.statusSlot
    active: root.alarming
    tooltipText: {
      var item = panelLoader.item
      if (!item || !item.fleetData) return root.alarming ? "YARD: Anomaly Detected" : "YARD: Beads Control Plane"
      var fd = item.fleetData
      var beadId = (fd.beads && fd.beads.inWork) ? fd.beads.inWork.id : "idle"
      var beadAdopt = (fd.beadsSystem) ? (fd.beadsSystem.adoptedRepos + "/" + fd.beadsSystem.totalRepos + " Beads") : ""
      return "YARD [" + beadAdopt + "] In-Work: " + beadId
    }
    onPressed: function(mouseButton) {
      if (mouseButton === Qt.LeftButton) root.togglePanel()
    }
  }
}
