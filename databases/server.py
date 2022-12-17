
"""
Book Tracker Webserver
To run locally:
    python3 server.py
Go to http://localhost:8111 in your browser.
"""
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, jsonify, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

user_id = 0
user_info = None

DATABASEURI = "postgresql://srb2225:9173@34.75.94.195/proj1part2"

engine = create_engine(DATABASEURI)

#setup
@app.before_request
def before_request():
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None


#teardown
@app.teardown_request
def teardown_request(exception):
  try:
    g.conn.close()
  except Exception as e:
    pass


#homepage shows all users and lets people selct which user they are
@app.route('/')
def index():
  #get all users
  cursor = g.conn.execute("""
  SELECT * 
  FROM Users
  """)
  users = []
  for result in cursor:
    users.append(result)
  cursor.close()
  context = dict(data = users)
  return render_template("index.html", **context)


# #setting global user_id and user_info vars to the user_id & corresponding user tuple selected
@app.route('/save_user/<id>')
def saveUser(id):
  #setting the global vars of user_id and user_info
  global user_id
  global user_info
  user_id = id
  #getting the user tuple from the database based on the passed id
  cursor = g.conn.execute("""
  SELECT * 
  FROM Users U 
  WHERE U.user_id = %s
  """, user_id)
  user_info = cursor.first()
  cursor.close()
  #setting the context: currently selected user
  context = dict(user = user_info)
  #if default (no user selected), show browsing page
  if id == '0':
    return render_template("search_home.html", **context)
  #else show the profile page
  else:
    return render_template("user_tracker.html", **context)


#browsing and searching home
@app.route('/search_home')
def search_home():
  global user_info
  #set the context: just need the currently selected user
  context = dict(user = user_info)
  return render_template("search_home.html", **context)


#search all books for a specifc substring in their title
@app.route('/book_search/<term>')
def showBooks(term=None):
  title = term
  #if a user was selected, get which books they have already read (no option to mark as read)
  read_isbn = []
  if user_info is not None:
    cursor_read = g.conn.execute("""
    SELECT R.isbn 
    FROM Read R 
    WHERE R.user_id = %s
    """, user_id)
    for result in cursor_read:
      read_isbn.append(result[0])
    cursor_read.close()
  #get books with the substring in their title
  term = '%' + term + '%'
  cursor = g.conn.execute("""
  SELECT * 
  FROM Books B
  WHERE B.title LIKE %s
  """, term)
  books = []
  for result in cursor:
    books.append(result)
  cursor.close()
  #set the context: books wtih substring in title, action & entity & term searching for (so we can reuse templates), read books, and currently selected user
  context = dict(data = books, action = "Searching", entity = "Books", term = "for " + title, read_books = read_isbn, user = user_info)
  return render_template("book_results.html", **context)


#browsing, need to show all book tuples
@app.route('/books_browse')
def browseBooks():
  #if a user was selected, get which books they have already read (no option to mark as read)
  read_isbn = []
  if user_info is not None:
    cursor_read = g.conn.execute("""
    SELECT R.isbn
    FROM Read R
    WHERE R.user_id = %s
    """, user_id)
    for result in cursor_read:
      read_isbn.append(result[0])
    cursor_read.close()
  #select all books: browsing, need to show all
  cursor = g.conn.execute("""
  SELECT * 
  FROM Books""")
  books = []
  for result in cursor:
    books.append(result)
  cursor.close()
  #set the context: all books, action & entity (so we can reuse templates), read books, and currently selected user
  context = dict(data = books, action = "Browsing", entity = "Books", read_books = read_isbn, user = user_info)
  return render_template("book_results.html", **context)


#show the add bool form
@app.route('/add_book')
def addBooksPage():
  return render_template('add_book.html')


