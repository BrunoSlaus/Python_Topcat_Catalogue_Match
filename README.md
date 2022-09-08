# Python_Topcat_Catalogue_Match
A python code for matching catalogues via Topcat. 

This repository contains the codes needed to match two catalogues
via the Topcat -stilts and produce the graphs detailing the match.
The graphs will show both the integrated and non-integrated
increase in the number of corresponding matches.

In order for the codes to work you need to put them together in 
one folder. In that same folder you should create the "Input" 
folder containing the input data (i.e. fields to be matched).
You should also create the "Output" and "log" folders as well.
The names of these folders should be exactly as stated.

The match is a "skymatch" between the RA and DEC of 2 fields.
The RA column is called "RA" while the DEC column is called 
"DEC". Adjust the column names of your fields accordingly or
alter the codes.

The repository contains:
1) Matcher.py      : This is the main code used for calling 
                     "Topcat_Match.py" and plotting the graphs. 

2) Topcat_Match.py : This is the -stilts program calling Topcat
                     to perform the match.  
