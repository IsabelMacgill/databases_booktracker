/* This is JavaScript file for the comments.html file, for the adding comments on a book.
 * 
 * This takes in the comment's content and the  the book's isbn and the user_id.
 * Before sending them to the server, it makes sure there is content in the comment.
 * 
 */
function add_comment(){
    //gets data from the input boxes and the id from the content
    let data_to_save = {
        content: $(".content").val(),
        isbn: $(".content")[0].id,
    };
    $.ajax({ 
        type: "POST",
        //app route
        url: "add_comment",
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
                let success = new $("<div class='alert alert-success' role='alert'>Comment added successfully!</div>");
                $("#adding").append(success);
            }
        },
        //if there was an error, log that error
        error: function (request, status, error) {
          console.log("Error");
          console.log(request);
          console.log(status);
          console.log(error);
        }, 
    });  
}

//This function makes sure that the comment's content is not left blank, and appends a warning instead of sending if so.
function check_input(){
    if($("#content").val().length <= 0){
        let warning = new $("<div class='alert alert-warning' role='alert'> Please enter an author name.</div>");
        $("#author").append(warning);
        return false;
    }
    return true;
}

//The adding button removes any existing warning divs, checks the inputs, and then calls the add_comment function.
$(document).ready(function(){
    $("#adding").submit(function(event){
        event.preventDefault();
        $(".alert").remove();
        add_comment();
    });
});