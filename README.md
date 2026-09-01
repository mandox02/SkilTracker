Thank you for downloading SkilTracker!

This Python application runs thanks to the following libraries:
Openpyxl
CustomTKInter

Before you start, however, keep in mind that this tool is meant to be used in a business environment, and is specifically meant for tracking employee or consultant skills in order to determine their fit for a position, but should not be taken as an end-all, be-all to the process.

The skills for each employee or consultant (that from this point will be referred to as candidate) are meant to be taken from their CV or any other documentation that proves they have a certain skillset. Please be responsible about this, as I do not want to get sued by anyone for the use of this tool.

This tool depends on the following understanding, please read this carefully.
Skills have three categories:
    Category 1: The skills that the candidate is most proficient in (Limit 2 per candidate)
    Category 2: Other skills the candidate has direct business exposure to (Limit 5 per candidate)
    Category 3: Skills that the candidate has only taken courses in, and has no business exposure to (Limit 5 per candidate)

Each candidate has a unique, non-modifiable ID (likely assigned already by the business, but if not, can be assigned internally in the tool). When opening for the first time, you (from now on referred to as the end user) must declare how many characters this ID contains, as the format has to be consistent across all IDs.* 
Each candidate also requires a name, band and sector (sometimes called department). All of this information is mandatory.

/* I haven't gotten around to adding this functionality in yet. For now, all IDs must be 6 characters long, and the tool will not allow you to adjust this. The same is true for the band range, this is set at 1-10. I promise I will add a config file at some point to fix this.

All of these values can be edited in the excel file directly, but I strongly advise against it, unless the format has been verified to match.

To register a candidate:
    - Click the New button in the main window
    - Fill in all the required fields.
    - Verify all fields have the proper format.
    - Click Save

To use the search feature:
    - Click the Search Bar in the main window
    - Input the ID or Name, if searching for a specific candidate, or a skill to find all candidates with that skill.
    - To use the advanced search feature, click the advanced search button next to the Search Bar in the main window.
    - The advanced search needs at least one search term to display a list of all candidates that match the criteria.

Changelog:
v0.1-0.4: Start of the project, process of main script writing and the beginning of the development of the UI. 
v0.5:
    - Main window now has full functionality!
    - Search by ID or name is fully functional
    - Create, Edit and Delete all work as intended
    - Warning and confirmation pop ups all work as intended.
    - Fixed a bug where the search results frame shrank every consecutive button.
    - Fixed a bug that caused errors to not show up.
v0.6:
    - Fixed a styling error in the confirmation popup when deleting a candidate. Appearance is now as intended.
    - Advanced search window now works.
    - added a cheat code to the ID search: type "all" to view all entries.
    - Fixed a bug where the band dropdown remains editable when cancelling an edit operation.
    - Identified a bug where the skills get saved even if at least one category is empty.
v0.7 (LATEST):
    - The advanced search window now displays all existing bands and sectors in the excel.
    - Began bug testing, and here are the bugs I found in my testing:
    - Fixed a bug where the skills get saved even if at least one category is empty.
    - Fixed the skills searching, no longer are they only exact (and case sensitive) matches.
    - Fixed a bug where the advanced search popup doesn't get destroyed after an error has been produced, and won't make new error popups either.
    - Fixed a bug where clicking a result won't destroy the advanced search window if another search overwrote the previous result list.
    - Fixed a bug where "No results" error popup doesn't occur in the advanced search.
    - An executable was created. Can be found under dist/SkilTracker/SkilTracker.exe
