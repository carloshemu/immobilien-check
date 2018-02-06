from craw_for_buy import *
from utilities import *

url = "https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Bayern/Muenchen-Kreis"

# Rent
# main_url = "https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Bayern/Muenchen-Kreis"
# fname = "munich_new.csv"


# Buy
main_url = "https://www.immobilienscout24.de/Suche/S-T/Wohnung-Kauf/Umkreissuche/M_fcnchen_20_28Kreis_29/-/118984/2024595/-/1276002060/20"
fname = "munich_buy.csv"


add_new_data(main_url, fname)


# save_webpage_to_file(main_url, "buy.html")