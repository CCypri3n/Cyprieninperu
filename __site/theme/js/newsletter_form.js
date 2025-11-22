const form = document.querySelector('form[name="newsletter"]');
  const successMessage = document.getElementById('newsletter-success');

  form.addEventListener('submit', function (event) {
    event.preventDefault(); // prevent default form submission

    const formData = new FormData(form);

    fetch('/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams(formData).toString(),
    })
    .then(response => {
      if (response.ok) {
        form.style.display = 'none';         // hide the form
        successMessage.style.display = 'block'; // show success message
        form.reset();
      } else {
        alert('There was a problem submitting your form');
      }
    })
    .catch(error => {
      alert('Error submitting form: ' + error.message);
  });
});