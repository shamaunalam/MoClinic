// Function to create a gauge chart with animated counting and slow loading
function createGaugeChart(canvasId, value, min, max, colors, labels, duration) {
  const ctx = document.getElementById(canvasId).getContext("2d");

  // Check if context is valid
  if (!ctx) {
    console.error("Chart context is not found for canvas ID:", canvasId);
    return;
  }

  // Animate the value
  let currentValue = min;
  let increment = (value - min) / (duration / 10);  // Increment step for animation

  // Update the value every 10ms (smooth animation)
  const valueUpdater = setInterval(() => {
    if (currentValue < value) {
      currentValue += increment;
      currentValue = Math.min(currentValue, value); // Ensure we don’t exceed the final value
      document.getElementById("heartRateValue").textContent = currentValue.toFixed(2) + " bpm"; // Update the displayed value
    } else {
      clearInterval(valueUpdater); // Stop the animation when we reach the target value
    }
  }, 10);

  // Create the chart after a delay (simulating slow load)
  setTimeout(() => {
    new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [
          {
            data: [value - min, max - value, max - min],
            backgroundColor: colors,
            borderWidth: 0,
          },
        ],
      },
      options: {
        responsive: true,
        rotation: -90,
        circumference: 180,
        cutout: "69%",
        plugins: {
          legend: { display: false },
        },
      },
    });
  }, 2000); // Delay chart loading by 2 seconds
}

// Create Heart Rate Gauge with animation and delayed loading
createGaugeChart(
  "heartRateGauge",
  82.83,  // Current value
  50,     // Min value
  200,    // Max value
  ["#4CAF50", "#FFEB3B", "#F44336"], // Segment colors
  ["Rest", "Normal", "Elevated"],     // Labels
  4500    // Duration for counting animation (3 seconds)
);
