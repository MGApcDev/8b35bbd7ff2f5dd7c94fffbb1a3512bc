<h1 align="center">LamasAndGroves</h1>
<p align="center">
    <img alt="Rax" src="https://media1.tenor.com/images/d70ca20256e8f2be561167278e00819c/tenor.gif" width="300">
</p>
<p align="center">
Small project to solve anamgras.
</p>
<p align="center">
<a href="https://travis-ci.org/MGApcDev/LamasAndGroves"><img alt="TypesetBot" src="https://travis-ci.org/MGApcDev/LamasAndGroves.svg?branch=master"></a>
<a class="badge-align" href="https://www.codacy.com/app/mgapcdev/8b35bbd7ff2f5dd7c94fffbb1a3512bc?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=MGApcDev/8b35bbd7ff2f5dd7c94fffbb1a3512bc&amp;utm_campaign=Badge_Grade"><img src="https://api.codacy.com/project/badge/Grade/fe959f1e438a4b6cb167c224562c52fb"/></a>
</p>

LamasAndGroves is a program for finding the anagrams behind a hash. 
So given a phrase, a list of words, a hashing algorithm and list of hashes.
The program will find the hashes in the list and output them with their hash counterpart:
```
# Output
8229b3735981c23fb122c6db1a2a09b9 --> Anagram found
...
```

# Basic usage
```bash
$ python src/lamasandgroves.py "some search phrase" some-dictionary.txt "md5" hashes-to-find.txt
args {
    0 =>           lamasandgroves.py,
    1 => str:      phrase to find anagrams for,
    2 => filename: file of words that could be in the anagram,
    3 => str:      hash algorithm (md5, sha1, sha256, sha512, plain),
    4 => filename: file of hashes we should look for
}
```

# Theory

When running the program a wordlist is provided, which will be the basis of the anagrams we need to find. 
To hold the words in memory so that it's quickly to parse and lookup. We'll be using a abstract syntax tree, where each branch in the tree represents a character.

We combine parsing words to an internal structure with reducing the list of words, to avoid keeping too much in memory. 

The program constructs an abstract syntax tree of the given dictonary of words.

   
| Word list        | Syntax Tree           |
| ------------- |:-------------:|
| <ul><li>and</li><li>app</li><li>apple</li><li>groves</li><li>lamas</li></ul> | <img src="https://i.imgur.com/nF1jzS0.png" width="200"> |


To find the anagrams of the words available, we create a tree of all the valid combinations, where each branch represents a word.

For the given phrase ```"an dlamasa pple"```, part of the tree we would produce is this:


<img src="https://i.imgur.com/gSJdExL.png" width="400">


To improve performance we implement a few heuristics that logically target the problem:

_1. Avoid computing branches that has the same subproblem_
- When going down branches we might end up with subproblems that are the same, so we know those branches will create the same sub-branches.
<img src="https://i.imgur.com/DlpWHPm.png" width="400">

- We avoid this by creating a representation for the remaining characters and make a table for 
```{dict_str => WordBranch}```.
- All branches with the same subproblem will therefore reference a single WordBranch.
- Looking at a example of 1.100 words, 35% of them are permutations of other words in the list, meaning we can skip those computations on every level.

_2. Solve hashes as we go_
- Using a dictionary of 99.000 words a small piece of text like "anagram" ends up having 34.668 valid anagrams.
- With this many solutions, either we have a lot of IO time or we use a lot of resources to keep all solutions in memory. Therefore we compute the hash of each candidate and check if it's one of the hashes we're looking for before we return the solutions.

_3. Terminate when hashes are found_
- When all solutions are found we might still have anagrams we haven't check. This gives no extra value and we terminate to recursive loop.

_4. Solve anagrams in levels_
- Once the AST of word combinations are constructed, we look for the solutions one level at a time, due to the increased likelyhood of the phrase we're looking for contains words longer than 1 letter. We would use a BFS algortihm to find solutions, but the implementation has some problems when it comes to space effecientcy, because we need to store a queue with elements equal to the width of the tree.
- We handle this by finding solutions using DFS for level 1, then solutions for level 1 + 2, then solutions for 1 + 2 +...+ k. This approach is not optimal, but due to the performance gains from removing dubplicate subproblems, we still save time overall.

# Test

Running time on instance: ```pharse length 18, valid words after parsing 1.659```

| Description | simple | w. heuristics |
| --- | --- | --- |
| 3-word combinations | 463s | 246s |
| 4-word combinations | 25.153s | 8.580s |
| 5-word combinations | unknown | unknown |


<img src="https://i.imgur.com/bCyFtQG.gif" height="75">
