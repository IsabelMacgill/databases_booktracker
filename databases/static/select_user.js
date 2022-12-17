/* This is JavaScript file for the index.html file which allows for visitors to select which user they are.
 * 
 * Each user div has a button with class = '.select_user' and id = that user's id. 
 * When clicked, it redirects to save_user + id app route, where it sets the global user variable and queries the database.
 * 
 * If the just browse button is selected, the user id of this button tis 0, which does not exist in the database. 
 * This button redirects to the save_user + id app route, but query will return none and the server directs to the seach_home app route. 
 */
$(document).ready(function(){
    //The buttons in this class have the users' ids as the button ids. 
    $(".select_user").click(function(){
        id = this.id;
        url = "/save_user/" + id;
        console.log(url);
        window.location.assign(url);

    });
    //This button has 0 (nonexistent) user id as its id.
    $(".just_browsing").click(function(){
        id = this.id;
        url = "/save_user/" + id;
        console.log(url);
        window.location.assign(url);

    });
});