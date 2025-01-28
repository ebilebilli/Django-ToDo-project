# Django To-Do Application

This is a Django-based To-Do application that allows users to create, manage, and organize their tasks. Users can create notes, assign labels, pin important notes, mark tasks as completed, and move tasks to a trash bin. The application also includes features like restoring deleted notes, permanently deleting notes, and managing labels.

## Features

- **User Authentication:** Users can register, log in, and log out.
- **Create Notes:** Users can create new notes and assign them to labels.
- **Edit Notes:** Users can update the content of existing notes.
- **Pin Notes:** Users can pin up to 6 important notes for quick access.
- **Mark as Completed:** Users can mark tasks as completed or incomplete.
- **Trash Bin:** Deleted notes are moved to a trash bin and can be restored or permanently deleted.
- **Label Management:** Users can create, edit, and delete labels for better organization.
- **Automatic Cleanup:** Notes in the trash bin for more than 30 days are automatically deleted.

Usage
User Registration and Login
Register a new account by visiting the registration page (/register).

Log in using your credentials at the login page (/login).

Managing Notes
Create a Note: On the home page, enter the note content and select a label (if any) to create a new note.

Edit a Note: Click on a note to view its details and update its content.

Pin a Note: Click the pin icon to pin a note. Only 6 notes can be pinned at a time.

Mark as Completed: Click the checkbox to mark a note as completed.

Delete a Note: Move a note to the trash bin by clicking the delete button.

Managing Labels
Create a Label: Use the label creation form to add a new label.

Delete a Label: Delete a label from the label management section.

Trash Bin
Restore a Note: Restore a deleted note from the trash bin.

Permanently Delete a Note: Delete a note permanently from the trash bin.

Automatic Cleanup: Notes in the trash bin for more than 30 days are automatically deleted.

API Endpoints
Get Notes by Label: /get-notes/<label_id>/ - Returns a JSON list of notes for a specific label.

Complete Note: /complete-note/<pk>/ - Toggles the completion status of a note.

Pin Note: /pin-note/<pk>/ - Toggles the pin status of a note.

Contributing
Contributions are welcome! If you'd like to contribute, please follow these steps:

Fork the repository.

Create a new branch (git checkout -b feature/YourFeatureName).

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/YourFeatureName).

Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Thanks to Django for providing a powerful web framework.

Special thanks to the open-source community for their contributions.

Contact
If you have any questions or suggestions, feel free to reach out:

Email: ebilebilli3gmail.com

GitHub: https://github.com/ebilebilli