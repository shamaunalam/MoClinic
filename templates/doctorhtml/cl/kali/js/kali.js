
// loading KALI
window.addEventListener("load", () => {
    const kali = document.getElementById("kali");
  
    // Add a delay before hiding the preloader (optional)
    setTimeout(() => {
      kali.style.opacity = "0"; // Fade-out effect
      kali.style.visibility = "hidden"; // Hide the preloader
      
    }, 1500);
  });
  