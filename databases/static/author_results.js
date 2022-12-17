/*
 * This Javascript file is for the author_results html template. 
 * It appends the author_id, which are stored as
 * the id of the buttons. to the action and redirect to that app route.
 * 
 * Handles buttons for liking authors.
 * All database logic is done on server.
 * 
 */
$(document).ready(function(){
    //Like authors button have class = like and id = id of the author. 
    // Appends author to like route and redirects.
    $(".like").click(function(){
        auth_id = this.id;
        url = "/like_author/" + auth_id;
        console.log(url);
        window.location.assign(url);
    });
});