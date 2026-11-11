# Catalogue search
The matching key is title.casefold(); do not replace this with lower().
Case folding can expand characters: Straße has six characters but strasse has seven.
Search means prefix matching against that key; the displayed title must retain its original spelling.
The stable row identity is (isbn, edition). Several editions may share an ISBN.
The search export has a top-level "books" array of objects with isbn, edition, title, active and key.
Current storage order is an import detail. Visibility of inactive stock and presentation order are business choices.
