#Thomas R
#Final Project
#This Program should read game data charts. specifically the game data provided in the project details of this assignment 
#This program was written by me with the assistance of Windows CoPilot working hand in hand,
#it should serve as an example that with Human oversight AI is capable of working for developers in a meaningful way 
  

import os
#imports the os module for filesystem operations

import csv
#imports the csv module for CSV parsing

import sys
#imports the sys module for graceful exit handling

# defines a function called setDataFilePath
def setDataFilePath():

    # declares that the function will modify the module-level variable
    global USER_SPECIFIED_PATH

    # prints the action header for setting the CSV path
    print("\nSet CSV File Path")

    # prints a separator for clarity
    print("------------------------------------------------------------")

    # prints instructions for entering the path
    print("Enter the full or relative path to your steamcharts.csv file.")

    # prints instructions for clearing the custom path
    print("Press Enter to clear the current custom path and use default filenames.")

    # prompts the user to enter the path and strips whitespace
    path = input("Path (include filename, e.g., C:/.../Full steamcharts.csv): ").strip()

    # if statement checking that a path was provided
    if path:

        # assigns the provided path to the module-level variable
        USER_SPECIFIED_PATH = path

        # prints confirmation that the custom path was set
        print(f"Custom CSV path set to: '{USER_SPECIFIED_PATH}'")

    # else branch when no path was provided
    else:

        # clears the user-specified path
        USER_SPECIFIED_PATH = ''

        # prints confirmation that the custom path was cleared
        print("Custom CSV path cleared. The program will try default filenames.")

#defines a function called main
def main():
    # declares that the function will modify the module-level variable
    global USER_SPECIFIED_PATH

    # prints a short startup banner
    print("Steam Games Data Analysis System")

    # prompts the user for the CSV path at startup and stores it
    USER_SPECIFIED_PATH = input("Enter full or relative path to steamcharts.csv (Enter to use defaults): ").strip()

    # clears the terminal screen for a clean UI
    clear_screen_ansi()

    # loads data using the provided path or default candidates
    steam_dictionary = getSteamData()

    # prints diagnostics so the user can confirm data loaded
    print_load_diagnostics(steam_dictionary)

    # while loop for the main interactive menu
    while True:
        # gets a validated menu choice from the user
        choice = getMenuChoice()
        # if statement handling quit selection
        if choice == 'Q':
            # prints a farewell message
            print("\nGoodbye.")
            # breaks out of the main loop to end the program
            break
        # if statement handling option 1: reload data
        if choice == 1:
            # reloads the steam data using current path settings
            steam_dictionary = getSteamData()
            # prints diagnostics after reloading
            print_load_diagnostics(steam_dictionary)
        # elif statement handling option 2: find a game
        elif choice == 2:
            # calls the search helper to find matching entries
            found = findASpecificGame(steam_dictionary)
            # if statement computing a short average summary for matches
            if found:
                # initializes a list to collect numeric avg_players values
                nums = []
                # for loop iterating through found entries
                for e in found:
                    # retrieves the avg_players string and strips whitespace
                    s = e.get('avg_players', '').strip()
                    # try block converting avg_players to float
                    try:
                        # appends numeric values to the list
                        nums.append(float(s))
                    # except block ignoring non-numeric or missing values
                    except Exception:
                        # passes on values that cannot be converted
                        pass
                # if statement printing the average for the first matched game
                if nums:
                    # prints the average players for the matched game
                    print(f"\nAverage players for '{found[0].get('gameName','Unknown')}': {sum(nums)/len(nums):.2f}")
                # pauses before returning to the menu
                pause()
        # elif statement handling option 3: list games by month
        elif choice == 3:
            # calls the month-filter helper to display matching games
            getGamesFromASpecificMonth(steam_dictionary)
        # elif statement handling option 4: show average players
        elif choice == 4:
            # calls the helper to compute and display average player count
            getAveragePlayerCount(steam_dictionary)
        # elif statement handling option 5: most popular game
        elif choice == 5:
            # calls the helper to find and display the most popular game
            findMostPopularGame(steam_dictionary)
        # elif statement handling option 6: list all game names
        elif choice == 6:
            # calls the helper to list game names with a sample and count
            listAllGameNames(steam_dictionary)
        # elif statement handling option 7: generate a report
        elif choice == 7:
            # calls the report generation helper that supports all/one game
            generateGameReport(steam_dictionary)
        # elif statement handling option 8: write report to file
        elif choice == 8:
            # calls the helper to write the all-games report to disk
            writeReportToFile(steam_dictionary)
        # elif statement handling option 9: set/change CSV path
        elif choice == 9:
            # calls the helper to set or change the CSV file path
            setDataFilePath()
        # else branch handling unrecognized menu choice
        else:
            # prints a message when an unrecognized menu choice is encountered
            print("Unrecognized menu choice. Please try again.")

