
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item for QUT's teaching unit
#  IFB104, "Building IT Systems", Semester 1, 2023.  By submitting
#  this code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#  Put your student number here as an integer and your name as a
#  character string:
#
student_number = 11557761
student_name   = "Bailey King"
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  All files submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assessment Task 2 Description----------------------------------#
#
#  In this assessment task you will combine your knowledge of Python
#  programming, HTML-style mark-up languages, pattern matching,
#  database management, and Graphical User Interface design to produce
#  a robust, interactive "app" that allows its user to view and save
#  data from multiple online sources.
#
#  See the client's briefings accompanying this file for full
#  details.
#
#  Note that this assessable assignment is in multiple parts,
#  simulating incremental release of instructions by a paying
#  "client".  This single template file will be used for all parts,
#  together with some non-Python support files.
#
#--------------------------------------------------------------------#



#-----Set up---------------------------------------------------------#
#
# This section imports standard Python 3 modules sufficient to
# complete this assignment.  Don't change any of the code in this
# section, but you are free to import other Python 3 modules
# to support your solution, provided they are standard ones that
# are already supplied by default as part of a normal Python/IDLE
# installation.
#
# However, you may NOT use any Python modules that need to be
# downloaded and installed separately, such as "Beautiful Soup" or
# "Pillow", because the markers will not have access to such modules
# and will not be able to run your code.  Only modules that are part
# of a standard Python 3 installation may be used.

# A function for exiting the program immediately (renamed
# because "exit" is already a standard Python function).
from sys import exit as abort

# A function for opening a web document given its URL.
# [You WILL need to use this function in your solution,
# either directly or via the "download" function below.]
from urllib.request import urlopen

# Some standard Tkinter functions.  [You WILL need to use
# SOME of these functions in your solution.]  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.  (NB: Although you can import individual widgets
# from the "tkinter.tkk" module, DON'T import ALL of them
# using a "*" wildcard because the "tkinter.tkk" module
# includes alternative versions of standard widgets
# like "Label" which leads to confusion.  If you want to use
# a widget from the tkinter.ttk module name it explicitly,
# as is done below for the progress bar widget.)
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding occurrences of a pattern defined
# via a regular expression.  [You do not necessarily need to
# use these functions in your solution, because the problem
# may be solvable with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.]
from re import *

# A function for displaying a web document in the host
# operating system's default web browser (renamed to
# distinguish it from the built-in "open" function for
# opening local files).  [You WILL need to use this function
# in your solution.]
from webbrowser import open as urldisplay

# All the standard SQLite database functions.  [You WILL need
# to use some of these in your solution.]
from sqlite3 import *

#
#--------------------------------------------------------------------#



#-----Validity Check-------------------------------------------------#
#
# This section confirms that the student has declared their
# authorship.  You must NOT change any of the code below.
#

if not isinstance(student_number, int):
    print('\nUnable to run: No student number supplied',
          '(must be an integer)\n')
    abort()
if not isinstance(student_name, str):
    print('\nUnable to run: No student name supplied',
          '(must be a character string)\n')
    abort()

#
#--------------------------------------------------------------------#



#-----Supplied Function----------------------------------------------#
#
# Below is a function you can use in your solution if you find it
# helpful.  You are not required to use this function, but it may
# save you some effort.  Feel free to modify the function or copy
# parts of it into your own code.
#

