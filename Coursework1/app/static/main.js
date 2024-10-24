document.addEventListener('DOMContentLoaded', function () {
    const today = new Date().toISOString().split('T')[0];
    const dateInput = document.querySelector('input[type="date"]');
    
    // Set the minimum date attribute to today
    dateInput.setAttribute('min', today);
  
    // Add an event listener to validate the date on change
    dateInput.addEventListener('change', function () {
      if (this.value < today) {
        alert('Past dates are not allowed.');
        this.value = '';
      }
    });
  });

  <script src="{{ url_for('static', filename='js/main.js') }}"></script>
