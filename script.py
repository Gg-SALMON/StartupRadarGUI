import requests
import pandas as pd
from tkinter import filedialog, messagebox
import customtkinter as customtkinter
from tkinter import ttk
from tkinter import *
import os
from pathlib import Path
from config import *


def create_data_frame_all_existing_lists():
    """
     Fetches all existing lists from the API and creates a DataFrame.

     Returns:
         pd.DataFrame: DataFrame containing the list information.
     """
    response = requests.get(url_base + "lists", headers=HEADERS)
    data = response.json()
    df_l = []
    for list_ in data:
        df_l.append([list_['id'], list_['name'], list_['description'], list_['created_at'], list_['updated_at']])
    df = pd.DataFrame(df_l)
    df.columns = ['id', 'name', 'description', 'created_at', 'updated_at']
    df.set_index(['id'])
    # df.created_at = (df.created_at.apply(lambda x: x.split('T')[0]))
    # df.created_at = pd.to_datetime(df.created_at)
    # df.updated_at = (df.updated_at.apply(lambda x: x.split('T')[0]))
    # df.updated_at = pd.to_datetime(df.updated_at)
    return df


# Create a DataFrame of existing lists
df_existing_list = create_data_frame_all_existing_lists()


# List of all available slugs
list_of_slug = df_existing_list.id.values.tolist()

# Default path for saving files
default_path = os.getcwd()


def get_slug_list():
    """
      Fetches all list slugs from the API.

      Returns:
          list: List of slugs available in the system.
      """
    response = requests.get(url_base+"lists", headers=HEADERS)
    data_list = response.json()
    return [list_['id'] for list_ in data_list]


def is_slug_available(slug):
    """
     Checks if a given slug is available in the list of slugs.

     Args:
         slug (int): Slug to check.

     Returns:
         bool: True if the slug is available, False otherwise.
     """
    global list_of_slug
    if slug in list_of_slug:
        return True
    else:
        print(f"slug number {slug} not available. Check the number or update the list")
        return False


def create_data_frame_all_existing_lists():
    """
         Fetches details of a specific list and creates a DataFrame.

         Returns:
             pd.DataFrame: DataFrame containing existing list
         """
    response = requests.get(url_base+"lists", headers=HEADERS)
    data = response.json()
    df_l = []
    for list_ in data:
        df_l.append([list_['id'], list_['name'], list_['description'], list_['created_at'], list_['updated_at']])
    df = pd.DataFrame(df_l)
    df.columns = ['id', 'name', 'description', 'created_at', 'updated_at']
    df.set_index(['id'])
    # df.created_at = (df.created_at.apply(lambda x: x.split('T')[0]))
    # df.created_at = pd.to_datetime(df.created_at)
    # df.updated_at = (df.updated_at.apply(lambda x: x.split('T')[0]))
    # df.updated_at = pd.to_datetime(df.updated_at)
    return df


def create_data_frame_existing_lists_detail(slug):
    """
         Fetches details of a specific list and creates a DataFrame.

         Args:
             slug (int): Slug of the list to fetch details for.

         Returns:
             pd.DataFrame: DataFrame containing list details or None if slug is unavailable.
         """
    if not is_slug_available(slug):
        return None
    response = requests.get(url_base+f"lists/{slug}/entries", headers=HEADERS)
    data = response.json()
    if len(data) == 0:
        data = [{'id': "",
                 'domain': '',
                 'rating': '',
                 'created_at': '',
                 'updated_at': ''}, ]
    df_l = []
    for company in data :
        df_l.append([company['id'], company['domain'], company['rating'], company['created_at'], company['updated_at']])
    df = pd.DataFrame(df_l)
    df.columns = ['index', 'domain', 'rating', 'created_at', 'updated_at']
    df.set_index(['index'])
    df.created_at = (df.created_at.apply(lambda x: x.split('T')[0]))
    df.created_at = pd.to_datetime(df.created_at)
    df.updated_at = (df.updated_at.apply(lambda x: x.split('T')[0]))
    df.updated_at = pd.to_datetime(df.updated_at)
    return df


