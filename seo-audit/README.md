# SEO audit and repair kit

Someone wants to book a bookbinding class at Folio Bench, a fictional workshop. The “Reserve a bench” link leads to a missing page. Give the web editor enough information to reproduce the failure and decide when to close the ticket.

1. Read [the bookbinding page](site/workshops/bookbinding/index.html) as source. Find the link destination and compare it with rows E03 and E06 in [the page inventory](evidence.csv).
2. Fill a copy of the [blank ticket](blank-ticket.csv). Record the affected path, what you observed, who can confirm the intended destination, and the test you will run after the repair.
3. Compare your ticket with row 01 of [the completed repair list](repairs.csv). A successful page load proves the visitor can reach booking. Completing a reservation requires a separate test.
4. Try the other two tickets. One workshop is accidentally excluded from search. Two workshops share a title. The archive and privacy pages have intentional exclusions.

With Python 3, run this command from the repository root. It checks the seven supplied pages, repairs a temporary copy, then verifies the three findings are resolved and both intentional exclusions survive.

```sh
python3 seo-audit/check.py --retest
```

For an actual site, verify redirects and the final response in a browser. Inspect HTTP headers as well as the rendered page before closing an indexing ticket. This exercise records what the sample files contain. Search indexing and rankings require separate evidence.