#save book
@app.route('/save_book', methods=['POST'])
def addBooks(): 
  #using json because we do input validation and attach warning on client javscript file
  json = request.get_json()
  author = json['author']
  book = json['title']
  isbn = json['isbn']
  pages = json['pages']
  date = json['date']
  #send back a specific response if unsuccessfu;
  response = ""
  #check if there is already a book with this isbn
  isbn_repeat = g.conn.execute("SELECT B.isbn FROM Books B WHERE B.isbn = %s", isbn)
  repeats = isbn_repeat.first()
  isbn_repeat.close()
  #if yes, populate response with message
  if repeats is not None :
    response = "There is already a book with this ISBN. Please try again."
  else:
    a_cursor = g.conn.execute("SELECT A.author_id FROM Authors A WHERE A.auth_name = %s", author)
    authors = []
    for result in a_cursor:
      authors.append(result)
    a_cursor.close()
    #if the author of the book does not exist: need to add new author to database before referncing in books
    if(len(authors) == 0):
      #get the last author_d
      id_cursor =  g.conn.execute("SELECT A.author_id FROM Authors A ORDER BY A.author_id DESC LIMIT 1")
      last_id = id_cursor.first()[0]
      #add one to last id to get new id
      id = last_id + 1
      #insert author
      g.conn.execute("INSERT INTO Authors(author_id, auth_name) VALUES(%s, %s)", id, author)
    #otherwsie author already exists, get that author's id
    else:
      id = authors[0][0]
    #if user input for book included num_pages and date
    if(len(pages) > 0 and len(date) > 0):
      try:
        g.conn.execute("INSERT INTO Books(isbn, title, author_id, date_published, num_pages) VALUES(%s, %s, %s, %s, %s)", isbn, book, id, date, pages)
      #date is not formatted correctly, send back error message
      except: 
        response= "Make sure your date is formatted correctly."
    #if user input for book just included pages & no date
    elif (len(pages) > 0):
      g.conn.execute("INSERT INTO Books(isbn, title, author_id, num_pages) VALUES(%s, %s, %s, %s)", isbn, book, id, pages)
    #if user input for book just included date & no pages
    elif(len(date) > 0):
      try:
        g.conn.execute("INSERT INTO Books(isbn, title, author_id, date_published) VALUES(%s, %s, %s, %s)", isbn, book, id, date)
      except: 
         response= "Make sure your date is formatted correctly."
    #if user input for book did not include date or page numbers
    else:
      g.conn.execute("INSERT INTO Books(isbn, title, author_id) VALUES(%s, %s, %s)", isbn, book, id)
  #return json of response string so we can append nice warnings over relevant input boxes
  return jsonify(response)


# Seeing comments for a specific book
@app.route('/see_comments/<isbn>')
def seeComments(isbn):
  #get the title of the book to show even if there are no comments
  title_cursor = g.conn.execute("""
  SELECT *
  FROM Books B
  WHERE B.isbn = %s
  """, isbn)
  title = title_cursor.first()
  title_cursor.close()
  #get all the comments and the users who wrote them, and the book title
  cursor = g.conn.execute("""
  SELECT C.content, C.name
  FROM (CommentsOnBooks NATURAL JOIN Users) C
  WHERE C.isbn = %s
  """, isbn)
  comments = []
  for result in cursor:
    comments.append(result)
  cursor.close()
  #set the context: all comments, title of book looking at, and currently selected user
  context = dict(data = comments, title = title, user = user_info)
  return render_template("comments.html", **context)


#seeing a user's friends, if a user is selected
@app.route('/see_comments/add_comment', methods=['POST'])
def addComments():
  json = request.get_json()
  content = json['content']
  isbn = json['isbn']
  #set up json response string to send back and append specfic warning messages if needed
  response = ""
  #get the last author id from Authors
  cursor = g.conn.execute("SELECT * FROM CommentsOnBooks C ORDER BY C.comment_id DESC LIMIT 1")
  ids = cursor.first()
  cursor.close()
  last_id = ids[0]
  #increment the last id by 1 for the new addition
  last_id += 1
  print(id)
  print(content)
  g.conn.execute("INSERT INTO CommentsOnBooks(comment_id, isbn, user_id, content) VALUES(%s, %s, %s, %s)", last_id, isbn, user_id, content)
  return jsonify(response)


#seeing the author of a specific book
@app.route('/see_authors/<id>')
def seeAuthor(id):
  #find the liked authors for current user if a user is selected
  liked_authors = []
  if user_info is not None:
    cursor_liked = g.conn.execute("""
      SELECT A.author_id FROM Likes_Author A 
      WHERE A.user_id = %s
      """, user_id)
    for result in cursor_liked:
      liked_authors.append(result[0])
    cursor_liked.close()
  #get the author matching this id
  cursor = g.conn.execute("""
  SELECT * FROM Authors A 
  WHERE A.author_id = %s
  """, id)
  authors = []
  authors.append(cursor.first())
  cursor.close()
  #set the context: the author, action & entity (so we can reuse templates), liked authors, and currently selected user
  context = dict(data = authors, action = "Viewing ", entity= "Author", liked_authors = liked_authors, user = user_info)
  return render_template("author_results.html", **context)


