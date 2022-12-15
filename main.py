#!/usr/bin/env python
# coding: utf-8


##########################
### Name: Yuqing Zhang ###
### Uniqname: zhyuqing ###
##########################



import pandas as pd


class movie:
    def __init__(self, ranking, imdbID, title, year, rating, runtime, genre, director, cast, imdbRating, poster, language, country):
        self.ranking = ranking
        self.imdbID = imdbID
        self.title = title
        self.year = year
        self.rating = rating
        self.runtime = runtime
        self.genre = genre
        self.director = director
        self.cast = cast
        self.imdbRating = imdbRating
        self.poster = poster
        self.language = language
        self.country = country
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size
    
    # Print as a list of movies
    def print_list(self):
        if self.root:
            self._print_list(self.root)
            
    def _print_list(self, currentNode):
        if currentNode:
            print(f'Rank #{currentNode.ranking}. {currentNode.title} ({currentNode.year}) --- {currentNode.imdbRating}')
            self._print_list(currentNode.left)
            self._print_list(currentNode.right) 
    
    
    # Print detail info of the movie
    def print_detail(self, ranking):
        if self.root:
            self._print_detail(self.root, ranking)
        return ""
            
    def _print_detail(self, currentNode, ranking):
        if currentNode:
            if currentNode.ranking == ranking:
                print("Ranking (#/300): " + str(currentNode.ranking))
                print("IMDb ID: " + str(currentNode.imdbID))
                print("Title: " + str(currentNode.title))
                print("Releasing year: " + str(currentNode.year))
                print("Rating: " + str(currentNode.rating))
                print("Runtime: " + str(currentNode.runtime))
                print("Genre: " + str(currentNode.genre))
                print("Director: " + str(currentNode.director))
                print("Cast: " + str(currentNode.cast))
                print("IMDb rating: " + str(currentNode.imdbRating))
                print("Language: " + str(currentNode.language))
                print("Country: " + str(currentNode.country))
            self._print_detail(currentNode.left, ranking)        
            self._print_detail(currentNode.right, ranking)
      
    
    # Insert data to BST
    def insert(self, ranking, imdbID, title, year, rating, runtime, genre, director, cast, imdbRating, poster, language, country):
        if self.root is None:
            self.root = movie(ranking, imdbID, title, year, rating, runtime, genre, director, cast, imdbRating, poster, language, country)
        else:
            self._insert(ranking, imdbID, title, year, rating, runtime, genre, director, cast, imdbRating, poster, language, country, self.root)
        self.size = self.size + 1
            
    def _insert(self, ranking, imdbID, title, year, rating, runtime, genre, director, cast, imdbRating, poster, language, country, currentNode):
        if ranking < currentNode.ranking:
            if currentNode.left is None:
                currentNode.left = movie(ranking, imdbID, title, year, rating, runtime, genre, director, cast, imdbRating, poster, language, country)
                currentNode.left.parent = currentNode
            else:
                self._insert(ranking, imdbID, title, year, rating, runtime, genre, director, cast, imdbRating, poster, language, country, currentNode.left)

        elif ranking > currentNode.ranking:
            if currentNode.right is None:
                currentNode.right = movie(ranking, imdbID, title, year, rating, runtime, genre, director, cast, imdbRating, poster, language, country)
                currentNode.right.parent = currentNode
            else:
                self._insert(ranking, imdbID, title, year, rating, runtime, genre, director, cast, imdbRating, poster, language, country, currentNode.right)
        else:
            print("Already exist")

    
    # Save tree to json        
    def convert_to_json(self, currentNode):
        if currentNode == None:
            return None
        else:
            return((f"Ranking: {currentNode.ranking}", f"IMDB ID: {currentNode.imdbID}", f"Title: {currentNode.title}",
                f"Year: {currentNode.year}", f"Rating: {currentNode.rating}", f"Runtime: {currentNode.runtime}",
                f"Genre: {currentNode.genre}", f"Director: {currentNode.director}", f"Cast: {currentNode.cast}",
               f"IMDb Rating: {currentNode.imdbRating}", f"Poster: {currentNode.poster}", f"Language: {currentNode.language}",
               f"Country: {currentNode.country}"),
               self.convert_to_json(currentNode.left), self.convert_to_json(currentNode.right))
    
    def save_tree_to_json(self, jsonfile):
        savetree = self.convert_to_json(self.root)
        content = json.dumps(savetree)
        f = open(jsonfile,"w")
        f.write(content)
        f.close()
    

    # Implement the ranking request
    def ranking(self, fromranking, toranking, BST):
        if self.root:
            self._ranking(self.root, fromranking, toranking, BST)
            return BST
    
    def _ranking(self, currentNode, fromranking, toranking, BST):
        if currentNode:
            if currentNode.ranking >= int(fromranking): 
                if currentNode.ranking <= int(toranking):
                    BST.insert(currentNode.ranking, currentNode.imdbID, currentNode.title, currentNode.year, 
                               currentNode.rating, currentNode.runtime, currentNode.genre, currentNode.director, 
                               currentNode.cast, currentNode.imdbRating, currentNode.poster, currentNode.language, 
                               currentNode.country)
            self._ranking(currentNode.left, fromranking, toranking, BST)
            self._ranking(currentNode.right, fromranking, toranking, BST)
        return BST
    
        
    # Implement the genre request    
    def genre(self, genre, BST):
        if self.root:
            self._genre(self.root, genre, BST)
            return BST
        
    def _genre(self, currentNode, genre, BST):   
        if currentNode:             
            if genre.lower() in currentNode.genre.lower():
                BST.insert(currentNode.ranking, currentNode.imdbID, currentNode.title, currentNode.year, 
                               currentNode.rating, currentNode.runtime, currentNode.genre, currentNode.director, 
                               currentNode.cast, currentNode.imdbRating, currentNode.poster, currentNode.language, 
                               currentNode.country)
            self._genre(currentNode.left, genre, BST)        
            self._genre(currentNode.right, genre, BST)
        return BST
   

    # Implement the year request
    def year(self, year_from, year_to, BST):
        if self.root:
            self._year(self.root, year_from, year_to, BST)
            return BST
    
    def _year(self, currentNode, year_from, year_to, BST):
        if currentNode:
            if currentNode.year >= int(year_from): 
                if currentNode.year <= int(year_to):
                    BST.insert(currentNode.ranking, currentNode.imdbID, currentNode.title, currentNode.year, 
                               currentNode.rating, currentNode.runtime, currentNode.genre, currentNode.director, 
                               currentNode.cast, currentNode.imdbRating, currentNode.poster, currentNode.language, 
                               currentNode.country)
            self._year(currentNode.left, year_from, year_to, BST)
            self._year(currentNode.right, year_from, year_to, BST)
        return BST

    
    # Implement the language request    
    def language(self, language, BST):
        if self.root:
            self._language(self.root, language, BST)
            return BST
        
    def _language(self, currentNode, language, BST):   
        if currentNode:             
            if language.lower() in currentNode.language.lower():
                BST.insert(currentNode.ranking, currentNode.imdbID, currentNode.title, currentNode.year, 
                               currentNode.rating, currentNode.runtime, currentNode.genre, currentNode.director, 
                               currentNode.cast, currentNode.imdbRating, currentNode.poster, currentNode.language, 
                               currentNode.country)
            self._language(currentNode.left, language, BST)        
            self._language(currentNode.right, language, BST)
        return BST


