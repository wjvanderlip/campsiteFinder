# Input file instructions:

If there is a certain target you are searching for, you can use an input file to pass to the program to skip the user input. The quick_load.txt
provides an example for this input file. Take care the all the formatting is correct or the input will break.

```
Start_date
End_date
campsite_input
e-mail
y/n for automation
time between searches
length to run search
```
### Running the search with input file

To run the search with input file from the script directory:
```
../scripts/finder.py << input_file.txt
```