#marking a book as read
@app.route('/read_book/<isbn>')
def likeBook(isbn):
  #if a user is selected, mark them as having read the book
  if user_info is not None:
    g.conn.execute("""
    INSERT INTO READ(user_id, isbn) VALUES(%s, %s)
    """, user_id, isbn)
  #set the context: currently selected user
  context = dict(user = user_info)
  return render_template("search_home.html", **context)


#searching an author for a substring
@app.route('/author_search/<term>')
def showAuthors(term):
  #find the liked authors for current user if a user is selected (so we can disable/mark out their like button)
  liked_authors = []
  if user_info is not None:
    cursor_liked = g.conn.execute("""
      SELECT A.author_id FROM Likes_Author A 
      WHERE A.user_id = %s
      """, user_id)
    for result in cursor_liked:
      liked_authors.append(result[0])
    cursor_liked.close()
  #get all authors with name matching searched subtring
  author = '%' + term + '%'
  cursor = g.conn.execute("""
  SELECT * FROM Authors A
  WHERE A.auth_name LIKE %s
  """, author)
  authors = []
  for result in cursor:
    authors.append(result)
  cursor.close()
  #set the context: authors matching search, action & entity & search term (so we can reuse templates), liked authors, and currently selected user
  context = dict(data = authors, action = "Searching", entity= "Authors", title = "for " + term, liked_authors = liked_authors, user = user_info)
  return render_template("author_results.html", **context)


#browse all authors
@app.route('/authors_browse')
def browseAuthors():
  #find the liked authors for current user if a user is selected (so we can disable/mark out their like button)
  liked_authors = []
  if user_info is not None:
    cursor_liked = g.conn.execute("""
      SELECT A.author_id FROM Likes_Author A 
      WHERE A.user_id = %s
      """, user_id)
    for result in cursor_liked:
      liked_authors.append(result[0])
    cursor_liked.close()
  #get all the authors because we are browsing
  cursor = g.conn.execute("""
  SELECT * 
  FROM Authors A
  """)
  authors = []
  for result in cursor:
    authors.append(result)
  cursor.close()
  #set the context: all authors, action & entity (so we can reuse templates), liked authors, and currently selected user
  context = dict(data = authors, action = "Browsing", entity = "Authors", liked_authors = liked_authors, user = user_info)
  return render_template("author_results.html", **context)


#like an author
@app.route('/like_author/<id>')
def likeAuthors(id):
  #if there is a currently selected user, mark that user as like this author
  if user_info is not None:
    g.conn.execute("""
    INSERT INTO Likes_Author(user_id, author_id) VALUES(%s, %s)
    """, user_id, id)
  #set the context: currently selected user
  context = dict(user = user_info)
  return render_template("search_home.html", **context)


#add an author template
@app.route('/add_author')
def addAuthorPage():
  return render_template('add_author.html')


#add an author logic
@app.route('/save_author', methods=['POST'])
def saveAuthor():
  #using JSON because we are doing input validation and appending warning methods for each input box on client side
  json = request.get_json()
  name = json['name']
  num_books = json['num_books']
  #set up json response string to send back and append specfic warning messages if needed
  response = ""
  #get the last author id from Authors
  cursor = g.conn.execute("SELECT * FROM Authors A ORDER BY A.author_id DESC LIMIT 1")
  ids = cursor.first()
  cursor.close()
  last_id = ids[0]
  #increment the last id by 1 for the new addition
  last_id += 1
  #if user input included how many books the author has written
  if(len(num_books) > 0):
    g.conn.execute("INSERT INTO Authors(author_id, auth_name, num_books) VALUES(%s, %s, %s)", last_id, name, num_books)
  else:
    g.conn.execute("INSERT INTO Authors(author_id, auth_name) VALUES(%s, %s)", last_id, name)
  return jsonify(response)


#genre search
@app.route('/genre_search/<term>')
def showGenres(term):
  #find the liked genres for current user if a user is selected (so we can disable the like button for those genres)
  liked_genres = []
  if user_info is not None:
    cursor_liked = g.conn.execute("""
      SELECT G.genre_id FROM Likes_Genre G 
      WHERE G.user_id = %s
      """, user_id)
    for result in cursor_liked:
      liked_genres.append(result[0])
    cursor_liked.close()
  #find genres with matching substring
  search = '%' + term + '%'
  cursor = g.conn.execute("""
  SELECT * 
  FROM Genre 
  WHERE Genre.gname 
  LIKE %s""", search)
  genres = []
  for result in cursor:
    genres.append(result)
  cursor.close()
  #set the context: genres with matching substring, action & entity & search term (so we can reuse templates), liked genres, and currently selected user
  context = dict(data = genres, action="Searching", entity = "Genres", term= "for " + term, liked_genres = liked_genres, user = user_info)
  return render_template("genre_wishlist_results.html", **context)


