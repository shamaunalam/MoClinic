
  document.getElementById("signOutBtn").addEventListener("click", function (e) {
    e.preventDefault(); // Prevent default action
    const confirmSignOut = confirm("ARE YOU SURE YOU WANT TO SIGN OUT?");
    if (confirmSignOut) {
      // Redirect to sign-out URL or perform an action
      window.location.href = "dashbord.html";
    }
  });
