# Startup Radar Interface
## Overview
This project provides a graphical user interface (GUI) built with Python's customtkinter and ttk libraries, enabling users to manage and interact with startup lists. The interface allows for the creation, viewing, and deletion of startup lists, as well as exporting these lists and their recommendations to CSV files.

## Features
- **List Management:**

   + View existing startup lists.
   + Create new lists and add entries to them.
   + Edit or delete existing entries within a list.
   + Delete entire lists.
- **CSV Export:**

   - Export selected lists or their recommendations as CSV files.
- **User Interface:**

   - Simple and intuitive interface.
   - Uses *customtkinter* for enhanced theming and styling.
  
## Installation
1. Clone the repository:

`git clone  https://github.com/Gg-SALMON/StartupRadarGUI.git>`

2.Install required dependencies:

`pip install -r requirements.txt`

3.Configure the project:
Update the config.py file with your correct API_KEY to connect to your backend API.

## How to Use
1. **Run the GUI :**
    
Execute the GUI.py file to launch the application:

`python GUI.py`

2. **Main Interface:**
- The main window displays a list of your existing startup lists.
- Use the buttons on the right side of the interface to manage your lists and export data.
3.**Creating a New List:**

- Click on "Create new list" and follow the prompts to add a new startup list.
4.**Viewing or Editing Lists:**

- Select a list and use the "View detail list" button to see its contents. You can then edit or delete specific entries.
5.**Exporting Data:**

- Use the "Generate CSV" buttons to export the data for selected lists.
## Directory Structure
- **GUI.py:** The main script that initializes and runs the GUI.
- **script.py:** Contains the backend logic for fetching data, interacting with the API, and handling user actions.
- **config.py:** Configuration file to store API endpoints and headers.
- **requirements.txt:** Lists the required Python packages for the project.
## Dependencies
- requests

- pandas

- tkinter

- customtkinter

- ttk

## Troubleshooting
- **API Connectivity**: Ensure that the url_base and HEADERS in config.py are correctly configured to connect to the backend API. Visit [StartUpRadar API documentation](https://api.startupradar.co/docs#/lists/) to check any update on the endpoints.
- **Data Not Loading**: If the list data does not load, check the API connection and ensure the server is running.

## Acknowledgments
Special thanks to the developers of **customtkinter** and **ttk** for their excellent libraries that made this project possible.
