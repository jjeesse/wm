$(document).ready(function(){
//#button1 = id?
    $('.upvote').click(function(){
    var postid;
    postid = $(this).attr("data-postid");
    update_id = $(this).attr("data-update-id");
     $.get('/upvote/', {post_id: postid,id:update_id}, function(data){ 
               $('#'+update_id).html('<span class="glyphicon glyphicon-bitcoin" aria-hidden="true"></span> Upvotes: '+data);
             
           });
});

    $('.comment_upvote').click(function(){
    var commentid;
    commentid = $(this).attr("data-postid");
    comment_update_id = $(this).attr("data-update-id");
     $.get('/comment_upvote/', {comment_id: commentid,id:comment_update_id}, function(data){ 
               $('#'+comment_update_id).html('<span class="glyphicon glyphicon-bitcoin" aria-hidden="true"></span> Comment Upvotes: '+data);
             
           });
});

    $('.nested_comment_upvote').click(function(){
    var nestedid;
    nestedid = $(this).attr("data-postid");
    nested_update_id = $(this).attr("data-update-id");
     $.get('/nested_comment_upvote/', {nested_id: nestedid,id:nested_update_id}, function(data){ 
               $('#'+nested_update_id).html('<span class="glyphicon glyphicon-bitcoin" aria-hidden="true"></span> Nested Comment Upvotes: '+data);
             
           });
    });

});