def create_data_frame_recommendation(slug):
    """
        Fetches recommendations for a specific list and creates a DataFrame.

        Args:
            slug (int): Slug of the list to fetch recommendations for.

        Returns:
            pd.DataFrame: DataFrame containing the recommendations.
        """
    response = requests.get(url_base + f"lists/{slug}/recommendations", headers=HEADERS)
    data = response.json()
    df_l = []
    for company in data:
        df_l.append([company['domain'], company['priority']])
    df = pd.DataFrame(df_l)
    df.columns = ['domain', 'priority', ]
    return df


def create_csv_created_list(tree):
    """
        Creates CSV files for selected lists and saves them to the selected directory.

        Args:
            tree (ttk.Treeview): Treeview widget containing the list selections.
        """
    path = Path(select_directory())
    list_slug = [element[0] for element in export_selection(tree)]
    if list_slug:
        for slug in list_slug:
            df = create_data_frame_existing_lists_detail(slug)
            df.to_csv(Path(path, f"{slug}.csv"), index=False)
    else:
        messagebox.showwarning(title="No selection", message="Please select at least one list")


def create_csv_recommendation(tree):
    """
       Creates CSV files for selected list recommendations and saves them to the selected directory.

       Args:
           tree (ttk.Treeview): Treeview widget containing the list selections.
       """
    path = Path(select_directory())
    list_slug = [element[0] for element in export_selection(tree)]
    if list_slug:
        for slug in list_slug:
            df = create_data_frame_recommendation(slug)
            df.to_csv(Path(path,f"{slug}_recommendation.csv"), index=False)
    else:
        messagebox.showwarning(title="No selection", message="Please select at least one list")


def export_selection(tree):
    """
        Exports the selected items from a treeview widget.

        Args:
            tree (ttk.Treeview): Treeview widget containing the list selections.

        Returns:
            list: List of selected items.
        """
    selection = []
    selected = tree.selection()

    if selected:
        for str_ind in selected:
            values = tree.item(str_ind, 'values')
            # Append empty list with slug, name and description for each selection
            selection.append([int(values[0]), values[1], values[2]])
    return selection


def open_window_create_new_list(window, tree):
    """
        Opens a window for creating a new list.

        Args:
            window (Tk): The main application window.
            tree (ttk.Treeview): Treeview widget containing the list selections.
            """
    create_new_list_window = customtkinter.CTkToplevel(window)
    create_new_list_window.title("Create a new list")
    create_new_list_window.geometry('600x320')
    create_new_list_window.resizable(width=False, height=False)
    create_new_list_window.configure(padx=1, pady=1)
    create_new_list_window.transient()  # place this window on top of the root window
    create_new_list_window.grab_set()

    customtkinter.CTkLabel(create_new_list_window, text="Name", text_color=('#062557', '#ffffff'),
                           font=("Calibri", 14,), height=10, )\
        .grid(row=0, column=0, sticky=W, padx=10, pady=2, columnspan=2)
    entry_name = customtkinter.CTkEntry(create_new_list_window, placeholder_text="Enter a name for your list", width=590)
    entry_name.grid(row=1, column=0, sticky=EW, columnspan=2, pady=(2,10), padx=3)

    customtkinter.CTkLabel(create_new_list_window, text="Description", text_color=('#062557', '#ffffff'),
                           font=("Calibri", 14,), height=10, ).grid(row=2, column=0, sticky=W, padx=10,
                                pady=2, columnspan=2, )
    entry_description = customtkinter.CTkTextbox(create_new_list_window, width=590, height=180)
    entry_description.grid(row=3, column=0, sticky=EW, columnspan=2, pady=(2,10), padx=3)

    button_create = customtkinter.CTkButton(create_new_list_window, text="Create",
                                            command=lambda: create_new_list(entry_name,
                                                                            entry_description,
                                                                            tree,
                                                                            create_new_list_window), width=100)
    button_create.grid(row=4, column=0, sticky=W, padx=2)

    button_quit = customtkinter.CTkButton(create_new_list, text="Close",
                                          command=lambda: quit_window(create_new_list_window), width=100)
    button_quit.grid(row=4, column=1, sticky=E, )


