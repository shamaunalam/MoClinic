// add hovered class to selected list item

let list = document.querySelectorAll(".navigation li");
function activeLink() {
  list.forEach((item) => {
    item.classList.remove("hovered");
  });
  this.classList.add("hovered");
}

list.forEach((item) => item.addEventListener("mouseover", activeLink));

// Menu Toggle

let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".navigation");
let main = document.querySelector(".main");

toggle.onclick = function () {
  navigation.classList.toggle("active");
  main.classList.toggle("active");
};






// PATIENT DETAILS

const patient = {
  name: "OGGY",
  age: 22,
  sex: "Male",
  temperature: 33.9,
  respiratory: 15.27,
  glucose: 114.77,
  cholesterol: 204.07
};

// Function to animate counting numbers
const animateNumber = (id, target, duration = 3700) => {
  const element = document.getElementById(id);
  if (!element) return console.error(`Element with ID '${id}' not found.`);
  
  let start = 0;
  const step = target / (duration / 10); // Increment per 10ms
  
  const update = () => {
    start = Math.min(start + step, target);
    element.textContent = start.toFixed(1); // Set with 1 decimal precision
    if (start < target) setTimeout(update, 10); // Continue until target is reached
  };
  update();
};

// Populate static details
document.getElementById('name').textContent = patient.name;
document.getElementById('age').textContent = patient.age;
document.getElementById('sex').textContent = patient.sex;

// Animate numerical fields
animateNumber('temperature', patient.temperature);
animateNumber('respiratory', patient.respiratory);
animateNumber('glucose', patient.glucose);
animateNumber('cholesterol', patient.cholesterol);



//    SYMPTOMS

// Function to dynamically add patient symptoms
function addObservationText(text) {
  const textarea = document.getElementById('symptomsText');
  textarea.value = text;
}

// Example usage
document.addEventListener("DOMContentLoaded", function () {
  // Example: Dynamically populating the textarea with patient observations
  addObservationText("Headache,Cough,Runny nose,Sneezing,Fever");
});


//     CHART ....................






//      loading animation......



// // Function to animate the counting effect
function animateCountUp(element, target) {
  let current = 0;
  const increment = target / 100; // Divide the target into small increments
  const duration = 4000; // Total animation duration in milliseconds
  const interval = duration / 100; // Interval time for updates

  const counter = setInterval(() => {
      current += increment; // Increase the current value
      if (current >= target) {
          current = target; // Ensure it stops at the target
          clearInterval(counter); // Stop the interval
      }
      element.textContent = Math.ceil(current); // Update the text content
  }, interval);
}

// Start the counting animation for each card
function startCounting() {
  const numbers = document.querySelectorAll('.numbers'); // Select all number elements
  numbers.forEach(number => {
      const target = parseInt(number.getAttribute('data-target')); // Get the target value
      animateCountUp(number, target); // Animate counting for this number
  });
}

// Start counting once the page loads
window.onload = startCounting;