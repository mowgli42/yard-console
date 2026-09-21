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
