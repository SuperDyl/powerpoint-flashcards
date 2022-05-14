# powerpoint-flashcards
Immediately create a get-to-know-you flashcards PowerPoint.
Currently, it will automatically pull employee data from https://religion.byu.edu
and make a slide for each picture along with the employee's name.
Slides for adjunct, on-leave, or Salt Lake Center faculty are not created.

Support will be later added for flashcards of employee's room numbers,
joke slides, and more command line options.

You can download a branch, but the easiest way is to download a release version.
Run the install-mac.command or install-windows.bat file to setup the program.
It will place a file named FlashcardsPowerpoint-mac or FlashcardsPowerpoint-win
into the main directory.

The FlashcardsPowerpoint script can be called with command-line arguments,
including -h to receive help on all options.
One of the most useful arguments would be --refreshall .
It forces pulling employee information and photos from online.

The existing professor data can be edited easily:
professors.csv