# cvbankas.lt web site scraper

Tool for scraping cvbankas.lt web site.

## Running 

### Installation
Two ways to install:

1. Clone repo and execute
```
pip install .
```

2. Pip install
```
pip install cvbankas_scraper
```

### Command line

arguments:
```
  -h, --help    show this help message and exit
  -v VERBOSE    Set verbose True/False
  -t TIMEOUT    Timeout between single page requests, default 1 second
  -o FILE_PATH  JSON file path to store results
  -u URL        URL to start scraping
```

execute command
```
>> cvbankas_scraper -v true -u "https://www.cvbankas.lt/?miestas=Kaunas&page=21" -o /tmp/output.json -t 1
```

### Usage example
```python
import cvbankas_scraper

# single advertisement
cvbankas_scraper.scrape_single_advertisement(url="https://www.cvbankas.lt/etransport-vairuotojas-a-keleiviu-pavezejas-a-kaune-kaune/1-4351087")

# multiple advertisements
cvbankas_scraper.scrape_multiple_advertisements(url="https://www.cvbankas.lt/?miestas=Kaunas&page=21",
                                                timeout=2,
                                                verbose=True)

# all pages from url as start page
cvbankas_scraper.scrape_multiple_advertisements(url="https://www.cvbankas.lt/?miestas=Kaunas&page=19",
                                                timeout=2,
                                                verbose=True)
```