def create_new_list(entry_name, entry_description, tree, window):
    """
        Creates a new list using the provided name and description.

        Args:
            entry_name (CTkEntry): Entry widget containing the list name.
            entry_description (CTkTextbox): Textbox widget containing the list description.
            tree (ttk.Treeview): Treeview widget containing the list selections.
        """
    name = entry_name.get()
    description = entry_description.get("1.0", "end-1c")
    if not name:
        messagebox.showwarning(title="Missing domain", message="Please enter a valid domain")
        return
    if not description:
        messagebox.showwarning(title="Missing description", message="Please enter a description")
        return
    print(f"new_list created \n {name} \n {description}")

    data = {"name": name,
            "description": description
            }
    response = requests.post(url_base + "lists", headers=HEADERS, json=data)
    result=response.json()
    messagebox.showinfo(title="List created",
                        message=f"New list created \n Name :{name} \n Description : {description[:30]}")

    refresh_main_tree(tree)
    window.destroy()


def refresh_main_tree(tree):
    for i in tree.get_children():
        tree.delete(i)
    df = create_data_frame_all_existing_lists()
    for i, row in df.iterrows():
        tag_name = 'oddrow' if i % 2 == 0 else 'evenrow'
        tree.insert(parent='', index='end', iid=i, text="", values=list(row), tags=tag_name)


def view_list_detail(tree, window):
    """
       Opens a window to view the details of selected lists.

       Args:
           window (Tk): The main application window.
           tree (ttk.Treeview): Treeview widget containing the list selections.
       """
    global df_view

    list_selected_slug = export_selection(tree)
    print(list_selected_slug)
    if len(list_selected_slug) != 1:
        messagebox.showwarning(title="Selection error", message="Please select one and only one list")
    else:
        data_window = customtkinter.CTkToplevel(window)
        data_window.title("Data preview")
        data_window.geometry('760x420')
        data_window.resizable(width=False, height=False)
        data_window.configure(padx=1, pady=1)
        data_window.transient()  # place this window on top of the root window
        data_window.grab_set()

        # Create two frames, left for tree and right for buttons
        frame_left_d = customtkinter.CTkFrame(data_window, width=550, height=400)
        frame_left_d.grid_propagate(False)
        frame_left_d.grid(row=1, column=0, pady=3)

        frame_right_d = customtkinter.CTkFrame(data_window, width=199, height=400)
        frame_right_d.grid_propagate(False)
        frame_right_d.grid(row=1, column=1, pady=3)

        # Left frame content
        #       Headings with list information
        customtkinter.CTkLabel(frame_left_d, text=f"slug : {list_selected_slug[0][0]}",
                               text_color=('#062557', '#ffffff'),
                               font=("Calibri", 14, 'bold', 'roman', ), height=10, width=550,
                               justify='left', anchor=W).grid(row=0, column=0, padx=20, pady=3, sticky=W)

        customtkinter.CTkLabel(frame_left_d, text=f"Name : {list_selected_slug[0][1]}",
                               text_color=('#062557', '#ffffff'),
                               font=("Calibri", 14, 'bold', 'roman', ), height=10, width=550,
                               justify='left', anchor=W).grid(row=1, column=0, padx=20, pady=3, sticky=W)

        #       Create Tree for list details
        frame_tree = customtkinter.CTkScrollableFrame(frame_left_d, width=550, height=200)
        frame_tree.grid(row=2, column=0, pady=3)

        #       Configure tree style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#d3d3d3",
                        foreground="black",
                        rowheight=20,
                        fieldbackground="#ededed"
                        )
        style.map("Treeview",
                  background=[('selected', '#316B90')])

        #        Define tree columns
        tree_detail = ttk.Treeview(frame_tree, height=100)
        tree_detail.tag_configure('oddrow', background='#DFE9F0')
        tree_detail.tag_configure('evenrow', background='#E8F5FF')
        tree_detail.pack()

        # Dataframe
        df_view = create_data_frame_existing_lists_detail(list_selected_slug[0][0])
        # Formate columns
        tree_detail.column("#0", width=0, stretch=NO)
        cols = list(df_view.columns)
        tree_detail["columns"] = cols
        for i in cols:
            tree_detail.column(i, anchor="w")
            tree_detail.heading(i, text=i, anchor='w')

        tree_detail.column("index", width=60, stretch=NO)
        tree_detail.column("domain", width=240, stretch=NO)
        tree_detail.column("rating", width=100, stretch=NO)
        tree_detail.column("created_at", width=120, stretch=NO)
        tree_detail.column("updated_at", width=120, stretch=NO)

        for i, row in df_view.iterrows():
            tag_name = 'oddrow' if i % 2 == 0 else 'evenrow'
            tree_detail.insert(parent='', index='end', iid=i, text="", values=list(row), tags=tag_name)

        # Right frame : create Buttons
        # Add Entry
        button_add_entry = customtkinter.CTkButton(frame_right_d, text="Add entry",
                                                   command=lambda: open_window_add_new_entry(data_window,
                                                                                             list_selected_slug[0][0]),
                                                   width=150, )
        button_add_entry.grid(row=0, column=0, pady=(25, 3), padx=25)
        # Edit Entry
        button_edit_entry = customtkinter.CTkButton(frame_right_d, text="Edit entry",
                                                    command=lambda: open_window_edit_entry(list_selected_slug[0][0],
                                                                                           tree_detail, data_window),
                                                    width=150, )
        button_edit_entry.grid(row=1, column=0, pady=3, padx=25)
        # Delete Entry
        button_delete_entry = customtkinter.CTkButton(frame_right_d, text="Delete entry", command=export_selection,
                                                      width=150, state="disabled")
        button_delete_entry.grid(row=2, column=0, pady=3, padx=25)
        # Upload CSV
        button_upload_csv = customtkinter.CTkButton(frame_right_d, text="Upload CSV",
                                                    command=lambda: open_window_upload_csv(list_selected_slug[0][0],
                                                                                           data_window),
                                                    width=150, )
        button_upload_csv.grid(row=3, column=0, pady=3, padx=25)
        # Close window
        button_quit_tree = customtkinter.CTkButton(frame_right_d, text="Close window",
                                                   command=lambda: quit_window(data_window), width=150, )
        button_quit_tree.grid(row=4, column=0, pady=(20, 3), padx=25)


