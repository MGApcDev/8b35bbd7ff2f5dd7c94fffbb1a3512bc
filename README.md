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

# Basic usage
```bash
python src/lamaandgroves.py "poultry outwits ants" some-dictionary.txt > anagrams.txt

python src/lamahash.py anagrams.txt solutions-to-find.txt
# Output:
............
.....
```

# Theory

The program constructs and abstract syntax tree of the given dictonary of words.

```Input phrase: "an dlamasa pple"```
   
| Word list        | Syntax Tree           |
| ------------- |:-------------:|
| <ul><li>and</li><li>app</li><li>apple</li><li>groves</li><li>lamas</li></ul> | <img src="https://i.imgur.com/nF1jzS0.png" width="200"> |



And a solution tree that accounts for all anagrams while accounting for the letters available...
<img src="https://i.imgur.com/gSJdExL.png" width="400" style="float:right">


<img src="https://i.imgur.com/bCyFtQG.gif" height="100">
