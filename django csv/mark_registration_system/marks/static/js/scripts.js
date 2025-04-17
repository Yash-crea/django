// static/js/scripts.js

// Validate the input form before submission
function validateForm() {
    const moduleCode = document.getElementById('module_code').value;
    const moduleName = document.getElementById('module_name').value;
    const coursework1 = document.getElementById('coursework_1').value;
    const coursework2 = document.getElementById('coursework_2').value;
    const coursework3 = document.getElementById('coursework_3').value;
    const studentID = document.getElementById('student_id').value;
    const studentName = document.getElementById('student_name').value;
    const gender = document.querySelector('input[name="gender"]:checked');
    const dateOfEntry = document.getElementById('date_of_entry').value;

    if (!moduleCode || !moduleName || !coursework1 || !coursework2 || !coursework3 || !studentID || !studentName || !gender || !dateOfEntry) {
        alert("Please fill in all the fields!");
        return false;
    }
    return true;
}