#module-level variable to hold a user-specified CSV path
USER_SPECIFIED_PATH = ''

#list of default candidate filenames to try when loading
DEFAULT_CANDIDATES = ['steamcharts.csv', 'Full steamcharts.csv']

#defines a function called clear_screen_ansi
def clear_screen_ansi():
   
    #prints ANSI codes to clear the terminal screen for the user
    print("\033[2J\033[H", end='')

#defines a function called pause
def pause():
   
    #prints a prompt asking the user to press Enter to continue
    input("\nPress Enter to return to the main menu...")

#defines a function called print_load_diagnostics
def print_load_diagnostics(steam_dictionary):
   
    #prints a diagnostics header
    print("\n--- Load diagnostics ---")
   
    #prints the number of games loaded while using len to count the items in the list 
    print("Number of games loaded:", len(steam_dictionary))
   
    #prints a sample of game names loaded within the list
    print("Sample game names:", list(steam_dictionary.keys())[:10])
   
    #prints a diagnostics footer wile trimming unseen characters 
    print("------------------------\n")

#defines a function called getSteamData
def getSteamData():
   
    #initializes the container dictionary for game records
    steam_dictionary = {}

   
    #creates an empty list and assigns it to variable candidates
    candidates = []
   
    #if statement checking for a user-specified path
    if USER_SPECIFIED_PATH:
   
        #appends the user-specified path to candidates
        candidates.append(USER_SPECIFIED_PATH)

    #extends the candidates list with default filenames
    candidates.extend(DEFAULT_CANDIDATES)

    #for loop iterating over candidate paths
    for candidate in candidates:
   
        #try block for existence check print
        try:
   
            #prints which candidate is being tried and whether it exists
            print(f"Trying: {candidate}  Exists: {os.path.exists(candidate)}")
   
        #except block when os.path.exists raises
        except Exception:
   
            #prints the candidate being tried if existence check fails
            print(f"Trying: {candidate}")

   
        #try block for opening and parsing the CSV file
        try:
            #open the file for reading, using UTF-8 encoding and fixing any bad characters
            with open(candidate, mode='r', encoding='utf-8-sig', errors='replace') as fh:
   
                #creates a CSV reader for the opened file
                reader = csv.reader(fh)
   
                #try block for reading the header row
                try:
   
                    #reads the header row from the CSV
                    header_row = next(reader)
   
                #except block for empty file
                except StopIteration:
   
                    #prints a message if the file appears empty
                    print(f"File '{candidate}' appears to be empty.")
   
                    #returns an empty dictionary when file is empty
                    return {}
   
                #normalizes header names by stripping whitespace
                header_fields = [h.strip() for h in header_row]

   
                #for loop processing each subsequent row in the CSV
                for row in reader:
   
                    #if statement skipping empty rows
                    if not row:
   
                        #continues to the next CSV row
                        continue
   
                    #if statement padding short rows
                    if len(row) < len(header_fields):
   
                        #extends the row with empty strings to match header length
                        row = row + [''] * (len(header_fields) - len(row))
   
                    #maps header fields to row values for this entry
                    entry = {header_fields[i]: row[i].strip() for i in range(len(header_fields))}
                    
                    #attempts to find the game name using common header variants (note there are two extra attempts due to error handling may remove)
                    game_name = (
                        entry.get('gameName') or
                        entry.get('Game Name') or
                        entry.get('name') or
                        ''
                    )
                    # if statement using index 6 as a fallback for game name
                    if not game_name and len(header_fields) > 6:
   
                        # uses the 7th column as a fallback for game name
                        game_name = row[6].strip()
                    
                    # if statement skipping rows without a game name
                    if not game_name:
                    
                        # continues to the next CSV row
                        continue
   
                    # if statement ensuring a list exists for this game
                    if game_name not in steam_dictionary:
   
                        # creates a new list for this game
                        steam_dictionary[game_name] = []
   
                    # appends the parsed entry to the game's list
                    steam_dictionary[game_name].append(entry)
   
            # prints a success message when loading succeeded
            print(f"Loaded data from '{candidate}'.")
   
            # returns the populated steam_dictionary to the caller
            return steam_dictionary
   
        # except block when the candidate file was not found
        except FileNotFoundError:
   
            # prints a message when the candidate file was not found
            print(f"Could not open '{candidate}'. Trying next candidate if available...")
   
            # continues to the next candidate in the loop
            continue
   
        # except block for other read/parsing errors
        except Exception as e:
   
            # prints a message describing any other error encountered
            print(f"Error reading '{candidate}': {e}")
   
            # continues to the next candidate in the loop
            continue

    # prints a message when no candidate files could be opened
    print("Could not find or open any of the candidate files. Please check the path and try again.")
   
    # returns an empty dictionary when loading fails
    return {}
