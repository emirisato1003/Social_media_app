# Social Media Web Application - Visualist

## Project Overview
This project is a Django-based social media web application that allows users to create profiles, make posts, follow other users, and interact with content through likes and saves.

## Distinctiveness and Complexity
- Advanced User Interactions: The application implements complex user relationships including following/follower systems and post interactions (likes, saves).
- Custom User Profiles: Each user has a detailed profile with additional information beyond the standard Django User model.
- Comprehensive Post Management: Users can create and edit posts.
- Responsive Design: The application uses a combination of server-side rendering and client-side interactivity for a smooth user experience.

### File Structure and Contents
- ```views.py```: contains all the view functions for handling HTTP requests and responses.
  - ```index```: Tenders the main page
  - ```single_post```: Displays a single post
  - ```edit```: handles post editing
  - ```profile```: manages user profile views and interactions
  - ```follow / unfollow_user```: manages user's follower and following system.
  - ```like```: deals with user's like interactions
  - ```save / unsave```: manages the posts that user saved.
  - ```upload```: handles uploading new posts
  - ```settings```: displays and handle user's profile page.

- ```models.py```: defines the database models including User, Profile, Post, Category, Like, Save, and Follow.

- ```templates/```: Directory containing HTML templates:
  * ```index.html```: Main page template
  * ```layout.html```: Base template for consistent layout
  * ```login.html```: Login page
  * ```profile.html```: User profile page
  * ```register.html```: Registration page
  * ```saved.html```: Saved posts page
  * ```setting.html```: Profile settings page
  * ```single_post.html```: Individual post view
  * ```upload.html```: Post creation/upload page


```static/```: Contains static files like images, CSS and JavaScript:
  - ```style.css```: Main stylesheet
  - ```index.js```: Client-side interactivity scripts


### How to run application
1. Ensure you have Python and Django installed.
2. Clone the repository to your local machine.
3. Navigate to the project directory in your terminal.
4. Install required packages: ```pip install -r requirements.txt```
5. Run migrations: ```python manage.py migrate```
6. Create a superuser: ```python manage.py createsuperuser```
7. Start the development server: ```python manage.py runserver```
8. Access the application at ```http://localhost:8000```