def open_window_add_new_entry(window, slug):
    """
      Opens a new window to add a new entry to a list.

      Args:
          window (CTk): The parent window from which this window is opened.
          slug (int): The unique identifier for the list to which the entry will be added.
      """
    # Create a new top-level window
    add_entry_window = customtkinter.CTkToplevel(window)
    add_entry_window.title("Add a new entry")
    add_entry_window.geometry('600x170')
    # data_window.resizable(width=False, height=False)
    add_entry_window.configure(padx=1, pady=1)
    add_entry_window.transient()  # place this window on top of the root window
    add_entry_window.grab_set()

    # Create and place the "Domain" label and entry field
    customtkinter.CTkLabel(add_entry_window, text="Domain", text_color=('#062557', '#ffffff'),
                           font=("Calibri", 14,), height=10, ).grid(row=0, column=0, sticky=W, padx=10,
                                                                    pady=2, columnspan=2)
    entry_domain = customtkinter.CTkEntry(add_entry_window, placeholder_text="Enter a domain", width=590)
    entry_domain.grid(row=1, column=0, sticky=EW, columnspan=2, pady=(2, 10), padx=3)
    # Create and place the "Rating" label and entry field
    customtkinter.CTkLabel(add_entry_window, text="Rating", text_color=('#062557', '#ffffff'),
                           font=("Calibri", 14,), height=10, ).grid(row=2, column=0, sticky=W, padx=10,
                                pady=2, columnspan=2, )
    entry_rating = customtkinter.CTkEntry(add_entry_window,
                                          placeholder_text="Enter a rating (float between 0 and 1.0", width=100)
    entry_rating.grid(row=3, column=0, sticky=EW, columnspan=2, pady=(2, 10), padx=3)

    # Create and place the "Add" and "Close" buttons
    button_add = customtkinter.CTkButton(add_entry_window, text="Add",
                                         command=lambda: add_entry(slug,entry_domain, entry_rating), width=100, )
    button_add.grid(row=4, column=0, sticky=W, padx=2)

    button_quit = customtkinter.CTkButton(add_entry_window, text="Close",
                                          command=lambda: quit_window(add_entry_window), width=100, )
    button_quit.grid(row=4, column=1, sticky=E, )


