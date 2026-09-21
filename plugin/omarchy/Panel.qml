import QtQuick
import QtQuick.Controls
import Quickshell
import Quickshell.Io
import qs.Commons
import qs.Ui
import "YardModel.js" as YardModel

Panel {
  id: root
  moduleName: "omarchy.yard-console"
  ipcTarget: "omarchy.yard-console"
  manageIpc: false

  property var anchorItem: null
  property var hostWidget: null

  readonly property color foreground: bar ? bar.foreground : Color.foreground
  readonly property color urgent: bar ? bar.urgent : Color.urgent
  readonly property color dim: Qt.darker(foreground, 1.55)
  readonly property string fontFamily: bar ? bar.fontFamily : Style.font.family

  property var fleetData: null
  readonly property bool alarming: fleetData && fleetData.fleet ? fleetData.fleet.alarming === true : false

  readonly property string statusScriptPath: decodeURIComponent(String(Qt.resolvedUrl("bin/yard-status")).replace(/^file:\/\//, ""))

  function open() {
    if (root.controller) root.controller.show()
    refreshStatus()
  }

  function close() {
    if (root.controller) root.controller.hide()
  }

  function toggle() {
    root.opened ? root.close() : root.open()
  }

  function refreshStatus() {
    if (!statusProcess.running) {
      statusProcess.command = [root.statusScriptPath]
      statusProcess.running = true
    }
  }

  function launchWebConsole() {
    if (root.bar) root.bar.run("omarchy launch browser " + (root.settings && root.settings.webConsoleUrl ? root.settings.webConsoleUrl : "http://localhost:8000"))
    root.close()
  }

  Process {
    id: statusProcess
    running: false
    stdout: StdioCollector {
      waitForEnd: true
      onStreamFinished: {
        var parsed = YardModel.parseStatus(text)
        if (parsed) root.fleetData = parsed
      }
    }
  }

  Timer {
    interval: (root.settings && root.settings.refreshIntervalSec ? root.settings.refreshIntervalSec : 30) * 1000
    running: true
    repeat: true
    triggeredOnStart: true
    onTriggered: root.refreshStatus()
  }

  IpcHandler {
    target: root.ipcTarget
    function open(): void { root.open() }
    function close(): void { root.close() }
    function toggle(): void { root.toggle() }
    function refresh(): string { root.refreshStatus(); return "ok" }
  }

  KeyboardPanel {
    id: panel
    anchorItem: root.anchorItem
    owner: root
    bar: root.bar
    open: root.opened
    contentWidth: panel.fittedContentWidth(Style.space(380))
    contentHeight: panel.fittedContentHeight(mainCol.implicitHeight, Style.space(560))

    Column {
      id: mainCol
      anchors.fill: parent
      spacing: Style.space(12)
      padding: Style.space(14)

      // Header
      PanelHero {
        width: parent.width
        title: "YARD CONTROL PLANE"
        meta: root.alarming ? "⚠ Anomaly Flagged" : "All Runtimes Nominal"
        foreground: root.foreground
        fontFamily: root.fontFamily
      }

      PanelSeparator { foreground: root.foreground }

      // Fleet Summary
      Column {
        width: parent.width
        spacing: Style.space(6)

        PanelSectionHeader {
          text: "FLEET RUNTIMES"
          foreground: root.foreground
          fontFamily: root.fontFamily
        }

        Item {
          width: parent.width
          implicitHeight: Style.space(22)
          Text {
            text: "Active Crews WIP"
            color: root.foreground
            font.family: root.fontFamily
            font.pixelSize: Style.font.body
            anchors.left: parent.left
          }
          Text {
            text: root.fleetData && root.fleetData.fleet ? (root.fleetData.fleet.activeCrews + " / " + root.fleetData.fleet.maxCrews) : "—"
            color: root.dim
            font.family: root.fontFamily
            font.pixelSize: Style.font.caption
            anchors.right: parent.right
          }
        }

        Item {
          width: parent.width
          implicitHeight: Style.space(22)
          Text {
            text: "Cursor Builder"
            color: root.foreground
            font.family: root.fontFamily
            font.pixelSize: Style.font.body
            anchors.left: parent.left
          }
          Text {
            text: root.fleetData && root.fleetData.cursor ? (root.fleetData.cursor.storiesCount + " stories · " + YardModel.formatTokens(root.fleetData.cursor.tokenBurn)) : "—"
            color: Color.accent
            font.family: root.fontFamily
            font.pixelSize: Style.font.caption
            anchors.right: parent.right
          }
        }

        Item {
          width: parent.width
          implicitHeight: Style.space(22)
          Text {
            text: "Grok Canary"
            color: root.foreground
            font.family: root.fontFamily
            font.pixelSize: Style.font.body
            anchors.left: parent.left
          }
          Text {
            text: root.fleetData && root.fleetData.grok ? (root.fleetData.grok.canaryTag + " (" + root.fleetData.grok.canaryPercent + "%)") : "—"
            color: root.dim
            font.family: root.fontFamily
            font.pixelSize: Style.font.caption
            anchors.right: parent.right
          }
        }
      }

      PanelSeparator { foreground: root.foreground }

      // Local Watch Alerts
      Column {
        width: parent.width
        spacing: Style.space(6)

        PanelSectionHeader {
          text: "LOCAL WATCH (ZERO EGRESS)"
          foreground: root.foreground
          fontFamily: root.fontFamily
        }

        BorderSurface {
          width: parent.width
          implicitHeight: alertText.implicitHeight + Style.space(16)
          visible: root.alarming
          color: Qt.rgba(root.urgent.r, root.urgent.g, root.urgent.b, 0.12)
          borderSpec: Border.flat(Qt.rgba(root.urgent.r, root.urgent.g, root.urgent.b, 0.4), 1)
          radius: Style.cornerRadius

          Text {
            id: alertText
            textFormat: Text.PlainText
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            anchors.margins: Style.space(10)
            text: (root.fleetData && root.fleetData.localWatch && root.fleetData.localWatch.alerts && root.fleetData.localWatch.alerts.length > 0)
              ? (root.fleetData.localWatch.alerts[0].id + ": " + root.fleetData.localWatch.alerts[0].message)
              : "No active anomaly."
            color: root.urgent
            font.family: root.fontFamily
            font.pixelSize: Style.font.caption
            wrapMode: Text.WordWrap
          }
        }

        Text {
          visible: !root.alarming
          text: "Local watch is quiet. Zero egress maintained."
          color: root.dim
          font.family: root.fontFamily
          font.pixelSize: Style.font.caption
        }
      }

      // Quick Launch Button
      Button {
        width: parent.width
        text: "Open YARD Tokyo Night Console"
        bordered: true
        foreground: root.foreground
        fontFamily: root.fontFamily
        onClicked: root.launchWebConsole()
      }
    }
  }
}
