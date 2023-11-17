# Uniclef
### Description of the Project:
Uniclef is an online music learning platform that offers a variety of music courses to users interested in learning and improving their musical skills. Users can create accounts, browse courses, enroll in courses, and read about the instructors. The platform also supports payment processing, refunds, and payment history tracking.
### Roadmap
#### Iteration 1
-	Users can create an account
-	Users can login
-	Users can view list of music courses
-	Users can filter courses by title, category/genre, difficulty, duration, or price
-	Users can view information on instructors
-	Users can view featured courses and the instructor of the month
#### Iteration 2
-	Users can buy a course to become enrolled in it
- Users payment methods are stored
-	Users can see the courses they are enrolled in
-	*Enrolled users can access the course materials* **(NOT IMPLEMENTED)**
-	*Enrolled users can track their progress in the course* **(NOT IMPLEMENTED)**
#### Iteration 3
-	*Enrolled users can leave reviews and ratings for courses they complete* **(NOT IMPLEMENTED)**
-	Users can request a refund of a course
-	If refunded, users lose access to the course (lose their enrollment)
-	Users can see their payment history
### Acceptance Criteria
#### Iteration 1 (with acceptance criteria)
- **Users can create an account**
  - User should be able to create an account with the following details: first name, last name, gender, phone number, email address, city, country, and password
  - Valid email has an @ and valid domain
  - Valid phone is all numbers
  - Password is at least 8 characters long
  - Password and email cannot be the same
  - Password is not entirely numeric
  - If any of the above is empty or not valid, show relevant message
  - The user’s sign up date is stored in the database
  - The user’s last log in date is stored in the database.
- **Users can login**
  - Email and password must entered
  - Password must be valid
- **Users can view list of music courses**
  - Courses are listed sorted desc with date of release
  - A course listing shows title, photo, instructor, short description, duration of course, difficulty of course, category/categories, ratings, reviews and an enroll button
- **Users can filter courses by title, category/genre, difficulty, duration, or price**
  - Users can filter courses by typing in keywords in the title, category, choose difficulty, duration or price range
  - Display a message if no courses match the selected filters
- **Users can view information on instructors**
  - Users can see all instructor names and pictures, and description of the instructor of the month
- **Users can view featured courses and the instructor of the month**
  - Users can see the most popular/latest courses, and the instructor of the month
  - Featured courses are the most recently released courses or courses with highest ratings
  - Instructors of the month are ones that have the highest enrollments in their courses
#### Iteration 2 (with acceptance criteria)
- **Users can add payment method**
  - Users can add cards as their payment method
  - Payment methods are stored securely in the database
- **Users can buy a course to become enrolled in it**
  - Users can buy and enroll in a course
  - Enrollment and payment details such as course_id, student_id, enrollment_date, and amount_paid are stored in the database
- **Users can see the courses they are enrolled in**
  - All courses the user is enrolled in are displayed on their dashboard
- **(NOT IMPLEMENTED)** **Enrolled users can access the course materials and assessments** **(NOT IMPLEMENTED)**
  -	Users who have paid/enrolled in a course can access course materials such as videos, audios, and text-based resources
  - Enrolled users can also access assessments such as quizzes, tasks and exams
  - Users cannot access a course material unless they have enrolled in the course
- **(NOT IMPLEMENTED)** **Enrolled users who started courses can track their progress** **(NOT IMPLEMENTED)**
  - Enrolled users can see how far along they are in a course (percentage), how they scored on assessments, how many tasks/assessments they have remaining.
#### Iteration 3 (with acceptance criteria)
- **(NOT IMPLEMENTED)**	**Enrolled users can leave reviews and ratings for courses they complete** **(NOT IMPLEMENTED)**
  - Enrolled users can leave reviews and ratings for courses they have completed
  - Reviews and ratings are stored in the database and displayed publicly on the course page
- **Users can request a refund of a course**
  - After buying a course, a user can request a refund within 3 days stating the reason for refunding a course
  - After 3 days of purchase, a user cannot request a refund of the course
- **If refunded, users lose access to the course**
  - Refunded users can no longer access course materials or their progress in them
  - Refund details such as date and reason for cancellation are stored in the database
- **Users can see their payment history**
  - Users can view their payment history on the platform
  - Payment history details such as date, amount, and payment method are displayed to the user

#### The following are the ER models from the database designing stage and from the Django application:
![ERD Final](https://github.com/sarakabariti/Uniclef/assets/61201657/f4d24ceb-088b-4760-b42d-378289c765a4)
![Django ERD](https://github.com/sarakabariti/Uniclef/assets/61201657/d885e77a-9e8c-499c-a54a-e03d26a3af03)

### Set up instructions:
1. To install the libraries, first you need to create a virtual environment:
<br> ```python3 -m venv venv```
2. To activate the virtual environment: 
<br> ```source venv/bin/activate```
3. To install all the requirements:
<br> ```pip3 install -r requirements.txt```
4. Launch the Postgres console by running ```psql```
5. Create a new database named *uniclefdb* with the command ```CREATE DATABASE uniclefdb```
6. To connect and access the database use a valid postgres username and password ```CREATE USER username WITH PASSWORD 'supersecret'```
7. To get explicit permission to have read and write capabilities on the newly created database: ```GRANT ALL PRIVILEGES ON DATABASE "uniclefdb" to username;```
8. Modify /uniclef/settings.py file 
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'uniclefdb',
        'USER': 'username',
        'PASSWORD': 'supersecret',
        'HOST': 'localhost'
    }
}
```
9. Run ```python manage.py makemigrations```
10. Run ```python manage.py migrate```
11. Run ```python manage.py runserver```

### Contribution List:
- Principles of Relational Database Management Systems
- Entity-relationship models
- Database normalization and schema optimization (many different versions of the schema over time)
- Database indexing
- Database constraints
- Object-relational Mapper (ORM) using postgreSQL
