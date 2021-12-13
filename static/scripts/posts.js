var users = {}

$(document).ready(function() {
    var filter_by = 0;

    getUsernames();


    getPosts();

    $('#new_post').click(function() {
        var text = $('#new_post_text').val();
        $.ajax({
            url: "/posts",
            type: "post",
            data: { text: text },
            success: function(response) {

                //TODO do something with the response 

                // $("#wordResult").html(response.html);
            },
            error: function(xhr) {
                //Do Something to handle error
            }
        });
    });
});

function getuserbyID(user_id) {
    return $.ajax({
        url: "/getuserbyid",
        type: "post",
        data: { text: user_id },
        success: function(response) {

            return response;

        },
        error: function(xhr) {
            //Do Something to handle error
        }
    });
}

function getReply(post_id) {
    return $.ajax({
        url: "/getreplybyid",
        type: "post",
        data: { text: post_id },
        success: function(response) {

            return response;

        },
        error: function(xhr) {
            //Do Something to handle error
        }
    });
}

function getUsernames() {
    $.ajax({
        url: "/getuser",
        type: "get",
        success: function(response) {

            for (let index = 0; index < Object.keys(response).length; index++) {

                users[index] = {
                    NAME: response[index].name,
                    ID: response[index].id,
                    EMAIL: response[index].email
                }

            }

        },
        error: function(xhr) {
            //Do Something to handle error
        }
    });
}

async function getPosts() {

    $.ajax({
        url: "/posts",
        type: "get",
        success: async function(response) {
            //console.log(response)
            for (let index = 0; index < Object.keys(response).length; index++) {

                try {
                    let postuser = await getuserbyID(response[index].user_id);

                    let postreply = await getReply(response[index].id)


                    for (let jdex = 0; jdex < Object.keys(postreply).length; jdex++) {

                        // console.log(postreply[jdex])

                        var replies_data = {
                            REPLY_TEXT: postreply[jdex].text,
                            REPLY_NAME: postreply[jdex].user_id
                        }

                        replies_data += postreply_template.replace(/\{(.*?)\}/g, function(match, token) {
                            return replies_data[token];
                        });




                    }

                    console.log((replies_data))


                    var data = {
                        TEXT: response[index].text,
                        NAME: postuser[0].name,
                        USER_ID: response[index].user_id,
                        REPLIES: replies_data
                    }

                } catch (error) {
                    console.log('Error:', error);
                }

                replies = {}

                var result = post_template.replace(/\{(.*?)\}/g, function(match, token) {
                    return data[token];
                });

                var rows = htmlToElement(result);
                parent = document.querySelector("#posts");
                parent.appendChild(rows);

            }

        },
        error: function(xhr) {
            //Do Something to handle error
        }
    });

}

//New Post
function htmlToElement(html) {
    var template = document.createElement('template');
    html = html.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;
    return template.content.firstChild;
}

var post_template = `<div class="card post">
                                    <div class="card-body">
                                        <div class="postuserinfo">
                                            <div class="postuserdivimage">
                                                <img src="/static/profile/profile_4.png" class="postuserprofileimg"
                                                    alt="WHEN LOGGED IN IT SHOULD SHOW PROFILE IMAGE">
                                                <h5 id="post_user_id" class="card-title"> {NAME} </h5>
                                            </div>
                                            <div class="postuserdivcontent">
                                                <h6 is="post_date" class="card-subtitle mb-2 text-muted">{USER_ID} </h6>
                                                <p id="post_text" class="card-text">{TEXT}</p>
                                            </div>
                                        </div>
                                        <hr>
                                        <h5 class="card-header"><i class="bi bi-reply"></i> Replies </h5>
                                        {REPLIES}
                                        <div class="postbottombar">
                                            <a href="#" class="btn btn-info"><i class="bi bi-hand-thumbs-up"></i> Like <span
                                                    class="badge badge-secondary">{LIKES}</span> </a>
                                            <a href="#" class="btn btn-info"><i class="bi bi-reply"></i> Reply</a>
                                        </div>
                                    </div>
                                    </div>`

var postreply_template = `<!-- post replies -->
                            <div class="replyuserinfo">
                                <div class="replyuserimagediv">
                                    <img src="/static/profile/profile_7.png" class="postuserprofileimg"
                                        alt="WHEN LOGGED IN IT SHOULD SHOW PROFILE IMAGE">
                                    <h5 class="card-title">{REPLY_NAME}</h5>
                                </div>
                                <div class="replyusercontent">
                                    <h6 class="card-subtitle mb-2 text-muted">Card subtitle</h6>
                                    <p class="card-text">{REPLY_TEXT}</p>
                                </div>
                            </div>
                            <hr>`