# Initial data input
def dataset_input():
    movie_combined = pd.read_csv(r'movie_combined.csv')
    bst = BST()
    for i in range(len(movie_combined)):
        bst.insert(movie_combined.loc[i][0], movie_combined.loc[i][1], movie_combined.loc[i][2], movie_combined.loc[i][3], 
                   movie_combined.loc[i][4], movie_combined.loc[i][5], movie_combined.loc[i][6], movie_combined.loc[i][7], 
                   movie_combined.loc[i][8], movie_combined.loc[i][9], movie_combined.loc[i][10], movie_combined.loc[i][11], 
                   movie_combined.loc[i][12])
    return bst


def ranking_input(BST_ORI, BST_AFT):
    yes = ["yes", 'y', 'yup', 'yep', 'sure']
    no = ['no', 'n', 'nope']
    
    ranking = input("Do you have preference for movie ranking? (yes/no) ")
    while ranking.lower() not in yes and ranking.lower() not in no:
        print("Invalid input. Please try again!")
        ranking = input("Do you have preference for movie ranking? (yes/no) ")   
    if ranking.lower() in yes:             
        top_ranking = input("Please enter your ranking request. From (an integer between 1-299):  ")
        low_ranking = input("Please enter your ranking request. To (an integer between 2-300):  ")
        print("\n")
        BST_AFT = BST_ORI.ranking(top_ranking, low_ranking, BST_AFT)
    
    elif ranking.lower() in no:     
        BST_AFT = BST_ORI
    return BST_AFT