#defines a function called getMenuChoice
def getMenuChoice():

    #while loop that repeats until a valid input is received
    while True:

        #prints the menu header separator
        print("============================================================")

        #prints the program title line
        print("             STEAM GAMES DATA ANALYSIS SYSTEM")

        #prints the menu header separator again
        print("============================================================")

        #prints the available operations header
        print("Available Operations:")

        #prints option 1 description
        print("1. Reload Steam data from file")

        #prints option 2 description
        print("2. Find a specific game")

        #prints option 3 description
        print("3. List games from a specific month")

        #prints option 4 description
        print("4. Show the average player count for a specific game")

        #prints option 5 description
        print("5. Find the most popular game by average number of players")

        #prints option 6 description
        print("6. List all game names")

        #prints option 7 description
        print("7. Generate game report")

        #prints option 8 description
        print("8. Write report to file")

        #prints option 9 description
        print("9. Set or change CSV file path")

        #prints option Q description
        print("Q. Quit the program")

        #prints a separator line before the prompt
        print("------------------------------------------------------------")

        #prompts the user for their menu choice
        choice = input("Enter your choice (1-9, Q to quit): ").strip()

        #if statement handling quit selection
        if choice.upper() == 'Q':

            #returns the quit signal to the caller
            return 'Q'

        #try block for parsing the input as an integer
        try:

            #turn the user's input into an integer
            menu_choice_number = int(choice)

            #check if the number is between 1 and 9
            if 1 <= menu_choice_number <= 9:

                #return the valid menu choice
                return menu_choice_number

            #prints a message when the number is out of range
            else:
                print("Please enter a number between 1 and 9, or Q to quit.")

        #except block when the input is not a valid integer
        except ValueError:

            #prints a message when the input is not a valid integer
            print("Invalid input. Please enter a number between 1 and 9, or Q to quit.")

#defines a function called findASpecificGame
def findASpecificGame(steam_dictionary):
   
    #prints the search header
    print("\nGame Search - Find a Specific Game")
   
    #prompts the user for the game name to search and strips whitespace
    name = input("Enter the game name to search for: ").strip()
   
    #if statement handling empty game name input
    if not name:
   
        #prints a message indicating no input was provided
        print("No game name entered. Returning to menu.")
   
        #returns an empty list to the caller
        return []
   
    #prepares a casefolded search term for case-insensitive matching
    term = name.casefold()
   
    #initializes a list to collect matching entries
    results = []
   
    #for loop iterating through game entry lists
    for entries in steam_dictionary.values():
   
        #for loop iterating through individual entry dictionaries
        for entry in entries:
   
            #retrieves the stored game name safely from the entry
            stored = entry.get('gameName', '')
   
            #if statement adding matches to the results list
            if stored and term in stored.casefold():
   
                #appends the matching entry to the results list
                results.append(entry)
   
    #if statement handling no matches found
    if not results:
   
        #prints the requested apology message
        print("I'm sorry that game isn't available")
   
        #returns an empty list to the caller
        return []
   
    #prints how many matches were found for the user's query
    print(f"\nFound {len(results)} entries for '{name}':")
   
    #returns the list of found entries to the caller
    return results