#browse for genres
@app.route('/genre_browse')
def browseGenre():
  #find the liked genres for current user if a user is selected (so we can disable the like button for those genres)
  liked_genres = []
  if user_info is not None:
    cursor_liked = g.conn.execute("""
      SELECT G.genre_id 
      FROM Likes_Genre G 
      WHERE G.user_id = %s
      """, user_id)
    for result in cursor_liked:
      liked_genres.append(result[0])
    cursor_liked.close()
  #get all genres to browse
  cursor = g.conn.execute("""SELECT * FROM Genre""")
  genres = []
  for result in cursor:
    genres.append(result)
  cursor.close()
  #set the context: all genres, action & entity (so we can reuse templates), liked genres, and currently selected user
  context = dict(data = genres, action="Browsing ", entity = "Genres", liked_genres = liked_genres, user = user_info)
  return render_template("genre_wishlist_results.html", **context)


#like a genre
@app.route('/like_genre/<id>')
def likeGenre(id):
  #if there is a current user, mark this user as liking that genre
  if user_info is not None:
    g.conn.execute("""
    INSERT INTO Likes_Genre(user_id, genre_id) VALUES(%s, %s)
    """, user_id, id)
  #set the context: currently selected user
  context = dict(user = user_info)
  return render_template("search_home.html", **context)


#see all the books in a genre
@app.route('/see_books_genre/<id>')
def seeBooksGenre(id):
  #get all the books belonging to the genre
  books = []
  cursor = g.conn.execute("""
  SELECT B.isbn, B.title, B.author_id, B.date_published, B.num_pages
  FROM (Books NATURAL JOIN Is_Genre) B
  WHERE B.genre_id = %s
  """, id)
  for result in cursor: 
    books.append(result)
  cursor.close()
  #if a user was selected, get which books they have already read (no option to mark as read)
  read_isbn = []
  if user_info is not None:
    cursor_read = g.conn.execute("""
    SELECT R.isbn
    FROM Read R
    WHERE R.user_id = %s
    """, user_id)
    for result in cursor_read:
      read_isbn.append(result[0])
  #get the name of the genre
  g_cursor = g.conn.execute("""
  SELECT G.gname
  FROM Genre G
  WHERE G.genre_id = %s
  """, id)
  gname = g_cursor.first()
  if gname is not None:
    gname = gname[0]
  g_cursor.close()
  #set the context: all books in genre, action & entity & which genre (so we can reuse templates), read books, and currently selected user
  context = dict(data = books, action = "Seeing", entity = "Books", title = "in " + gname, read_books = read_isbn, user = user_info)
  return render_template("book_results.html", **context)


#searching the user's wishlists (should only show up if user is selected)
@app.route('/wishlist_search/<term>')
def showWishlists(term):
  #get wishlists created by the current user that have a mataching substring
  wishlists = []
  if user_info is not None:
    name = '%' + term + '%'
    cursor = g.conn.execute("""
    SELECT * 
    FROM (Wishlists NATURAL JOIN User_Has_Wishlist) W 
    WHERE W.user_id = %s AND W.wname LIKE %s
    """, user_id, name)
    for result in cursor:
      wishlists.append(result)
    cursor.close()
  #set the context: wishlists, action & entity & search term (so we can reuse templates), and currently selected user
  context = dict(data = wishlists, action="Searching", entity = "Wishlists", term = "for " + term, user = user_info)
  return render_template("genre_wishlist_results.html", **context)


#browsing a users' created wishlists if a user is selected
@app.route('/wishlist_browse')
def browseWishlists():
  #get all wishlists created by the current user
  wishlists = []
  if user_info is not None:
    cursor = g.conn.execute("""
    SELECT * 
    FROM (Wishlists NATURAL JOIN User_Has_Wishlist) W 
    WHERE W.user_id = %s
    """, user_id)
    for result in cursor:
      wishlists.append(result)
    cursor.close()
  #set the context: wishlists, action & entity (so we can reuse templates), currently selected user
  context = dict(data = wishlists, action="Browsing ", entity = "Wishlists", user = user_info)
  return render_template("genre_wishlist_results.html", **context)


