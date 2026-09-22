.pragma library

function formatTokens(count) {
  var n = Number(count || 0);
  if (n >= 1e6) return (n / 1e6).toFixed(1) + "M";
  if (n >= 1e3) return (n / 1e3).toFixed(1) + "K";
  return String(n);
}

function parseStatus(rawText) {
  try {
    return JSON.parse(rawText);
  } catch (e) {
    return null;
  }
}

function getActiveBeadSummary(fleetData) {
  if (!fleetData || !fleetData.beads) return "No active bead";
  var inWork = fleetData.beads.inWork;
  if (!inWork) return "All beads idle";
  return inWork.id + " · " + (inWork.title || "In progress");
}

function getBeadsAdoptionLabel(fleetData) {
  if (!fleetData || !fleetData.beadsSystem) return "Beads: Ready";
  var sys = fleetData.beadsSystem;
  return sys.adoptedRepos + "/" + sys.totalRepos + " repos (" + sys.adoptionPercent + "%)";
}

function getGithubSummary(fleetData) {
  if (!fleetData || !fleetData.allProjects) return "Git: Nominal";
  var totalPrs = 0;
  var projects = Object.keys(fleetData.allProjects);
  for (var i = 0; i < projects.length; i++) {
    var prList = fleetData.allProjects[projects[i]].githubPrs;
    if (prList && prList.openPrs) {
      totalPrs += prList.openPrs.length;
    }
  }
  return totalPrs > 0 ? (totalPrs + " open PRs") : "Clean";
}

function getWelfareSummary(fleetData) {
  if (!fleetData || !fleetData.coordinator || !fleetData.coordinator.welfareAudit) {
    return "Welfare: Nominal";
  }
  var audit = fleetData.coordinator.welfareAudit;
  if (audit.stalled > 0) {
    return "Welfare: " + audit.stalled + " Stalled Worker" + (audit.stalled > 1 ? "s" : "");
  }
  if (audit.warning > 0) {
    return "Welfare: " + audit.warning + " Warning · " + audit.healthy + " Healthy";
  }
  return "Welfare: " + audit.healthy + "/" + audit.totalWorkers + " Healthy";
}

function getActiveWorkerHost(fleetData) {
  if (!fleetData || !fleetData.allProjects || !fleetData.beads) return "local";
  var p = fleetData.allProjects[fleetData.beads.activeProject];
  return p && p.host ? p.host : "local";
}

function getActiveWorkerWelfare(fleetData) {
  if (!fleetData || !fleetData.allProjects || !fleetData.beads) return "NOMINAL";
  var p = fleetData.allProjects[fleetData.beads.activeProject];
  return p && p.welfare && p.welfare.status ? p.welfare.status : "NOMINAL";
}

function getActiveWorkerPeek(fleetData) {
  if (!fleetData || !fleetData.allProjects || !fleetData.beads) return "No active probe";
  var p = fleetData.allProjects[fleetData.beads.activeProject];
  if (p && p.welfare && p.welfare.peek && p.welfare.peek.summary) {
    return p.welfare.peek.summary;
  }
  return "Heartbeat nominal";
}