# A function to download and save a web document.  The function
# returns the downloaded document as a character string and
# optionally saves it as a local file.  If the attempted download
# fails, an error message is written to the shell window and the
# special value None is returned.  However, the root cause of the
# problem is not always easy to diagnose, depending on the quality
# of the response returned by the web server, so the error
# messages generated by the function below are indicative only.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * incognito - If this parameter is True the Python program will
#      try to hide its identity from the web server. This can
#      sometimes be used to prevent the server from blocking access
#      to Python programs. However we discourage using this
#      option as it is both unreliable and unethical to
#      override the wishes of the web document provider!
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'downloaded_document',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             incognito = False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request
    import ssl # I need this to bypass a certificate error..

    # Import an exception sometimes raised when a web server
    # denies access to a document
    from urllib.error import HTTPError

    # Import an exception raised when a web document cannot
    # be downloaded due to some communication error
    from urllib.error import URLError

    # Open the web document for reading (and make a "best
    # guess" about why if the attempt fails, which may or
    # may not be the correct explanation depending on how
    # well behaved the web server is!)
    try:
        if incognito:
            # Pretend to be a web browser instead of
            # a Python script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                               'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                               'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246')
            print("Warning - Request does not reveal client's true identity.")
            print("          This is both unreliable and unethical!")
            print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url 
        # Disable certificate verification
        context = ssl._create_unverified_context()
        web_page = urlopen(request, context=context)
    except ValueError as message: # probably a syntax error
        print("\nCannot find requested document '" + url + "'")
        print("Error message was:", message, "\n")
        return None
    except HTTPError as message: # possibly an authorisation problem
        print("\nAccess denied to document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None
    except URLError as message: # probably the wrong server address
        print("\nCannot access web server at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None
    except Exception as message: # something entirely unexpected
        print("\nSomething went wrong when trying to download " + \
              "the document at URL '" + str(url) + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set, errors='ignore')
    except UnicodeDecodeError as message:
        print("\nUnable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters")
        print("Error message was:", message, "\n")
        return None
    except Exception as message:
        print("\nSomething went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("\nUnable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution below.
#

# Create the main window
task_2_main_window = Tk()

### Your code goes here ###
#

import _tkinter

# defining url links as variables
radio_url ='https://www.abc.net.au/triplej/featured-music'
tv_url = 'https://10play.com.au/'
ufc_url = 'https://www.espn.com/mma/schedule/_/league/ufc'

# defining the event soruce names
radio_name = 'Radio - Triple J'
tv_name = 'TV - Channel 10'
ppv_name = 'PPV - UFC events'

# Using the 'download' fucntion that has so nicely been provided to get the info from the webpages
download(url = radio_url,
             target_filename = 'downloaded_radio_document',
             filename_extension = 'txt',
             save_file = True,
             char_set = 'UTF-8',
             incognito = False)

download(url = tv_url,
             target_filename = 'downloaded_tv_document',
             filename_extension = 'txt',
             save_file = True,
             char_set = 'UTF-8',
             incognito = True)

download(url = ufc_url,
             target_filename = 'downloaded_UFC_document',
             filename_extension = 'txt',
             save_file = True,
             char_set = 'UTF-8',
             incognito = True)

# -----
# Define a function to handle data extraction from files
def extract_data(file_path, pattern):
    try:
        file = open(file_path, 'r', encoding='utf-8')
        file_contents = file.read()
        data = findall(pattern, file_contents)
        file.close()
        if data:
            # Replace HTML entities with their corresponding characters
            data[0] = data[0].replace('&amp;', '&')
            data[0] = data[0].replace('&lt;', '<')
            data[0] = data[0].replace('&gt;', '>')
            data[0] = data[0].replace('&quot;', '"')
            data[0] = data[0].replace('&apos;', "'")
            data[0] = data[0].replace('&nbsp;', ' ')
            return data[0]
        else:
            return None
    except (FileNotFoundError, UnicodeDecodeError) as error:
        print(f"Error occurred while reading file '{file_path}': {error}")
        return None
    
# Define the file paths and regex patterns
radio_file_path = 'downloaded_radio_document.txt'
radio_pattern_title = r'<span class="KeyboardFocus_keyboardFocus__uwAUh"[^>]*>([^<]+)'
radio_pattern_artist = r'<p class="Typography_base__k7c9F TracklistCard_secondaryTitle__e1gyh[^>]*>([^<]+)'

UFC_file_path = 'downloaded_UFC_document.txt'
UFC_pattern_title = r'<a class="AnchorLink" tabindex="0" href="[^"]+">([UFC][^<]+)</a>'
UFC_pattern_location = r'<td class="location__col Table__TD"><div>(.*?)</div>'
UFC_pattern_date = r'<td class="date__col Table__TD"><span class="date__innerCell">(.*?)</span></td>'

tv_file_path = 'downloaded_tv_document.txt'
tv_pattern_title = r'"schedule":{"NSW":{"title":"(.*?)"'


# Extract data from files with error handling
song_title = extract_data(radio_file_path, radio_pattern_title)
song_artist = extract_data(radio_file_path, radio_pattern_artist)
event_title = extract_data(UFC_file_path, UFC_pattern_title)
event_location = extract_data(UFC_file_path, UFC_pattern_location)
event_date = extract_data(UFC_file_path, UFC_pattern_date)
program_title = extract_data(tv_file_path, tv_pattern_title)
tv_pattern_starttime = r':"' + program_title + '".*?T(.*?):00Z' # this has to sit down here otherwise it won't run and cause an error
program_starttime = extract_data(tv_file_path, tv_pattern_starttime)

# Perform necessary data manipulations and error handling
if program_starttime:
    try:
        hours, minutes = program_starttime.split(":")
        hours = int(hours) - 14
        hours = hours % 24
        hours_str = str(hours).zfill(2)
        new_start_time = hours_str + ":" + minutes
        program_starttime = new_start_time
    except ValueError as error:
        print(f"Error occurred while manipulating start time: {error}")
else:
    print("Error: Start time not found.")

#-----
# Introduce a variable to link the radio buttons 
button_chosen = IntVar()

# I'll need these defined for DB
## Below commented out because some STR error
## radio_summary = 'Song under review is ' + '"' + song_title + '"' + ' by ' + song_artist 

tv_summary = 'TV show under review is ' + '"' + program_title + '"' + ' (Program started at: ' + program_starttime + ')'

ppv_summary = 'Event under review is ' + '"' + event_title + '"' + ' at ' + event_location + ' on ' + event_date

#-----
# Defining functions that display results in text area.
#
# Global variable
summary_shown = False

radio_selected = 'Radio - Triple J selected'
tv_selected = 'TV - ABC broadcast selected'
ppv_selected = 'PPV - UFC Events 2023 selected'


def initial_text():
    display_text.insert(END, status_txt)
    
def display_radio():
    display_text.delete(0.0, END)
    display_text.insert(END, radio_selected)
    select_radio_button()

def display_tv():
    display_text.delete(0.0, END)
    display_text.insert(END, tv_selected)
    select_radio_button()

def display_ufc():
    display_text.delete(0.0, END)
    display_text.insert(END, ppv_selected)
    select_radio_button()

def select_radio_button():
    global summary_shown
    summary_shown = False

def show_summary():
    global summary_shown
    summary_shown = True
    
    display_text.delete(0.0, END)
    if button_chosen.get() == 1:
        display_text.insert(END, radio_summary)
    elif button_chosen.get() == 2:
        display_text.insert(END, tv_summary)
    elif button_chosen.get() == 3:
        display_text.insert(END, ppv_summary)
    else:
         display_text.insert(END, 'ERROR: No media source selected', 'error')
        
def show_details():
    display_text.delete(0.0, END)
    if button_chosen.get() == 1:
        display_text.insert(END, 'Showing song details in your web browser...\n')
        display_text.insert(END, radio_url)
        urldisplay(radio_url)
    elif button_chosen.get() == 2:
        display_text.insert(END, 'Showing progam details in your web browser...\n')
        display_text.insert(END, tv_url)
        urldisplay(tv_url)
    elif button_chosen.get() == 3:
        display_text.insert(END, 'Showing event details in your web browser...\n')
        display_text.insert(END, ufc_event_url)
        urldisplay("espn.com" + ufc_details_url[0])
    else:
        display_text.insert(END, 'ERROR: No media source selected', 'error')

def display_review():
    global summary_shown
    global value
    display_text.delete(0.0, END)

    # Get the value from the spinbox
    value = spinbox_var.get()

    # using python to interact with a database (SQLite)
    # Create a connection to the database
    connection = connect(database = 'media_reviews.db')

    # Get a local view of the database
    media_reviews_db = connection.cursor()

    # Execute the ALTER TABLE statement to drop the unique index
    media_reviews_db.execute("DROP INDEX IF EXISTS unique_index_name")
    # Check if a radio button has been selected and summary has been shown
    if not validate_spinbox(value):
        return  
    elif not summary_shown:
        display_text.insert(END, "ERROR: Please select an Entertainment option and and click 'Show summary' before saving the review.", 'error')
        return
    elif spinbox_var.get() == 0:
        display_text.insert(END, 'ERROR: No value was given, please chose a value.', 'error')
        return
    try:
        if button_chosen.get() == 1:
            media_reviews_db.execute('''INSERT into reviews (review, event_source, event_summary, url)
                                        VALUES (?, ?, ?, ?);''', (value, radio_name, radio_summary, radio_url )) # Execute an SQL scrip, query 
            connection.commit()
            display_text.insert(END, 'Review saved to database...' )
        elif button_chosen.get() == 2:
            media_reviews_db.execute('''INSERT into reviews (review, event_source, event_summary, url)
                                        VALUES (?, ?, ?, ?);''', (value, tv_name, tv_summary, tv_url ))
            connection.commit()
            display_text.insert(END, 'Review saved to database...' )
        elif button_chosen.get() == 3:
            media_reviews_db.execute('''INSERT into reviews (review, event_source, event_summary, url)
                                        VALUES (?, ?, ?, ?);''', (value, ppv_name, ppv_summary, ufc_url ))
            connection.commit()
            display_text.insert(END, 'Review saved to database...' )
        else:
            display_text.insert(END, 'ERROR: Cannot find database file media_reviews', 'error')
            
    # Error exception to keep from crashing
    except OperationalError as operation_error:
        if str(operation_error) == 'database is locked':
            display_text.insert(END, 'ERROR: Database is locked. Please try again later.', 'error')
        else:
            # Handle other operational errors
            display_text.insert(END, "An error occurred: OperationalError", error)
    except NameError as name_error:
        if str(name_error) == "name 'value' is not defined":
            display_text.insert(END, 'ERROR: No value was given, please chose a value.', 'error')
        else:
            display_text.insert(END, "An error occurred: NameError", error)
    except IntegrityError as integrity_error:
        if str(integrity_error) == "UNIQUE constraint failed:":
            display_text.insert(END, 'ERROR: UNIQUE constraint error', 'error')
        else:
            display_text.insert(END, "An error occurred: Data given has already been entered", 'error')
    #else:
        
                
    # Close the database
    media_reviews_db.close()
    connection.close()
    
# Just gonna shorten the variable for main window
window = task_2_main_window

#-----
# Define global constants
bg_colour = 'lemon chiffon'
border_style = 'groove'
border_margin = (10, 0)
title_margin = (20,0)

#-----
# Define font size
title_font = ('Arial', 18)
title_colour = 'dimgrey'
button_font = ('Arial', 12)

#-----
# Create main window 
window.geometry('730x400')
window.configure(bg= bg_colour)
window.title('BK Media Reviews!')

#-----
# Create the image
img = PhotoImage(file="image1.png")
img = img.subsample(2) # Resize image to half original size
Label(window, image=img, border = 3, relief = 'solid').\
                  grid(row = 0, column = 0, padx = 10, pady = 10,sticky = W)

txt_below_img = Label(text = "BK'S MEDIA REVIEW!", bg = bg_colour, width = 20, font =('Arial', 20)).grid(row = 1, column = 0, padx = 0, pady = (0,50))

#-----
# Contents for all 3 sections 
# Create borders 
review_stat_border = Label(window, width = 47, height = 6, borderwidth = 3,
                   relief  = border_style, bg = bg_colour).\
                   grid(row = 0, column = 1, padx = border_margin, pady = (0 ,210), sticky = W)

entertainment_border = Label(window, width = 50, height = 9, borderwidth = 3,
                   relief  = border_style, bg = bg_colour).\
                   grid(row = 0, column = 1, padx = border_margin, pady = (55, 0), sticky = W)
                
num_stars_border = Label(window, width = 27, height = 4, borderwidth = 3,
                   relief  = border_style, bg = bg_colour).\
                   grid(row = 0, column = 1, padx = border_margin, pady = (295, 0), sticky = W)
# Create titles  
review_status_title = Label(window, text = 'Review status',
                   fg = title_colour, bg = bg_colour ,font = title_font).\
                   grid(row = 0, column = 1, padx = (title_margin), pady = (0, 305), sticky = W)
enternaiment_title = Label(window, text = 'Entertainment Options',
                   fg = title_colour, bg = bg_colour ,font = title_font).\
                   grid(row = 0, column = 1, padx = (title_margin), pady = (0,80), sticky = W)
num_stars_title = Label(window, text = 'Number of stars',
                   fg = title_colour, bg = bg_colour ,font = title_font).\
                   grid(row = 0, column = 1, padx = (title_margin), pady = (235,0), sticky = W)

#-----
# Create text box to display information from user input
display_text = Text(window, width = 28, height = 3,
                    wrap = WORD, bg = bg_colour, font = ('black'),
                    border = 0, state = NORMAL, takefocus = False)
display_text.grid(row = 0, column = 1, padx = title_margin, pady = (0,210),
                    sticky = W)

# Configure the tag for red text
display_text.tag_configure("error", foreground="red")

#-----
# Create frame to hold three radio buttons
option_buttons = Frame(window, bg = bg_colour)
option_buttons.grid(row =0, column = 1, padx = title_margin, pady = (40,0),
                    sticky = W)

#-----
# Define and position the radio buttons
radio_button = Radiobutton(option_buttons, text = radio_name,
                      variable = button_chosen, value = 1, font = button_font, bg= bg_colour,
                      command = display_radio, takefocus = False).\
                      grid(row = 0, sticky = W)
channel_button = Radiobutton(option_buttons, text = tv_name,
                      variable = button_chosen, value = 2, font = button_font, bg= bg_colour,
                      command = display_tv, takefocus = False).\
                      grid(row = 1, sticky = W)
ppv_button = Radiobutton(option_buttons, text = ppv_name,
                      variable = button_chosen, value = 3, font = button_font, bg= bg_colour,
                      command = display_ufc, takefocus = False).\
                      grid(row = 2, sticky = W)
#-----
# Create buttons to show summary and details and postion them 
summary_button = Button(window, width = 13, text = 'Show summary',
                      activeforeground = 'red', font = ('Arial', 12),
                      command = show_summary, takefocus = False).\
                      grid(row = 0, column = 1, padx = 220, pady = 10, sticky = W)
details_button = Button(window, width = 10, text = 'Show details',
                      activeforeground = 'red',font = ('Arial', 12),
                      command = show_details, takefocus = False).\
                      grid(row = 0, column = 1, padx = 220, pady = (90,0), sticky = W)

# Function is to validate the values in the spinbox 
def validate_spinbox(value):
    try:
        value = int(value)
        if value < 1 or value > 5:
            raise ValueError
    except (ValueError, TypeError):
        display_text.delete(0.0, END)
        display_text.insert(END, 'ERROR: Please enter a valid number between 1 and 5.', 'error')
        return False
    return True

#-----
# Create spinbox with max int of 5
spinbox_var = StringVar()  # Create a IntVar to track the spinbox value
spinbox_var.set(0)      # Set the initial value of spinbox

# Create spinbox widget
spinbox = Spinbox(window, from_ = 0, to = 5, textvariable = spinbox_var,
                  command = lambda: validate_spinbox(spinbox_var.get()),
                  width = 2, font =('Arial', 14)).\
                  grid(row = 0, column = 1, padx = title_margin, pady = (305,0), sticky = W)
                       
#-----
# Create Save review button
save_review = Button(window, width = 10, text = 'Save review',
                  activeforeground = 'red', font = ('Arial', 12),
                  command = display_review, takefocus = False).\
                  grid(row = 0, column = 1, padx = (75,0), pady = (305,0), sticky = W)

#-----
# Set inital text for the user status & call function
status_txt = "Please select an entertainment option ..."
initial_text()
                       
# Start the event loop to detect user inputs
window.mainloop()