#defines a function called getGamesFromASpecificMonth
def getGamesFromASpecificMonth(steam_dictionary):
   
    # prints the month filter header
    print("\nGame Data By Month")
   
    # prompts the user for a three-letter month prefix and strips whitespace
    raw = input("Enter the month (first three letters, e.g., Oct): ").strip()
   
    # if statement handling empty month prefix input
    if not raw:
   
        # prints a message indicating no month prefix was entered
        print("No month prefix entered. Returning to menu.")
   
        # returns None to the caller
        return
   
    # normalizes the month prefix to title case for validation
    month = raw.title()
    
    # defines the set of valid three-letter month abbreviations
    valid_months = {'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'}
    
    # if statement handling invalid month prefix
    if month not in valid_months:
    
        # prints a message indicating the month prefix is invalid
        print(f"Invalid month prefix '{raw}'. Please enter a valid three-letter month like 'Jan' or 'Oct'.")
    
        # returns None to the caller
        return
    
    # initializes a list to collect entries matching the requested month
    found = []
    
    # for loop iterating through game entry lists
    for entries in steam_dictionary.values():
    
        # for loop iterating through individual entry dictionaries
        for entry in entries:
    
            # retrieves the month value from the entry safely
            m = entry.get('month', '')
    
            # if statement adding entries that match the requested month
            if m.startswith(month):
    
                # appends the matching entry to the found list
                found.append(entry)
    
    # prints a header for the results table
    print("============================================================")
    
    # prints column headers for the results table
    print(f"{'Game Name':40s} {'Average Players':>15s}")
    
    # prints a separator line under the headers
    print("============================================================")
    
    # if statement handling presence of matching entries
    if found:
   
        # prints how many entries were found for the month
        print(f"Found {len(found)} entries in '{month}':")
   
        # for loop printing each matching entry
        for e in found:
   
            # retrieves the game name for printing
            g = e.get('gameName', 'Unknown')
   
            # retrieves the average players value for printing
            a = e.get('avg_players', '0')
   
            # prints the formatted game name and average players
            print(f"{g:40s} {a:>15s}")
    
    # else branch when no entries matched the requested month
    else:
   
        # prints a message when no entries match
        print(f"No entries found for month prefix '{month}'.")
   
    # pauses so the user can read the results before returning to the menu
    pause()

#defines a function called getAveragePlayerCount
def getAveragePlayerCount(steam_dictionary):
    # reuses the findASpecificGame helper to get matching entries
    results = findASpecificGame(steam_dictionary)
    
    #if statement handling no matches found
    if not results:

        #return command    
        return
    
    #initializes a list to collect numeric avg_players values
    average_player_values = []
    
    #for loop iterating through each found entry
    for entry in results:
     
        #retrieves the avg_players string and strips whitespace
        avg_players_value = entry.get('avg_players', '').strip()
        
        #if statement skipping empty avg_players values
        if not avg_players_value:
           
            #continue to next block
            continue
        
        #try block for converting avg_players to float
        try:
            average_player_values.append(float(avg_players_value))
        
        #Except statement for error handling 
        except ValueError:
            #continues to next block 
            continue
    
    #if statement handling absence of numeric values
    if not average_player_values:
        
        #Prints user friendly message
        print("No numeric average player values found for this game.")
   
        #pauses screen for user to read
        pause()
       
        #returns data
        return
    
    #computes the average of the collected numeric values and assigns it to average 
    average = sum(average_player_values) / len(average_player_values)
    
    #retrieves the display name for the game from the first result
    game_name_value = results[0].get('gameName', 'Unknown')
    
    #prints the computed average players for the selected game
    print(f"\nAverage players for '{game_name_value}': {average:.2f} over {len(average_player_values)} months.")
   
    #pauses screen for user to read
    pause()

#defines a function called findMostPopularGame
def findMostPopularGame(steam_dictionary):

    # show a header message
    print("\nMost Popular Game by Average Number of Players")

    # set a starting value for the highest average
    highest_average = None

    # set a starting value for the best entry
    best_entry = None

    # go through all the lists of entries
    for entries in steam_dictionary.values():

        # go through each entry in the list
        for entry in entries:

            # get the average players value as text
            avg_players_value = entry.get('avg_players', '').strip()

            # if the value is empty
            if not avg_players_value:
              
                # skip to the next entry
                continue

            # try to turn the value into a number
            try:
                value = float(avg_players_value)
            
            # if the value is not a number
            except ValueError:
            
                # skip to the next entry
                continue

            # if this is the first value or bigger than the current highest
            if highest_average is None or value > highest_average:
            
                # update the highest value
                highest_average = value
            
                # remember this entry as the best one
                best_entry = entry

    #if a best entry was found
    if best_entry:
        
        #show the most popular game name
        print("\nMost Popular Game, by average number of players, in the Records:")
        
        #prints user friendly message and variables
        print(best_entry.get('gameName', 'Unknown'))
    
    #if no valid entry was found
    else:
    
        #tell the user no data was found
        print("No valid numeric average player data found in the records.")

    #wait for the user before going back to menu
    pause()