def genre_input(BST_ORI, BST_AFT):
    yes = ["yes", 'y', 'yup', 'yep', 'sure']
    no = ['no', 'n', 'nope']
    
    genre_in = input("Do you have preference for the genre? (yes/no) ")
    while genre_in.lower() not in yes and genre_in.lower() not in no:
        print("Invalid input. Please try again!")
        genre_in = input("Do you have preference for the genre? (yes/no) ")   
    if genre_in.lower() in yes:  
        i = 0
        while(i == 0):
            print("Please enter your preferred genre.")
            genre = input("e.g. Action/Adventure/Comedy/Crime/Drama/Fantasy/History/Horror/Romance/Sci-Fi/Thriller/War... ")
            print("\n")
            BST_AFT = BST_ORI.genre(genre, BST_AFT)
            if BST_AFT.size == 0:
                print("No movies found under this genre. Please try another!")
            else:
                break
    elif genre_in.lower() in no:     
        BST_AFT = BST_ORI  
    return BST_AFT


def year_input(BST_ORI, BST_AFT):
    yes = ["yes", 'y', 'yup', 'yep', 'sure']
    no = ['no', 'n', 'nope']
    
    year_in = input("Do you have preference for movie's releasing year? (yes/no) ")
    while year_in.lower() not in yes and year_in.lower() not in no:
        print("Invalid input. Please try again!")
        year_in = input("Do you have preference for movie's releasing year? (yes/no) ")   
    if year_in.lower() in yes:     
        i = 0
        while(i == 0):
            print("Please enter your request for releasing year.")
            year_from = input("From (an integer between 1931-2015):  ")
            year_to = input("To (an integer between 1931-2015):  ")
            print("\n")
            BST_AFT = BST_ORI.year(year_from, year_to, BST_AFT)   
            if BST_AFT.size == 0:
                print("No movies found between this range. Please try again!")
            else:
                break
    elif year_in.lower() in no:     
        BST_AFT = BST_ORI
    
    return BST_AFT


def language_input(BST_ORI, BST_AFT):
    yes = ["yes", 'y', 'yup', 'yep', 'sure']
    no = ['no', 'n', 'nope']
    
    lan_in = input("Do you have preference for the language? (yes/no) ")
    while lan_in.lower() not in yes and lan_in.lower() not in no:
        print("Invalid input. Please try again!")
        lan_in = input("Do you have preference for the language? (yes/no) ")   
    if lan_in.lower() in yes:  
        i = 0
        while(i == 0):
            print("Please enter your preferred language.")
            language = input("e.g. Arabic/Cantonese/Chinese/English/French/German/Italian/Japanese/Mandarin/Russian/Spanish... ")
            print("\n")
            BST_AFT = BST_ORI.language(language, BST_AFT)
            if BST_AFT.size == 0:
                print("No movies found in this language. Please try another!")
            else:
                break
    elif lan_in.lower() in no:     
        BST_AFT = BST_ORI  
    return BST_AFT


def detail_input(BST):
    yes = ["yes", 'y', 'yup', 'yep', 'sure']
    no = ['no', 'n', 'nope']
    
    i = 0
    while(i == 0):
        detail_in = input("Do you want to check detail information? (yes/no) ")
        while detail_in.lower() not in yes and detail_in.lower() not in no:
            print("Invalid input. Please try again!")
            detail_in = input("Do you want to check detail information? (yes/no) ")   
        if detail_in.lower() in yes:  
            ranking =  input("Please enter the rank of the movie (an integer): ")
            print("\n")
            print(BST.print_detail(int(ranking)))
        elif detail_in.lower() in no:     
            break


def main():
    print("Welcome!")
    print("Have no idea of which movie to watch?")
    print("We will give you recommendations! Find your movie now!")
    
    bst = dataset_input()
    bst1 = BST()
    bst1 = ranking_input(bst, bst1)
    #bst1.print_list()
    
    bst2 = BST()
    bst2 = genre_input(bst1, bst2)
    #bst2.print_list()
    
    bst3 = BST()
    bst3 = year_input(bst2, bst3)
    #bst3.print_list()
    
    bst4 = BST()
    bst4 = language_input(bst3, bst4)
    print("Here are our recommendations!")
    bst4.print_list()
    detail_input(bst4)
    
    print("Bye!")


if __name__ == '__main__':
    main()