#see all the books in a wishlist
@app.route('/see_books_wishlists/<id>')
def seeBooksWishlists(id):
  #see all the books for the given wishlist
  if user_info is not None:
    books = []
    cursor = g.conn.execute("""
    SELECT B.isbn, B.title, B.author_id, B.date_published, B.num_pages
    FROM (Books NATURAL JOIN Wishlist_Contains) B
    WHERE B.wishlist_id = %s
    """, id)
    for result in cursor: 
      books.append(result)
    cursor.close()
    #if a user was selected, get which books they have already read (no option to mark as read)
    read_isbn = []
    if user_info is not None:
      cursor_read = g.conn.execute("""
      SELECT R.isbn
      FROM Read R
      WHERE R.user_id = %s
      """, user_id)
      for result in cursor_read:
        read_isbn.append(result[0])
  #get the name of the wishlist
  w_cursor = g.conn.execute("""
  SELECT W.wname
  FROM Wishlists W
  WHERE W.wishlist_id = %s
  """, id)
  wname = w_cursor.first()
  if wname is not None:
    wname = wname[0]
  w_cursor.close()
  #set the context: all books in wishlist, action & entity  & title of wishlist (so we can reuse templates), read books, and currently selected user
  context = dict(data = books, action = "Seeing", entity = "Wishlists", title = "in " + wname, read_books = read_isbn, user = user_info)
  return render_template("book_results.html", **context)


#profile homepage, see your own likes, wishlists, and read
@app.route('/user_tracker')
def showUserTracker():
  context = dict(user = user_info)
  return render_template('user_tracker.html', **context)


#showing the user's read books, is a user is selected
@app.route('/read_books')
def readBooks():
  #get the read books of the currently selected user
  books = []
  if user_info is not None:
    cursor = g.conn.execute("""
    SELECT B.isbn, B.title, B.author_id, B.date_published, B.num_pages
    FROM (Books NATURAL JOIN Read) B
    WHERE B.user_id = %s
    """, user_id)
    for result in cursor:
      books.append(result)
    cursor.close()
  #set the context: read boojs, action & entity (so we can reuse templates), and currently selected user
  context = dict(data = books, action="Viewing your", entity = "Read Books", user=user_info)
  return render_template("book_results.html", **context)


#showing the user's liked authors, if there is a selected user
@app.route('/liked_authors')
def likedAuthors():
  #get the liked authors of the currently selected user
  authors = []
  if user_info is not None:
    cursor = g.conn.execute("""
    SELECT A.author_id, A.auth_name, A.num_books
    FROM (Authors NATURAL JOIN Likes_Author) A
    WHERE A.user_id = %s
    """, user_id)
    for result in cursor:
      authors.append(result)
    cursor.close()
  #set the context: liked authors, action & entity (so we can reuse templates), and currently selected user
  context = dict(data = authors, action="Viewing your", entity = "Liked Authors", user = user_info)
  return render_template("author_results.html", **context)


#seeing a user's liked genres, if a user is selected
@app.route('/liked_genres')
def likedGenres():
  genres = []
  #get the liked genres for the current user
  if user_info is not None:
    cursor = g.conn.execute("""
    SELECT G.genre_id, G.gname
    FROM (Genre NATURAL JOIN Likes_Genre) G
    WHERE G.user_id = %s
    """, user_id)
    for result in cursor:
      genres.append(result)
    cursor.close()
  #set the context: liked genres, action & entity (so we can reuse templates), and currently selected user
  context = dict(data = genres, action="Viewing your", entity = "Liked Genres", user = user_info)
  return render_template("genre_wishlist_results.html", **context)


#seeing a user's friends, if a user is selected
@app.route('/friends')
def friends():
  #get the names of friends of the current user (if the current user is user_1 or user_2 in friendship)
  friends = []
  if user_info is not None:
    cursor = g.conn.execute("""
    SELECT F1.name 
    FROM 
      (SELECT * 
      FROM (Users U JOIN Friends F ON U.user_id = F.user1_id OR U.user_id = F.user2_id) 
      WHERE (F.user1_id = %s  OR F.user2_id = %s)) 
    AS F1 
    WHERE NOT F1.user_id = %s
    """, user_id, user_id, user_id)
    for result in cursor:
      friends.append(result)
    cursor.close()
  #set the context: names of friends, and currently selected user
  context = dict(data = friends, user = user_info)
  return render_template("friends.html", **context)



if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python3 server.py

    Show the help text using:

        python3 server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