#defines a function called listAllGameNames
def listAllGameNames(steam_dictionary):

    # prints the header for listing all game names
    print("\nList of All Game Names in the Records")

    # prints a separator under the header
    print("=====================================")

    # if statement handling empty dataset
    if not steam_dictionary:

        # prints a message indicating no data is loaded
        print("No data is loaded. Use option 9 to set the CSV path, then option 1 to reload.")

        # pauses before returning to the menu
        pause()

        # returns None to the caller
        return
    
    #builds a sorted list of unique game names from the dictionary keys
    unique_names = sorted(set(steam_dictionary.keys()))
    
    # prints the total count of unique games
    print(f"Total unique games: {len(unique_names)}")
    
    # prints a subheader for the sample list
    print("\nFirst 25 game names:")
    
    # for loop printing the first 25 game names
    for name in unique_names[:25]:
    
        # prints a single game name
        print(name)
    
    # if statement handling case where more than 25 games exist
    if len(unique_names) > 25:
    
        # prints how many additional games are not shown in the sample
        print(f"... and {len(unique_names) - 25} more. Use report options to see details.")
    
    # pauses so the user can read the list before returning to the menu
    pause()

#defines a function called generateGameReport
def generateGameReport(steam_dictionary):
   
    # if statement handling empty dataset
    if not steam_dictionary:
   
        # prints a message indicating no data is loaded
        print("No data is loaded. Use option 9 to set the CSV path, then option 1 to reload.")
   
        # pauses before returning to the menu
        pause()
   
        # returns None to the caller
        return
   
    # prints the report options header
    print("\nReport Options")
   
    # prints option 1 for all-games summary
    print("1. Summary for ALL games")
   
    # prints option 2 for one-game summary
    print("2. Summary for ONE game")
   
    # prompts the user to choose a report type
    choice = input("Enter 1 or 2: ").strip()
   
    # if statement routing to the all-games report
    if choice == '1':
   
        # calls the helper function to generate the all-games report
        _report_all_games(steam_dictionary)
   
    # elif statement routing to the one-game report
    elif choice == '2':
   
        # calls the helper function to generate a one-game report
        _report_one_game(steam_dictionary)
   
    # else branch handling invalid report type selection
    else:
   
        # prints a message when the user enters an invalid choice
        print("Invalid choice. Returning to menu.")
   
    # pauses so the user can read the report before returning to the menu
    pause()

#defines a function called _report_all_games
def _report_all_games(steam_dictionary):

    # show a header message
    print("\nGame Report - Average Peak Players Over Recorded Months (ALL games)")

    # show a separator line
    print("========================================================")

    # show column headers
    print(f"{'Game Name':45s} {'Average Peak Players':>20s}")

    # show another separator line
    print("--------------------------------------------------------")

    # go through each game and its list of entries
    for game_name_value, entries in steam_dictionary.items():

        # set starting totals
        total_peak = 0.0
        peak_count = 0

        # go through each entry for this game
        for entry in entries:

            # get the peak players value as text
            peak_players_value = entry.get('peak_players', '').replace(',', '').strip()

            # if the value is empty
            if not peak_players_value:
                # skip to the next entry
                continue

            # try to turn the value into a number
            try:
                total_peak += float(peak_players_value)
                peak_count += 1
            # if the value is not a number
            except ValueError:
                # skip to the next entry
                continue

        # if at least one number was found
        if peak_count > 0:
          
            # work out the average peak players
            average_peak = total_peak / peak_count
          
            # show the game name and average peak players
            print(f"{game_name_value:45s} {average_peak:20.2f}")

