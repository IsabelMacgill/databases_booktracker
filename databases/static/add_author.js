/* This is JavaScript file for the add_author.html file, for the adding author page.
 * 
 * This takes in the author's name and the number of books they've written from the two inboxes. 
 * Before sending them to the server, it makes sure there is an auhtor's name value and if not appends a warning.
 * 
 * If the insertion fails, the response text is sent back and appended as a warning.
 */
function add_author(){
    //gets data from the input boxes
    let data_to_save = {
        name: $("#author_name").val(),
        num_books: $("#number_books").val(),
    };
    $.ajax({ 
        type: "POST",
        //app route
        url: "save_author",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data_to_save),
        success: function(result){
            //if there is a result message, the query was not successsful (logic in server)
            if(result.length > 1){
                let warning = new $("<div class='alert alert-warning' role='alert'>" + result +"</div>");
                $("#adding").append(warning);
            }
            //if the entry was successful, append success message
            else{
                $(".form-control").val('');
                let success = new $("<div class='alert alert-success' role='alert'>Book added successfully!</div>");
                $("#adding").append(success);
            }
        },
        //if there was an error, log that
        error: function (request, status, error) {
          console.log("Error");
          console.log(request);
          console.log(status);
          console.log(error);
        }, 
    });  
}

//This function makes sure that the author's name is not left blank, and appends a warning instead of sending if so.
function check_input(){
    if($("#author_name").val().length <= 0){
        let warning = new $("<div class='alert alert-warning' role='alert'> Please enter an author name.</div>");
        $("#author").append(warning);
        return false;
    }
    return true;
}

//The adding button removes any existing warning divs, checks the inputs, and then calls the save_author function.
$(document).ready(function(){
    $("#adding").submit(function(event){
        event.preventDefault();
        $(".alert").remove();
        if(check_input()){
            add_author();
        }
    });
});