def add_entry(slug, entry_domain, entry_rating):
    """
       Adds a new entry to the list specified by the slug.

       Args:
           slug (str): The unique identifier for the list.
           entry_domain (CTkEntry): The entry widget containing the domain name.
           entry_rating (CTkEntry): The entry widget containing the rating.
       """
    domain = entry_domain.get()
    rating = entry_rating.get()
    # Check if the domain is provided
    if not domain:
        messagebox.showwarning(title="Missing domain", message="Please enter a valid domain")
    # Validate the rating and add the entry if valid
    if test_rating_validity(rating):
        print(f"new_list entry \n {domain} \n {rating} for slug {slug}")
        data = {
            "domain": domain,
            "rating": rating
            }
        # Send a POST request to add the entry
        response = requests.post(url_base + f"lists/{slug}/entries", headers=HEADERS, json=data)
        if response.json().get("detail") == 'domain invalid':
            messagebox.showwarning(title="Domain invalid",
                                   message=f"Domain {domain} is invalid and will not be added. Please double check and try again.")
        else:
            messagebox.showinfo(title="Entry added successfully",
                                message=f"The domain {domain} has been added to the list slug {slug}. ")
        # Clear the entry fields
        entry_rating.delete(0, END)
        entry_domain.delete(0, END)


def test_rating_validity(number):
    """
        Tests the validity of the rating.

        Args:
            number (str or float): The rating to validate.

        Returns:
            bool: True if the rating is valid, False otherwise.
        """
    try:
        # Convert to a float
        n = float(number)

        # Check if number is between 0 and 1
        if 0 <= n <= 1:
            return True
        else:
            messagebox.showwarning(title="Rating error", message="The number should be between 0 and 1")
            return False
    except ValueError:
        messagebox.showwarning(title="Rating error", message="Please enter a valid number")
        return False
    except TypeError:
        messagebox.showwarning(title="Rating error", message="Please enter a valid number")
        return False


def open_window_edit_entry(slug, tree, window):
    """
        Opens a window to edit the selected entry in the list.

        Args:
            slug (str): The unique identifier for the list.
            tree (Treeview): The treeview widget displaying the list entries.
            window (CTk): The parent window from which this window is opened.
        """
    # Get the selected entry from the treeview
    list_selected_entry = export_selection(tree)
    print(f"Edit {list_selected_entry}")
    # Ensure only one entry is selected
    if len(list_selected_entry)!=1:
        messagebox.showwarning(title="Selection error", message="Please select one and only one entry")
        return
    # Create a new top-level window for editing
    edit_entry_window = customtkinter.CTkToplevel(window)
    edit_entry_window.title(f"Edit entry for {list_selected_entry[0][1]}")
    edit_entry_window.geometry('400x170')
    edit_entry_window.resizable(width=False, height=False)
    edit_entry_window.configure(padx=1, pady=1)
    edit_entry_window.transient()  # place this window on top of the root window
    edit_entry_window.grab_set()
    # Display the current domain and rating
    customtkinter.CTkLabel(edit_entry_window, text=f"{list_selected_entry[0][1].upper()}",
                           text_color=('#062557', '#ffffff'), font=("Calibri", 14,"bold"), height=10, )\
        .grid(row=0, column=0, sticky=W, padx=10, pady=(2,20), columnspan=2)

    customtkinter.CTkLabel(edit_entry_window, text="Current rating", text_color=('#062557', '#ffffff'),
                           font=("Calibri", 14,), height=10, ).grid(row=1, column=0, sticky=W, padx=10, pady=2,)

    customtkinter.CTkLabel(edit_entry_window, text=f"{list_selected_entry[0][2]}", text_color=('#062557', '#ffffff'),
                           font=("Calibri", 14,), height=10, ).grid(row=1, column=1, sticky=W, padx=10, pady=2,)

    # Create a new entry field for the updated rating
    customtkinter.CTkLabel(edit_entry_window, text=f"New rating", text_color=('#062557', '#ffffff'),
                           font=("Calibri", 14,), height=10, ).grid(row=2, column=0, sticky=W, padx=10, pady=2,
                                                                    )
    new_entry_rating = customtkinter.CTkEntry(edit_entry_window, placeholder_text="New rating",
                                          width=100)
    new_entry_rating.grid(row=2, column=1, sticky=EW,  pady=(2, 10), padx=3)

    entry_id = list_selected_entry[0][0]
    new_entry_rating = new_entry_rating.get()

    # Create and place the "Edit" and "Close" buttons
    button_edit = customtkinter.CTkButton(edit_entry_window, text="Add",
                                         command=lambda: edit_entry(slug, entry_id, new_entry_rating), width=100, )
    button_edit.grid(row=5, column=0, sticky=W, padx=2)

    button_quit = customtkinter.CTkButton(edit_entry_window, text="Close", command=lambda: quit_window(edit_entry_window),
                                          width=100, )
    button_quit.grid(row=5, column=2, sticky=E, )


