/*
 * This Javascript file is for the book_results html template. 
 * It appends the book isbn or author id, which are stored as
 * the id of the buttons, to the action and redirects to that app route.
 * 
 * Handles buttons for seeing comments for a book, the author of a book, 
 * and marking a book as read.
 * All database logic is done on server.
 * 
 */
$(document).ready(function(){
    //The comments button appends the isbn of the book and redirect to that app route.
    $(".comments").click(function(){
        id = this.id;
        url = "/see_comments/" + id;
        window.location.assign(url);
    });
    //The authors button appends the author_id, stored as the button id attribute, and redirects.
    $(".authors").click(function(){
        id = this.id;
        console.log(id);
        url = "/see_authors/" + id;
        console.log(url);
        window.location.assign(url);
    });
    //The read button appends the book isbn and redirects. 
    $(".read").click(function(){
        book_isbn = id = this.id;
        url = "/read_book/" + book_isbn;
        console.log(url);
        window.location.assign(url);
    });
});