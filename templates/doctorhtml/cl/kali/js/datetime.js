function updateDateTime() {
    const now = new Date();
    document.getElementById("date").textContent = now.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    document.getElementById("time").textContent = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    document.getElementById("day").textContent = now.toLocaleDateString('en-US', { weekday: 'long' });
  }
  
  // Update every second
  setInterval(updateDateTime, 1000);
  updateDateTime();
  