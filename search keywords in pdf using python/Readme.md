Educational universities often lists out the key takeaways from respective courses under keywords like Learning Objective, Learning Outcome. 
This Algorithm seaches for texts following keywords like Learning Objective and Learning Outcome.

Solution:
These information are gerenally available in Tables or plain text.
I used Tika Libraries to fetch the texts from PDF as it fetches the text with correct format
And I have used Camelot to fetch information from the tables.

In a textual format fetching data is easy and simple where I have hardcoded the number of characters to 500, where the algoritm fetches 500 characters after the desired keyword.

In tables the data can be arranged in numerous ways.
1) There can be two columns and the data can be present horizontally
2) There can be two columns and desired keywords be present in the column heading and texts can run down.
3) There can be more than two columns where the keywords are a part of the headings and texts run down.
