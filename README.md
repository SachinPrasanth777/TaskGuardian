<h1 align="center" id="title">TaskGuardian</h1>

<p id="description">Welcome to the TaskGuardian Repository. This is an API that is built to manage tasks by admins and users. The Key features include secure authentication and use of mails to notify the users about their tasks and also for authentication purposes.</p>

## Features

- [x] User registration
- [x] User verification via email
- [x] Admin registration
- [x] Admin verification via email
- [x] Issue Tasks to users followed by emails
- [x] Update the assignees of each task followed by emails 

## API Documentation
### `Admin Routes`

### `POST /admin/signup`

Signup for the admin users.

### `POST /admin/generate-otp`

Generates OTP to the user account for secure admin authentication.

### `POST /admin/verify-otp`

Verifies OTP with the one sent to the Email.

### `POST /admin/create-task`

> [!NOTE]  
> This route requires a JWT Token

Route for creating a task and assigning a user.

### `DELETE /admin/delete-task`

> [!NOTE]  
> This route requires a JWT Token

Route for admin to delete a task.

### `PUT /admin/update-task`

> [!NOTE]  
> This route requires a JWT Token

Route for admin to update a task and its users. If the assignee is changed an email is sent to the new assignee.

### `User Routes`

### `POST /users/signup`

Signup for the users.

### `POST /users/generate-otp`

Generates OTP to the user account for secure user authentication.

### `GET /users/login`

For secure and passwordless authentication with your google account.

### `GET /users/auth`

For finding out the user information from google and getting an access token for otp generation.

### `POST /users/verify-otp`

Verifies OTP with the one sent to the Email.

### `GET /users/user`

> [!NOTE]  
> This route requires a JWT Token

Get the information about the user.

### `GET /users/tasks`

> [!NOTE]  
> This route requires a JWT Token
Get all the tasks assigned to the user.

### `GET /users/all-tasks`

> [!NOTE]  
> This route requires a JWT Token

Get all the tasks created by the admin

<h2>Screenshots</h2>
<img width="1440" alt="Screenshot 2024-07-10 at 3 32 46 PM" src="https://github.com/SachinPrasanth777/TaskGuardian/assets/142246653/fbf15c4f-7be6-40b8-9a5f-94dd0b45d7cd">
<img width="1440" alt="Screenshot 2024-07-10 at 3 32 56 PM" src="https://github.com/SachinPrasanth777/TaskGuardian/assets/142246653/e237f226-ddf5-474d-b448-d6674d409aad">
<img width="1440" alt="Screenshot 2024-07-10 at 3 37 09 PM" src="https://github.com/SachinPrasanth777/TaskGuardian/assets/142246653/03371d61-1f49-42e4-9210-8bd4df8c6796">
<img width="1440" alt="Screenshot 2024-07-10 at 3 36 52 PM" src="https://github.com/SachinPrasanth777/TaskGuardian/assets/142246653/f1c708e7-18bc-44ac-84ef-a29cdaf72f89">


# How Start the Project?

## Running the code
```
pip install -r requirements.txt
```
```
uvicorn index:app --reload
```

## Running the Docker Container
```
docker compose up --build
```

## Credits

This app uses the following tech stacks:

- FastAPI
- MongoDB
- Docker
- Google OAuth 2.0
