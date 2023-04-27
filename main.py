import os
import articles_functions
import books_functions

def create_bdd():
    books_functions.create_tab_list_names()
    books_functions.create_tab_books()
    articles_functions.create_tab_article() #stop after 1 or 2 "response ok"
    #si l'algo se stop, une boucle de create_tab_books s'est arreté, verifier alors si une table est apparu dans les bdd
    #si oui alors exceuter juste create_tab_article()

if __name__=="__main__":
    if len(os.listdir('data_brutes/data_books')) == 0:
        create_bdd()