def edit_entry(slug, entry_id, rating):
    """
        Edits the entry in the list specified by the slug and entry ID.

        Args:
            slug (int): The unique identifier for the list.
            entry_id (int): The unique identifier for the entry.
            rating (float): The new rating to be applied.
        """
    # Validate the new rating and update the entry if valid
    if test_rating_validity(rating):
        data = {"rating": rating}
        response = requests.put(url_base + f"lists/{slug}/entries/{entry_id}", headers=HEADERS, json=data)


def delete_entry(tree):
    """
        Deletes the selected entry from the list.

        Args:
            tree (Treeview): The treeview widget displaying the list entries.
        """
    # Get the selected entry from the treeview
    list_selected_slug = export_selection(tree)
    # Ensure only one entry is selected
    if len(list_selected_slug) != 1:
        messagebox.showwarning(title="Selection error", message="Please select one and only one entry")
    else:
        # Confirm deletion with the user
        if messagebox.askokcancel(title="Suppression",
                                  message=f"Are you sure you want to delete the entry {list_selected_slug[0][0]} - {list_selected_slug[0][1]} ?"):
            print("ok")
            #response = requests.delete(url_base + f"lists/{list_selected_slug[0][0]}", headers=HEADERS)
        else:
            print("cancel")


def delete_list(tree):
    """
        Deletes the selected list.

        Args:
            tree (Treeview): The treeview widget displaying the lists.
        """
    # Get the selected list from the treeview
    list_selected_slug = export_selection(tree)
    # Ensure only one list is selected
    if len(list_selected_slug) != 1:
        messagebox.showwarning(title="Selection error", message="Please select one and only one list")
    else:
        # Confirm deletion with the user
        if messagebox.askokcancel(title="Suppression",
                                  message=f"Are you sure you want to delete the list {list_selected_slug[0][0]} -"
                                          f" {list_selected_slug[0][1]} ?"):
            # Send a DELETE request to remove the list
            response = requests.delete(url_base + f"lists/{list_selected_slug[0][0]}", headers=HEADERS)
            refresh_main_tree(tree)


def quit_window(window):
    """
      Closes the given window.

      Args:
          window (Toplevel): The window to close.
      """
    window.destroy()


def select_csv(label):
    """
        Opens a file dialog to select a CSV file and updates the label with the file path.

        Args:
            label (CTkEntry): The entry widget to display the selected file path.
        """
    # Open file dialog to select CSV file
    filename = filedialog.askopenfilename(initialdir="/", title="Select  csv file",filetypes=(("CSV files", "*.csv"),))
    # Update the label with the selected file path
    label.delete(0, 'end')
    label.insert(0, filename)
    get_data_from_csv()


def select_directory():
    """
      Opens a file dialog to select a directory and updates the default path.

      Returns:
          str: The path to the selected directory.
      """
    global default_path
    folder_selected = filedialog.askdirectory(title="Choose directory", initialdir=default_path)
    default_path = folder_selected
    return folder_selected


