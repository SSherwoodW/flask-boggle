"use strict";

// class BoggleGame {
//     constructor(boardId, seconds = 60) {
//         this.seconds = seconds; //length of game
//         this.timer = timer;
//         this.score = 0;
//         this.words = [];
//         this.board = $("#" + boardId);
//         this.endTimer();

//         $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
//     }
// }
let score = 0;
$("#score").html("Your score: 0")
let words = [];
let seconds = 60;
$("#timer").html(seconds);

// Handle form submission
$(".add-word").on("submit", showWords, handleSubmit);

async function handleSubmit(evt) {
    // prevent form resubmission and page reload.
    evt.preventDefault();

    let word = $(".word").val();

    if(!word) return;

    const res = await axios.get("/check-word", {params: {word: word}});

    let response = res.data.response;

    showMessage(response, word);
    showWords(response, word);

    $(".add-word").trigger("reset");
}

function showMessage(response, word) {
    // show message on DOM based on if word qualifies. 
    if (response == 'not-on-board') {
        $("#response").html("That word is not on the board!")
    } else if (response == 'ok') {
        if (words.includes(word)) {
            $("#response").html("You already found that word!")
            return;
        }
        words.push(word);
        $("#response").html("Nice find!");
        score += word.length;
        $("#score").html(`Your score: ${score}`)
    } else {
        $("#response").html("That word is not in the dictionary!")
    }
}

let timer = setInterval(function () {
    seconds--;
    $("#timer").html(seconds);
    endTimer();
}, 1000);

function endTimer() {
    // hide form and end the game when timer runs out. 
    if (seconds < 1) {
    clearInterval(timer);
    $(".add-word").hide();
    $("#timer").hide();
    $("#response").html(`Game Over! You Scored ${score} Points!`);
    endGame();
    }
}

function showWords(response, word) {
    // add new words to list on DOM if they count towards user's score.
    if (response == 'ok' ) {
        if (words) {
            $(".words").append($("<li>", {text: word}));
        }
    }
}

async function endGame() {
    //send score to server. 
    await axios.post("/end-game", {score: score});
}

// function startTimer() {
//     if (seconds <= 60 && seconds > 0) {
//         seconds--;
//         $("timer").html(`Time Remaining: ${seconds}`)
//     } else {
//         $("#timer").html("Time's Up!")
//         $(".add-word").remove();
//         $("#response").html(`Game Over! You Scored ${score} points!`);
//         clearInterval(timer);
//     }
// }

// $("document").ready(function() {
//     window.setInterval(function () {
//         startTimer();
//     }, 1000);
// })