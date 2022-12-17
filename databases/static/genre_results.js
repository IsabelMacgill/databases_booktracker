/*
 * This Javascript file is for the genre_wishlists_results html template. 
 * It appends the genre id or wishlist id, which are stored as
 * the id of the buttons. to the action and redirect to that app route.
 * 
 * Handles buttons for liking genres and seeing the books belonging to genres and wishlists.
 * All database logic is done on server.
 * 
 */
$(document).ready(function(){
    //Each genre item has a button with the class = like, and the id = the id of the genre.
    //Clicking this needs to mark the genre as liked. 
    //It redirects to the like_genre with the genre id app route, where server handles this.
    $(".like").click(function(){
        g_id = this.id;
        url = "/like_genre/" + g_id;
        console.log(url);
        window.location.assign(url);
    });
    //Each genre item has a button with the class = see_books, and the id = the id of the genre.
    //Clicking this needs to display the books in the genre. 
    //It redirects to the see_books_genre with the genre id app route, where server handles this.
    $(".see_books").click(function(){
        id = this.id;
        url = "/see_books_genre/" + id;
        window.location.assign(url);
    });
    //This html template is also used for displaying wishlists.
    //Each wishlist item has a button with the class = see_books_wishlist, and the id = the id of the wishlist.
    //Clicking this needs to display the books in the wishlist. 
    //It redirects to the see_books_wishlists with the wishlist id app route, where server handles this.
    $(".see_books_wishlists").click(function(){
        id = this.id;
        url = "/see_books_wishlists/" + id;
        window.location.assign(url);
    });
});