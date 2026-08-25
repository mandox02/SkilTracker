README

Thank you for downloading SkilTracker!

This Python application runs thanks to the following libraries:
Openpyxl
CustomTKInter

Before you start, however, keep in mind that this tool is meant to be used in a business environment, and is specifically meant for tracking employee or consultant skills in order to determine their fit for a position, but should not be taken as an end-all, be-all to the process.

The skills for each employee or consultant (that from this point will be referred to as candidate) are meant to be taken from their CV or any other documentation that proves they have a certain skillset. Please be responsible about this, as I do not want to get sued by employees for the use of this tool.

This tool depends on the following understanding:
Skills have three categories:
    Category 1: The skills that the candidate is most proficient in (Limit 2 per candidate)
    Category 2: Other skills the candidate has direct business exposure to (Limit 5 per candidate)
    Category 3: Skills that the candidate has only taken courses in, and has no business exposure to (Limit 5 per candidate)

Each candidate has a unique, non-modifiable ID (likely assigned already by the business, but if not, can be assigned internally in the tool). When opening for the first time, you (from now on referred to as the end user) must declare how many characters this ID contains, as the format has to be consistent across all IDs.
Each candidate also requires a name, band and sector (sometimes called department). All of this information is mandatory.

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
v0.1: Start of the project with mostly complete main script.
v0.5 (LATEST):
    - Main window now has full functionality!
    - Search by ID or name is fully functional
    - Create, Edit and Delete all work as intended
    - Warning and confirmation pop ups all work as intended.
    - Fixed a bug where the search results frame shrank every consecutive button.
    - Fixed a bug that caused errors to not show up.