
const organData = {
  brain: 0,
  eye: 0,
  heart: 0,
  liver: 0,
  lungs: 0,
  stomach: 0,
};

function updateOrganStats(data) {
  document.querySelectorAll(".organ-stats li").forEach(item => {
    const organ = item.dataset.organ;
    if (data[organ] !== undefined) {
      item.querySelector(".progress").style.width = `${data[organ]}%`;
      item.querySelector(".percentage").textContent = `${data[organ]}%`;
    }
  });
}

// Initialize
updateOrganStats(organData);

// Simulate update
setTimeout(() => {
  updateOrganStats({
    brain: 95,
    eye: 90,
    heart: 85,
    liver: 90,
    lungs: 60,
    stomach: 75,
  });
}, 5000);

