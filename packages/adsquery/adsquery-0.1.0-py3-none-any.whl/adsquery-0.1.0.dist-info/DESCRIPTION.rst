# adsquery

This tool let you query the ADS using a simple CLI.

## Installation
You'll need an API key from NASA ADS labs. Sign up for the newest version of ADS search at https://ui.adsabs.harvard.edu, visit account settings and generate a new API token. The official documentation is available at https://github.com/adsabs/adsabs-dev-api.

You can then install the tool through pip:
```
$ pip install adsquery
```

After that, you should be able to use it under the name `adsquery`:
```
$ adsquery --help
$ adsquery query --help
```

## Querying
To make a query to the ADS, try:
```
$ adsquery query [my-query]
```
The query can either be an ADS compatible query or a bashist one. For example:
```
$ adsquery query --first-author Einstein 1915
$ adsquery query ^Einstein 1915
```
will result in the same results (papers by Einstein in 1915).


## Examples
Imagine we're looking at the original 1915 Einstein's paper that's explaining for the first time the advance of the perihelion of Mercury. Here's an example of how to use adsquery
```
$ adsquery query --first-author Einstein --year 1915
[0]: 1915, Annalen der Physik — Einstein, A., Antwort auf eine Abhandlung M. v. Laues Ein Satz der Wahrscheinlichkeitsrechnung und seine Anwendung auf die Strahlungstheorie
[1]: 1915, Sitzungsberichte der Königlich Preußischen Akademie der Wissenschaften (Berlin — Einstein, Albert, Die Feldgleichungen der Gravitation
[2]: 1915, Naturwissenschaften — Einstein, A., Experimenteller Nachweis der Ampèreschen Molekularströme
[3]: 1915, Sitzungsber. preuss.Akad. Wiss — Einstein, A., Erklarung der Perihelionbewegung der Merkur aus der allgemeinen Relativitatstheorie
[4]: 1915, Sitzungsberichte der Königlich Preußischen Akademie der Wissenschaften (Berlin — Einstein, Albert, Erklärung der Perihelbewegung des Merkur aus der allgemeinen Relativitätstheorie
[5]: 1915, Sitzungsberichte der Königlich Preußischen Akademie der Wissenschaften (Berlin — Einstein, Albert, Zur allgemeinen Relativitätstheorie
[6]: 1915, Koninklijke Nederlandse Akademie van Wetenschappen Proceedings Series B Physical Sciences — Einstein, A., de Haas, W. J., Experimental proof of the existence of Ampère's molecular currents
[7]: 1915, Sitzungsberichte der Königlich Preußischen Akademie der Wissenschaften (Berlin — Einstein, Albert, Zur allgemeinen Relativitätstheorie (Nachtrag)
[8]: 1915, Deutsche Physikalische Gesellschaft — Einstein, Albert, de Haas, Wander Johannes, Notiz zu unserer Arbeit "Experimenteller Nachweis der Ampèreschen Molekularströme"
[9]: 1915, Deutsche Physikalische Gesellschaft — Einstein, Albert, Berichtigung zu meiner gemeinsam mit Herrn J. W. de Haas veröffentlichten Arbeit "Experimenteller Nachweis der Ampèreschen Molekularströme"
```
Here we see we got a few papers from the period, let's keep only the ones matching the work `Merkur` (Mercury in German)
```
Comma separated articles to download [e.g. 1-3, 4], [m] for more [q] to quit or add more parameters to request [e.g. year:2016]: Merkur
[0]: 1915, Sitzungsberichte der Königlich Preußischen Akademie der Wissenschaften (Berlin — Einstein, Albert, Erklärung der Perihelbewegung des Merkur aus der allgemeinen Relativitätstheorie

# Now let's download it
Comma separated articles to download [e.g. 1-3, 4], [m] for more [q] to quit or add more parameters to request [e.g. year:2016]: 0
Download [d], bibtex[b], quit[q]? d
```
The file is now located at `~/ADS/1915SPAW.......831E_Einstein.pdf`. If you wanted the bibtex entry, you should replace the last `d` by `b`.

# Features
- [x] query the ADS
- [x] interactively prompt the user
  - [x] show bibtex reference
  - [x] download pdf file

## Bugs and suggestions
Feel free to fill in an issue if you have any problem or suggestion

## Thanks
Special thanks to andycasey for providing https://github.com/andycasey/ads and the ADS!


