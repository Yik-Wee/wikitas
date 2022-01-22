# WikiTAS
### Wikipedia "TAS Bot" to find the path from wikipedia page A to page B using a Breadth-First Search on a Tree constucted using Wikipedia links from respective pages
### Essentially just a bot for Wikipedia speedruns, where you go from page A to B using only the links on the page
### Using just a normal Breadth-First Search on all the links finds the shortest path, but is slow and takes up lots of memory having to search through possibly millions of links

## Attempts at optimizations on speed
1. Multi-threading multiple http requests at once
    - Significant decrease in search time
2. Matching links by relatedness (using nltk)
    - Gets the related words of the destination title and matches how related each link/title is to the related words
    - Searches the first n words in order of relatedness (default n = 7)
    - Search time decreases (sometimes very slightly) only for longer paths and for destination titles in the wordnet database

## Running/testing
1. Git clone the repo
2. Activate a python virtualenv in the directory or the cloned repo
3. Run `pip install -r requirements.txt`
4. Run tests or the main file `wikitas.py`
### USAGE: `python3 wikitas.py [START_PAGE] [END_PAGE] [...OPTIONS]`
### OPTIONS:
    -h | --help             Display this help page
    -w | --matchwords       Find path from START_PAGE to END_PAGE by matching the relatedness of words
    -s | --simple           Find path from START_PAGE to END_PAGE using without matching words
    -Pw | --Pmatchwords     Same as --matchwords but using multi-threaded http requests to the wikipedia api
    -Ps | --Psimple         (Default) Same as --simple but using multi-threaded http requests to the wikipedia api
### Example: `python3 wikitas.py among_us black_hole -Pw -Ps -w -s`
### Output:
```
-----------------------------------
Starting find_path_wordmatching
Finding path from Among Us to Black hole
Matching links against ['Black', 'hole']
[ Current page: Black ]
Among Us -> Color blindness -> Black -> Black hole
Found in 30.859390088000055 s
-----------------------------------
-----------------------------------
Starting find_path_simple_parallel
Finding path from Among Us to Black hole
[ Current page: Albert Einstein ]
Among Us -> Alexandria Ocasio-Cortez -> Albert Einstein -> Black hole
Found in 52.24804970499986 s
-----------------------------------
-----------------------------------
Starting find_path_wordmatching_parallel
Finding path from Among Us to Black hole
Matching links against ['Black', 'hole']
[ Current page: Black ]
Among Us -> Color blindness -> Black -> Black hole
Found in 7.343498709999949 s
-----------------------------------
-----------------------------------
Starting find_path_simple
Finding path from Among Us to Black hole
[ Current page: Albert Einstein ]
Among Us -> Alexandria Ocasio-Cortez -> Albert Einstein -> Black hole
Found in 780.7410415399997 s
-----------------------------------
```
