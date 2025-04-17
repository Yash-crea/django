import os
import csv
from django.shortcuts import render, redirect
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend before importing pyplot
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Path to the CSV file
file_path = os.path.join(os.path.dirname(__file__), 'marks_data.csv')

def home(request):
    num_students = 0
    num_modules = 0

    # Check if the file exists before reading it
    if os.path.exists(file_path):
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)[1:]  # Skip the header row

        # Count number of students
        num_students = len(data)

        # Count number of unique modules
        num_modules = len(set(row[0] for row in data))  # Assuming module_code is the first column

    return render(request, 'marks/home.html', {'num_students': num_students, 'num_modules': num_modules})

def input_mark(request):
    if request.method == 'POST':
        # Get data from form
        module_code = request.POST.get('module_code')
        module_name = request.POST.get('module_name')
        cw1 = request.POST.get('cw1')
        cw2 = request.POST.get('cw2')
        cw3 = request.POST.get('cw3')
        student_id = request.POST.get('student_id')
        student_name = request.POST.get('student_name')
        gender = request.POST.get('gender')
        date_of_entry = request.POST.get('date_of_entry')

        # If the file doesn't exist, create it and write the header
        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['module_code', 'module_name', 'CW1', 'CW2', 'CW3', 'student_id', 'student_name', 'gender', 'date_of_entry'])

        # Save the submitted data into the CSV
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([module_code, module_name, cw1, cw2, cw3, student_id, student_name, gender, date_of_entry])

        # Redirect to home page after submitting the form
        return redirect('home')  # Redirecting to the home page

    return render(request, 'marks/input_mark.html')

def view_mark(request):
    # Get module_code from the URL query string
    module_code = request.GET.get('module_code', None)

    # Initialize an empty list to store marks
    marks = []

    if module_code:
        # Open CSV and filter the data based on module_code
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                if row[0] == module_code:
                    # Safely attempt to sum CW1, CW2, CW3 and handle empty values
                    try:
                        # Convert empty strings to 0 if no mark is entered
                        cw1 = float(row[2]) if row[2] and row[2] != '' else 0.0
                        cw2 = float(row[3]) if row[3] and row[3] != '' else 0.0
                        cw3 = float(row[4]) if row[4] and row[4] != '' else 0.0
                        total_marks = cw1 + cw2 + cw3
                    except ValueError:
                        total_marks = 0.0  # Default to 0 if there's an invalid value

                    # Append the relevant data for the student
                    marks.append([row[5], row[6], row[2], row[3], row[4], total_marks])
    
    # Render the template with the marks
    return render(request, 'marks/view_mark.html', {'marks': marks, 'module_code': module_code})

def update_mark(request):
    if request.method == 'POST':
        module_code = request.POST['module_code']
        student_id = request.POST['student_id']
        date_of_entry = request.POST['date_of_entry']
        new_cw1 = request.POST['cw1']
        new_cw2 = request.POST['cw2']
        new_cw3 = request.POST['cw3']

        # Use file_path to get the correct path to the CSV
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            rows = []
            for row in reader:
                if row[0] == module_code and row[5] == student_id and row[8] == date_of_entry:
                    row[2] = new_cw1
                    row[3] = new_cw2
                    row[4] = new_cw3
                rows.append(row)
        
        # Write the updated rows back to the CSV
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    return render(request, 'marks/update_mark.html')

def visualisation(request):
    # Create bar chart (example: average marks per student)
    student_marks = {}
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            student_name = row[6]
            try:
                cw1 = float(row[2]) if row[2] else 0
                cw2 = float(row[3]) if row[3] else 0
                cw3 = float(row[4]) if row[4] else 0
                total = cw1 + cw2 + cw3
            except ValueError:
                total = 0
            if student_name not in student_marks:
                student_marks[student_name] = []
            student_marks[student_name].append(total)

    # Average marks per student
    avg_marks = {student: sum(marks) / len(marks) for student, marks in student_marks.items()}

    # Bar Chart (Average marks per student)
    plt.figure(figsize=(8, 5))  # Set figure size
    plt.bar(avg_marks.keys(), avg_marks.values())
    plt.xlabel('Student Name')
    plt.ylabel('Average Marks')
    plt.title('Average Marks Per Student')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

    # Save plot to a BytesIO object
    bar_buf = BytesIO()
    plt.savefig(bar_buf, format='png')
    bar_buf.seek(0)
    chart_url = base64.b64encode(bar_buf.read()).decode('utf-8')
    bar_buf.close()
    plt.clf()  # Clear figure
    plt.close()  # Close figure

    # Pie chart (Distribution of gender)
    gender_counts = {'Male': 0, 'Female': 0}
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            gender = row[7].strip().capitalize()  # Normalize gender input
            if gender in gender_counts:
                gender_counts[gender] += 1

    # Pie Chart (Gender distribution)
    plt.figure(figsize=(6, 6))
    plt.pie(gender_counts.values(), labels=gender_counts.keys(), autopct='%1.1f%%', startangle=140)
    plt.title('Gender Distribution')

    # Save pie chart to a BytesIO object
    pie_buf = BytesIO()
    plt.savefig(pie_buf, format='png')
    pie_buf.seek(0)
    pie_chart_url = base64.b64encode(pie_buf.read()).decode('utf-8')
    pie_buf.close()
    plt.clf()  # Clear figure
    plt.close()  # Close figure

    return render(request, 'marks/visualisation.html', {'chart_url': chart_url, 'pie_chart_url': pie_chart_url})