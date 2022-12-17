/* This is JavaScript file for the add_booksr.html file, for the adding book page.
 * 
 * This takes in the book's title, isbn, author, number of pages and date published from the input boxes. 
 * Before sending them to the server, it makes sure there is a title, isbn, and author value.
 * 
 * If the insertion fails, the response text is sent back and appended as a warning.
 */
function add_book(){
    //get the data from the input boxes
    let data_to_save = {
        title: $("#book_title").val(),
        author: $("#author_name").val(),
        isbn: $("#isbn_number").val(),
        pages: $("#num_pages").val(),
        date: $("#date_published").val(),
    };
    $.ajax({ 
        type: "POST",
        //app route
        url: "save_book",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data_to_save),
        success: function(result){
            //result text will not be '' if there is an error message, so we should that error
            if(result.length > 1){
                let warning = new $("<div class='alert alert-warning' role='alert'>" + result +"</div>");
                $("#adding").append(warning);
            }
            //if result = '' then there was no error, sucessfully inserted author(if needed) and book tuple
            else{
                $(".form-control").val('');
                let success = new $("<div class='alert alert-success' role='alert'>Book added successfully!</div>");
                $("#adding").append(success);
            }
        },
        //print error info
        error: function (request, status, error) {
          console.log("Error");
          console.log(request);
          console.log(status);
          console.log(error);
        }, 
    });  
}

function check_input(){
    //book title should not be blank
    if($("#book_title").val().length <= 0){
        let warning = new $("<div class='alert alert-warning' role='alert'> Please enter a book title.</div>");
        $("#book").append(warning);
        return false;
    }
    //author name should not be blank, because we will use this to find or create author_id on server
    if($("#author_name").val().length <= 0){
        let warning = new $("<div class='alert alert-warning' role='alert'> Please enter an author name.</div>");
        $("#author").append(warning);
        return false;
    }
    //isbn number should not be blank because this is the primary key
    if($("#isbn_number").val().length <= 0){
        let warning = new $("<div class='alert alert-warning' role='alert'> Please enter an ISBN number.</div>");
        $("#isbn").append(warning);
        return false;

    }
    //if all conditions pass, return true
    return true;
}

$(document).ready(function(){
    //submiting button: check the inputs, then pass to posting method
    $("#adding").submit(function(event){
        event.preventDefault();
        //remove any alerts from previous tries before rechecking
        $(".alert").remove();
        if(check_input()){
            add_book();
        }
    });
});