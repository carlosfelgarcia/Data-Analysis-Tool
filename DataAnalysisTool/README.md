# Data-Analysis-Tool
A small project that I am working on for data analysis.

It is a small tool that allows you to get CSV files and get some analysis.

## How it works

- Load a CSV file from the file top menu
- Once the file is loaded:
** Add or delete columns
** Add more functions to get more options into the tool by modifying "plot_generator" class and "get_information" method in the "data_analysis" class.

### Automatization

- All the changes that you do into the class are going to be reflected in the UI once you restart the tool, therefore the names of the new plot generators matter.
- For the new information that is added to the method, you also have to add that operation into a constant list in the UI named "INFO".

### New Column base on the function
To add a new column base on other columns, you may need to write the function that relates the new column with the other columns in the data frame.

## Contributions
If you like this project and want to contribute or use this tool feel free to do it.
Also, any feedback is welcome.
