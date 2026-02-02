import getCookie from "./getCookie.js";

const csrftoken = getCookie("csrftoken");

/* ================= COMMENTS ================= */

// додати коментар
$(".add-comment").on("click", function () {
    const postId = $(this).data("post-id");
    const input = $(`.comment-input[data-post-id="${postId}"]`);
    const text = input.val();

    if (!text.trim()) return;

    $.ajax({
        url: "/add-comment/",
        method: "POST",
        data: {
            post_id: postId,
            text: text,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (response) {
            $("#comments-list-" + postId).append(`
                <li class="list-group-item" id="comment-${response.id}">
                    ${response.text}
                    <button class="btn btn-sm btn-outline-danger delete-comment" data-id="${response.id}">
                        Delete
                    </button>
                </li>
            `);

            $("#comments-count-" + postId).text(response.comments_count);
            input.val("");
        },
    });
});

// видалити коментар (делегування!)
$(document).on("click", ".delete-comment", function () {
    const commentId = $(this).data("id");

    $.ajax({
        url: `/delete-comment/${commentId}/`,
        method: "POST",
        data: {
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (response) {
            $(`#comment-${commentId}`).remove();
            $("[id^='comments-count-']").text(response.comments_count);
        },
    });
});

/* ================= LIKES ================= */

$(".like-button").on("click", function () {
    const postId = $(this).data("id");

    $.ajax({
        url: `/like/${postId}/`,
        method: "POST",
        data: {
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (response) {
            $("#likes-count-" + postId).text(response.likes);
        },
    });
});

$(".dislike-button").on("click", function () {
    const postId = $(this).data("id");

    $.ajax({
        url: `/dislike/${postId}/`,
        method: "POST",
        data: {
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (response) {
            $("#dislikes-count-" + postId).text(response.dislikes);
        },
    });
});