def open_window_upload_csv(slug, window):
    """
      Opens a window to upload data from a CSV file and associate it with a list.

      Args:
          slug (int): The unique identifier for the list.
          window (CTk): The parent window from which this window is opened.
      """
    global columns_, label_csv, combo_name, combo_rating

    columns_ = [""]

    # Create a new top-level window for uploading CSV data
    upload_window = customtkinter.CTkToplevel(window)
    upload_window.title(f"Upload data from CSV for list {slug}")
    upload_window.geometry('860x150')
    # data_window.resizable(width=False, height=False)
    upload_window.configure(padx=1, pady=1)
    upload_window.transient()  # place this window on top of the root window
    upload_window.grab_set()

    # Create and place the entry field and button for selecting CSV file
    label_csv = customtkinter.CTkEntry(upload_window, placeholder_text="Select Excel or csv file", font=("Roboto", 15),
                                       height=10, width=650, )

    button_csv = customtkinter.CTkButton(upload_window, text="Select file", command=lambda: select_csv(label_csv), width=150, )
    button_csv.grid(row=1, column=0, sticky=W, pady=3, padx=3)

    label_csv = customtkinter.CTkEntry(upload_window, placeholder_text="Select Excel or csv file", font=("Roboto", 15),
                                       height=10, width=650, )
    label_csv.bind('<FocusOut>', lambda x: get_data_from_csv())
    label_csv.grid(row=1, column=1, sticky=EW, columnspan=2, pady=3, padx=5)

    # Create and place the labels and dropdowns for selecting CSV columns
    customtkinter.CTkLabel(upload_window, text=f"Choose column for Domain", text_color=('#062557', '#ffffff'),
                           font=("Calibri", 14,), height=10, ).grid(row=2, column=0, sticky=W, padx=10, pady=2,)

    combo_name = customtkinter.CTkOptionMenu(upload_window, values=columns_,)
    combo_name.grid(row=2, column=1, sticky=EW, pady=3)

    customtkinter.CTkLabel(upload_window, text=f"Choose column for Rating", text_color=('#062557', '#ffffff'),
                           font=("Calibri", 14,), height=10, ).grid(row=3, column=0, sticky=W, padx=10, pady=2, )

    combo_rating = customtkinter.CTkOptionMenu(upload_window, values=columns_,)
    combo_rating.grid(row=3, column=1, sticky=EW, pady=3)

    # Create and place the "Upload" and "Close" buttons
    button_upload = customtkinter.CTkButton(upload_window, text="Upload",
                                          command=lambda: upload_csv(slug,combo_name.get(),
                                                                     combo_rating.get()), width=100, )
    button_upload.grid(row=5, column=0, sticky=W, padx=2)

    button_quit = customtkinter.CTkButton(upload_window, text="Close",
                                          command=lambda: quit_window(upload_window),
                                          width=100, )
    button_quit.grid(row=5, column=2, sticky=E, )


def get_data_from_csv():
    """
        Reads the selected CSV file and updates the available columns in the dropdown menus.
        """
    global df_csv
    if label_csv.get():
        filename, file_extension = os.path.splitext(label_csv.get())
        if file_extension == '.csv':
            df_csv = pd.read_csv(label_csv.get())
            columns_csv = df_csv.columns
            combo_name.configure(values=columns_csv)
            combo_rating.configure(values=columns_csv)
            combo_name.set(columns_csv[1])
            combo_rating.set(columns_csv[2])
        else:
            messagebox.showwarning(title="Unvalid file", message="Select CSV file  only")


def upload_csv(slug, col_domain, col_rating):
    """
        Validates and uploads data from the CSV file to the specified list.

        Args:
            slug (int): The unique identifier for the list.
            col_domain (str): The name of the column in the CSV file containing domain names.
            col_rating (str): The name of the column in the CSV file containing ratings.
        """
    # Check if the field domain is not Nan for each row
    if bool(df_csv[col_domain].any()):
        messagebox.showwarning(title="Domain empty",
                               message=f"The column {col_domain} has empty value. Unable to upload")
        return


    # Validate all ratings in the selected column
    for rating in df_csv[col_rating].to_list():
        if not test_rating_validity(rating):
            return
    # Add new entries from the CSV file to the list
    for i, row in df_csv.iterrows():
        if row[col_domain] not in df_view.domain.to_list():
            print(f"add {row[col_domain]} - {row[col_rating]}")
            add_entry_from_csv(slug, row[col_domain], row[col_rating])
    # Update existing entries in the list with data from the CSV file
    for i, row in df_view.iterrows():
        if row['domain'] in df_csv[col_domain].to_list():
            if row['rating'] != (df_csv[df_csv[col_domain] == row['domain']][col_rating].values[0]):
                new_rating=(df_csv[df_csv[col_domain] == row['domain']][col_rating].values[0])
                print(f"update {row['domain']} - {new_rating}")
                edit_entry(slug, row['index'], new_rating)


def add_entry_from_csv(slug, domain, rating):
    """
        Adds a new entry from the CSV file to the specified list.

        Args:
            slug (int): The unique identifier for the list.
            domain (str): The domain name to add.
            rating (float): The rating associated with the domain.
        """
    data = {
        "domain": domain,
        "rating": rating
        }
    # Send a POST request to add the entry
    response = requests.post(url_base + f"lists/{slug}/entries", headers=HEADERS, json=data)
    if response.json().get("detail") == 'domain invalid':
        messagebox.showwarning(title="Domain invalid",
                               message=f"Domain {domain} is invalid and will not be added. Please double check and try again.")


