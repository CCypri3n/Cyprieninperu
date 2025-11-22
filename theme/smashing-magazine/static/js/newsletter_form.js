const form = document.querySelector('form[name="newsletter"]');
const successMessage = document.getElementById('newsletter-success');

form.addEventListener('submit', async function (event) {
  event.preventDefault(); // Prevent default form submission

  // Create a JS object with form values expected by Postcatch.io
  const data = {
    name: form.name ? form.name.value : 'Newsletter Subscription', // optional: if you have a name field
    email: form.email.value,
    message: form.message ? form.message.value : 'A new person subscribed to your newsletter.' // optional: if you have a message field
  };

  try {
    const response = await fetch('https://api.postcatch.io/submit/138b0e91-1945-4621-97cd-03f57daf2af0', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      form.style.display = 'none';
      successMessage.style.display = 'block';
      form.reset();
    } else {
      alert('There was a problem submitting your form');
    }
  } catch (error) {
    alert('Error submitting form: ' + error.message);
  }
});