#defines a function called _report_one_game
def _report_one_game(steam_dictionary):
    
    # prompts the user for the game name to report on
    search = input("Enter the game name to report on: ").strip()
    
    # if statement handling empty game name input
    if not search:
     
        # prints a message indicating no game name was entered
        print("No game name entered. Returning to menu.")
     
        # returns None to the caller
        return
    
    # prepares a casefolded search term for case-insensitive matching
    term = search.casefold()
    
    # initializes a list to collect matching rows for the selected game
    rows = []
    
    # for loop iterating through game entry lists
    for entries in steam_dictionary.values():
     
        # for loop iterating through individual entry dictionaries
        for entry in entries:
     
            # retrieves the stored game name for comparison
            game_name_value = entry.get('gameName', '')
            
            # if statement adding matching entries to rows
            if game_name_value and term in game_name_value.casefold():
     
                # appends the matching entry to the rows list
                rows.append(entry)
    
    # if statement handling no matches found
    if not rows:
     
        # prints the apology message when the game is not available
        print("I'm sorry that game isn't available")
     
        # returns None to the caller
        return
    
    #initializes accumulator for peak totals
    total_peak = 0.0
    
    #initializes counter for peak entries
    peak_count = 0
    
    #initializes accumulator for average player totals
    total_avg = 0.0
    
    #initializes counter for average player entries
    avg_count = 0
    
    #for loop iterating through each matching entry
    for entry in rows:
        #retrieves and normalizes the peak_players value
        peak_players_value = entry.get('peak_players', '').replace(',', '').strip()
        
        #retrieves the avg_players value
        average_players_value = entry.get('avg_players', '').strip()
        
        # try block for adding numeric peak values
        try:
            # if statement ensuring peak value is present
            if peak_players_value:
                # accumulates the peak value
                total_peak += float(peak_players_value)
                # increments the peak count
                peak_count += 1
        # except block ignoring non-numeric peak values
        except ValueError:
            pass
        
        # try block for adding numeric average values
        try:
            # if statement ensuring average value is present
            if average_players_value:
                # accumulates the average value
                total_avg += float(average_players_value)
                # increments the average count
                avg_count += 1
        # except block ignoring non-numeric average values
        except ValueError:
            pass
    
    # prints the report header for the selected game
    print("\nGame Report - Selected Game")
    
    # prints a separator line
    print("--------------------------------------------------------")
    
    # prints the game name being reported on
    print(f"Game: {rows[0].get('gameName','Unknown')}")
    
    # if statement printing average peak players only when data exists
    if peak_count > 0:
        # prints the computed average peak players and the count of months
        print(f"Average peak players: {total_peak/peak_count:.2f} over {peak_count} months")
    # else branch when no peak data is available
    else:
        # prints N/A when no peak data is available
        print("Average peak players: N/A")
    
    # if statement printing average players only when data exists
    if avg_count > 0:
        # prints the computed average players and the count of months
        print(f"Average players: {total_avg/avg_count:.2f} over {avg_count} months")
    # else branch when no avg player data is available
    else:
        # prints N/A when no avg player data is available
        print("Average players: N/A")

#defines a function called writeReportToFile
def writeReportToFile(steam_dictionary):

    #if no data is loaded
    if not steam_dictionary:
        # tell the user no data is loaded
        print("No data is loaded. Use option 9 to set the CSV path, then option 1 to reload.")
        # wait for the user before going back to menu
        pause()
        # stop the function
        return

    #ask the user for a filename
    filename = input("Enter the filename to write the report to (e.g., game_report.txt): ").strip()

    #if nothing was entered
    if not filename:
      
        # tell the user no filename was entered
        print("No filename entered. Returning to menu.")
      
        # stop the function
        return

    # try to open the file and write the report
    try:
      
        # open the file for writing
        with open(filename, mode='w', encoding='utf-8') as output_file:

            # write the report header
            output_file.write("Game Report - Average Peak Players Over Recorded Months\n")

            # write a separator line
            output_file.write("========================================================\n")

            # write column headers
            output_file.write(f"{'Game Name':45s} {'Average Peak Players':>20s}\n")

            # write another separator line
            output_file.write("--------------------------------------------------------\n")

            # go through each game and its list of entries
            for game_name_value, entries in steam_dictionary.items():

                # set starting totals
                total_peak = 0.0
                peak_count = 0

                # go through each entry for this game
                for entry in entries:

                    # get the peak players value as text
                    peak_players_value = entry.get('peak_players', '').replace(',', '').strip()

                    # if the value is empty
                    if not peak_players_value:
      
                        # skip to the next entry
                        continue

      
                    # try to turn the value into a number
                    try:
                        total_peak += float(peak_players_value)
                        peak_count += 1
      
                    # if the value is not a number
                    except ValueError:
      
                        # skip to the next entry
                        continue

                # if at least one number was found
                if peak_count > 0:
      
                    # work out the average peak players
                    average_peak = total_peak / peak_count
      
                    # write the game name and average peak players to the file
                    output_file.write(f"{game_name_value:45s} {average_peak:20.2f}\n")

        # tell the user the report was written
        print(f"Report successfully written to '{filename}'.")

    # if something went wrong while writing
    except Exception as ex:
      
        # tell the user there was an error
        print(f"Error writing report to '{filename}': {ex}")

    # wait for the user before going back to menu
    pause()



#Calls main()
if __name__ == "__main__":
    main()
