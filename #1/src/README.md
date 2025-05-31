# Cinema Management System

The **Cinema Management System** is a web-based application designed to manage movie data, theaters, and screening schedules. The project adopts a modular structure that separates presentation, logic, and data layers to ensure maintainability and scalability.

## Architecture

The application uses a combination of HTML, CSS, and JavaScript for the frontend, while the backend is built with PHP and a relational database. Communication between the client and server is handled asynchronously through AJAX, allowing seamless data exchange without requiring full page reloads. This ensures a responsive and fluid user experience.

Toast notifications are used to provide real-time feedback to users on operations such as insertions, deletions, and updates. For dynamic and interactive data presentation, especially for listings such as screenings or movies, the system leverages **DataTables**, enabling sorting, pagination, and filtering directly in the browser.

Server-side logic is organized into PHP scripts that handle CRUD operations. These scripts use prepared statements to communicate securely with the database and return structured responses in JSON format, which are then processed on the client side.

## Features

- Asynchronous client-server interaction using AJAX  
- Real-time user feedback via toast notifications  
- Interactive tabular views with DataTables  
- Secure and efficient database access through prepared PHP statements  
- Clear modular separation between UI, logic, and data layers
