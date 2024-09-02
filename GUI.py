from script import *


# GUI configuration
customtkinter.set_appearance_mode("system")
#customtkinter.set_appearance_mode("dark")

customtkinter.set_default_color_theme("dark-blue")



# Gui construction
window = customtkinter.CTk()

window.title("Startup Radar Interface")
#window.iconbitmap("Add your icon")
window.geometry('1200x405')
window.resizable(width=False, height=False)
window.configure(padx=1, pady=1)




# frame0 = customtkinter.CTkFrame(window, width=1199, height=15, fg_color=('#D6D9E1','#2C2D2E'))
# frame0.pack_propagate(False)
# frame0.grid(row=0, column=0, pady=3, columnspan=2)

frame1L = customtkinter.CTkFrame(window, width=1000, height=400)
frame1L.grid_propagate(False)
frame1L.grid(row=1, column=0, pady=3)



frame1R = customtkinter.CTkFrame(window, width=199, height=400)
frame1R.grid_propagate(False)
frame1R.grid(row=1, column=1, pady=3)




label_list = customtkinter.CTkLabel(frame1L, text="List of our Existing lists", text_color=('#062557','#ffffff'),
                                    font=("Calibri", 19, 'bold', 'roman', 'underline'), height=10, width=999, justify='center')
label_list.grid(row=0, column=0, sticky=EW, )


############## TREE CONSTRUCTION
frame_tree = customtkinter.CTkScrollableFrame(frame1L,  height=350, width=1000)
frame_tree.grid(row=1, column=0, sticky=EW, pady=3)

# Configure tree style
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

# Define columns
tree = ttk.Treeview(frame_tree, height=390)
tree.tag_configure('oddrow', background='#DFE9F0')
tree.tag_configure('evenrow', background='#E8F5FF')

tree.pack()
# Formate columns
tree.column("#0", width=0, stretch=NO)
cols = list(df_existing_list.columns)
tree["columns"] = cols
for i in cols:
    tree.column(i, anchor="w", width=250)
    tree.heading(i, text=i, anchor='w')

tree.column("id", width=40, stretch=NO)
tree.column("name", width=240, stretch=NO)
tree.column("description", width=620, stretch=NO)
tree.column("created_at", width=150, stretch=NO)
tree.column("updated_at", width=150, stretch=NO)

for i, row in df_existing_list.iterrows():
    tag_name = 'oddrow' if i % 2 == 0 else 'evenrow'
    tree.insert(parent='', index='end', iid=i, text="", values=list(row), tags=tag_name)


# Manage lists buttons
label_list = customtkinter.CTkLabel(frame1R, text="MANAGE LISTS", text_color=('#062557','#ffffff'),
                                    font=("Calibri", 17, 'bold', 'roman', 'underline'), height=10, width=150, justify='center')
label_list.grid(row=0, column=0, sticky=EW, pady=(20,3), padx=25)

button_create_new_list = customtkinter.CTkButton(frame1R, text="Create new list",
                                                 command=lambda: open_window_create_new_list(window,tree), width=150,)
button_create_new_list.grid(row=1, column=0, pady=3, padx=25)

button_view_detail_list = customtkinter.CTkButton(frame1R, text="View detail list",
                                                  command=lambda: view_list_detail(tree,window), width=150,)
button_view_detail_list.grid(row=2, column=0, pady=3, padx=25)

button_view_delete_list = customtkinter.CTkButton(frame1R, text="Edit list",
                                                  command=lambda: open_window_edit_list(window,tree), width=150,)
button_view_delete_list.grid(row=3, column=0, pady=3, padx=25)


button_view_delete_list = customtkinter.CTkButton(frame1R, text="Delete list",
                                                  command=lambda: delete_list(tree), width=150,)
button_view_delete_list.grid(row=4, column=0, pady=3, padx=25)

# Generate CSV buttons
label_csv = customtkinter.CTkLabel(frame1R, text="GENERATE CSV", text_color=('#062557','#ffffff'),
                                    font=("Calibri", 17, 'bold', 'roman', 'underline'), height=10, width=150, justify='center')
label_csv.grid(row=5, column=0, sticky=EW,  padx=25, pady=(20,3))


button_create_csv = customtkinter.CTkButton(frame1R, text="Existing list",
                                            command=lambda: create_csv_created_list(tree), width=150,)
button_create_csv.grid(row=6, column=0, pady=3, padx=25)

button_create_csv_recommendation = customtkinter.CTkButton(frame1R, text="Recommendation",
                                                           command=lambda: create_csv_recommendation(tree), width=150,)
button_create_csv_recommendation.grid(row=7, column=0, pady=3, padx=25)

button_create_csv_news = customtkinter.CTkButton(frame1R, text="What's new?",
                                                           command=lambda: history_recommendation(tree), width=150,)
button_create_csv_news.grid(row=8, column=0, pady=3, padx=25)

button_quit = customtkinter.CTkButton(frame1R, text="Quit", command=lambda: quit_window(window),  width=150, )
button_quit.grid(row=9, column=0, pady=(30,3), sticky='s', padx=25)


window.mainloop()

