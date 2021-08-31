Educational universities often list out the key takeaways from respective courses under keywords like Learning Objective, Learning Outcome. This Algorithm searches for texts following keywords like Learning Objective and Learning Outcome.

Solution: This information is generally available in Tables or plain text. Tika Libraries were used to fetch the texts from PDF with correct format and indentation And the Camelot package has been used to fetch information from the tables.

In a textual format fetching data is easy and simple where the character limit is hardcoded to 500, where the algorithm fetches 500 characters after the desired keyword.

In tables, the data can be arranged in numerous ways.

- There can be two columns and the data can be present horizontally
- There can be two columns and desired keywords be present in the column heading and texts can run down.
- There can be more than two columns where the keywords are a part of the headings and texts run down.
