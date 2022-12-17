/* This is JavaScript file for the search_home.html file, or for the viewing/browsing page.
 * 
 * This page has buttons to see books, authors, genres, and if a user is selected then their wishilsts.
 * There are text boxes to search those fields, and the search term is appended to the url and
 * the server queries the proper table for that term.
 * For author and books, there are also buttons to add new tuples. 
 * 
 */
$(document).ready(function(){
    //The search button is combined with the form input and redirecting to the corresponding app route.
    $("#search_books").submit(function(event){
        event.preventDefault();
        //The url includes the substring being searched for.
        url = "/book_search/" + $("#search_books_input").val();
        console.log(url);
        window.location.assign(url);
    });
    //The browse books button redirects to the books_browse app route. 
    $("#browse_books").click(function(){
        url = "/books_browse";
        console.log(url);
        window.location.assign(url);
    });
    //The add book button redirects to the add_book app route. 
    $("#add_book").click(function(){
        url = "/add_book";
        console.log(url);
        window.location.assign(url);
    });
    //The search button is combined with the form input and redirecting to the corresponding app route.
    $("#search_authors").submit(function(event){
        event.preventDefault();
        //The url includes the substring being searched for.
        url = "/author_search/" + $("#search_authors_input").val();
        console.log(url);
        window.location.assign(url);
    });
    //The browse authors button redirects to the authors_browse app route. 
    $("#browse_authors").click(function(){
        url = "/authors_browse";
        console.log(url);
        window.location.assign(url);
    });
    //The add author button redirects to the add_author app route. 
    $("#add_author").click(function(){
        url = "/add_author";
        console.log(url);
        window.location.assign(url);
    });
    //The search button is combined with the form input and redirecting to the corresponding app route.
    $("#search_genres").submit(function(event){
        event.preventDefault();
        //The url includes the substring being searched for.
        url = "/genre_search/" + $("#search_genres_input").val();
        console.log(url);
        window.location.assign(url);
    });
    //The browse genres button redirects to the genre_browse app route. 
    $("#browse_genres").click(function(){
        url = "/genre_browse";
        console.log(url);
        window.location.assign(url);
    });
    //The search button is combined with the form input and redirecting to the corresponding app route.
    $("#search_wishlists").submit(function(event){
        event.preventDefault();
        //The url includes the substring being searched for.
        url = "/wishlist_search/" + $("#search_wishlists_input").val();
        console.log(url);
        window.location.assign(url);
    });
    //The browse wishlists button redirects to the wishlist_browse app route. 
    $("#browse_wishlists").click(function(){
        url = "/wishlist_browse";
        console.log(url);
        window.location.assign(url);
    });
});