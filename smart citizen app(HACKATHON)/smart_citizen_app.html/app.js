function submitForm() {
    var name = document.getElementById('name').value;
    var email = document.getElementById('email').value;
    var issue = document.getElementById('issue').value;

    if (name.trim() === '' || email.trim() === '' || issue.trim() === '') {
        document.getElementById('errorMessage').innerText = 'All fields are required';
    } else {
        alert('Form submitted successfully!');
        document.getElementById('citizenForm').reset();
        document.getElementById('errorMessage').innerText = '';
    }
}
