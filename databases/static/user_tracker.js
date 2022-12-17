/* This is JavaScript file for the user_tracker.html file, or for the viewing profile page.
 * 
 * If a user is selected, they have buttons to see the books they've read, the authors they've liked,
 * the genres they've liked, the wishlists they've created, and the users they are friends with. 
 * 
 * If a user is not selected, they are not shown this and prompted to go back to the select user page.
 */
$(document).ready(function(){
    //The button to see read books redirects to read_books app route in server. 
    $("#read_books").click(function(){
        url = "/read_books";
        console.log(url);
        window.location.assign(url);
    });
    //The button to see liked authors redirects to liked_authors app route in server. 
    $("#liked_authors").click(function(){
        url = "/liked_authors";
        console.log(url);
        window.location.assign(url);
    });
    //The button to see liked genres redirects to liked_genres app route in server. 
    $("#liked_genres").click(function(){
        url = "/liked_genres";
        console.log(url);
        window.location.assign(url);
    });
    //The button to see your wishlists redirects to wishlists_browse app route in server. 
    $("#created_wishlists").click(function(){
        url = "/wishlist_browse";
        console.log(url);
        window.location.assign(url);
    });
    //The button to see your friends redirects to friends app route in server. 
    $("#friends").click(function(){
        url = "/friends";
        console.log(url);
        window.location.assign(url);
    });
    /* If no user is selected yet, all of the above buttons and corresponding divs are not shown.
     * Instead this button to redirects to index app route in server which shows users.
     */
    $("#select_user").click(function(){
        url = "/";
        console.log(url);
        window.location.assign(url);
    });
});