function App() { }

App.prototype.setState = function(key, state) {
  localStorage.setItem(key, state);
}

App.prototype.getState = function(key) {
  return localStorage.getItem(key);
}

function init() {
  var app = new App();
  
  // Get all checkboxes that we want to check
  var checkboxes = document.querySelectorAll('.list input[type="checkbox"]');
   
  // Loop through all checkboxes
  for (var i = 0; i < checkboxes.length; i++) {
    
    // The current checkbox in the loop
    var checkbox = checkboxes[i];
    
    // Determine if the checkbox is saved in LocalStorage
    var isSaved = app.getState(checkbox.id);
      
    // Set the selected state
    if (isSaved === 'true') {
      checkbox.checked = true;
    }
    
    // Create an event listener for each checkbox
    checkbox.addEventListener('click', function(e) {
      // We save the checkbox id as the key in localStorage
      // We save the checkbox checked state as the value
      var _checkbox = e.target;
      app.setState(_checkbox.id, _checkbox.checked)
    });
  }
}

init();