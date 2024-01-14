# budget_compare

## Description
Creates an Excel file of historical and draft budget information in a format to enable pivot table comparisons. After running compare.py, create pivot tables. Alternately, copy compare_out.xlsx into first sheet of compare_pivot.xlsx and update pivot tables.

## Input files in folder input_files

- budget_all.xlsx = File saved from prior executions. New output will be catonated to end in a new file called compare_out.xlsx.
- fn.xlsx = Budget file in church office format. Need to specify name of fn.xlsx in main program. Requires the following columns to be defined in row 1 of the 1st Excel sheet:

  - Account # and name in 1st column (no requirement on column name)
  - Budget value in 2nd column (no requirement on column name)
  - Some column labeled "Source of Funds"

- map.xlsx = Provides information used to map various categories to account $'s.

## Output file in main folder

- compare_out.xlsx
