The bot must provide users with the ability to add product cards. The cards should have the following attributes: name, description, price, and photo (optional).

The main menu must include the buttons: "Add Product Card" and "View Product Cards."
- Upon clicking the first button, the bot should collect information about the card from the user in a multi-step process and then send it for moderation.
- Upon clicking the second button, the bot should send the first card from the database with inline buttons. The "«" and "»" buttons should switch between product cards, allowing users to view them all.

There must also be an Admin Menu. It can be accessed via an "Admin Menu" button, which should be present in the keyboard for admins but not for regular users.
The Admin Menu contains the following buttons: "Moderation," "Statistics," and "Back."
- The "Moderation" button allows admins to moderate user cards and decide whether to approve or delete them. This section should also use an inline keyboard for pagination. Additionally, there should be an "Edit" inline button; clicking it should trigger a reply keyboard where an attribute can be selected and modified.
- The "Statistics" button displays a list of users and the number of cards they have created (total, approved, and rejected).
- The "Back" button returns the admin to the main keyboard.

Development Preferences:
- Modular architecture
- Use of custom filters
- Database: SQLite or PostgreSQL
- Logging of main actions (standard logger is acceptable)
