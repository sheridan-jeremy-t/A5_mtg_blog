This is assignment 4 for the OntarioLearn course Python for Web Development hosted by Sheridan College.  

Assignment 4: HTML Django templates

User Name: jeremy pwd: Admin1234$  
User Name: instructor pwd: DjangoRocks1!


Assignment – Photo contest

This assignment adds another feature to your blog website which will collect and save user data and an image to the database as part of a hypothetical photo contest.

Add a link to the contest in the main navigation bar which will take users to a page describing the contest and containing a form in which they can upload their information and photo submission.

The required pieces of information to gather from the user are

    Their name
    Their email address
    An image

In addition to the information gathered, also save the date & time of the submission.

Register the model in the Django admin and customize its presentation so it can be sorted, filtered, etc. by a staff member of your site.
Hints

    To upload files in a form you must set the encoding to "multipart/form-data" by adding the following to the <form> tag: <form enctype="multipart/form-data" ... >

Evaluation
Grading 	Criteria
/ 5 	Upload form
/ 5 	Django admin
/ 5 	Template presentation, presence of links to contest page
Grade ( / 5 ) 	Explanation of Criteria
5 	Criteria is met and all functionality is present
3 	Criteria is mostly met with some gaps in functionality
1 	Criteria is mostly unsatisfied or not functional, though some elements are present
0 	Criteria is not met. No visible attempt to satisfy it exists

Submission Details:

Submit in the assignment dropbox:

    A copy of your db.sqlite3 file containing your database.
    The GitHub repository URL

Create a superuser account for yourself and for the instructor. The instructor username should be: instructor and the password should be DjangoRocks1!
Running the code:

The instructor will run your code using these steps. Make sure your project is compatible.

    Checkout your code from the provided public Github repository.
    Install any new pip modules by running: pip install -r requirements.txt
    Copy your db.sqlite3 submitted file to the project folder
    Start the website: python manage.py runserver
    Test your website by navigating to: http://127.0.0.1:8000

The course grading policy is available here: Evaluation Plan & Grading Policy.