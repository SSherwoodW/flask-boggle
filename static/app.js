

async function handleSubmit(evt) {
    evt.preventDefault();

    let word = $(".add-word").val();

    if(!word) return;

    const res = await axios.post("/check-word", {params: {word: word}});

    console.log(res);
}

$(".word").on("submit", handleSubmit);