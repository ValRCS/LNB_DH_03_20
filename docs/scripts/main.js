// https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
// const data = { username: 'example' };

// sample data from nlp.ailab.lv korpusa

const data = {
    data: {
        text: `Veikals "Lidl" oficiāli apstiprinājis ienākšanu Latvijā, pērk zemesgabalus un meklē darbiniekus, taču konkrētus plānus glabā lielā slepenībā. Portāls "Delfi" noskaidroja, ka līdztekus vairākiem veikaliem Rīgā "Lidl" noskatījis arī Liepāju un Jūrmalu.`
    },
    steps: ["tokenizer", "morpho", "parser", "ner"],
    model: "default",
    config: null
};


fetch('http://nlp.ailab.lv/api/nlp', {
    method: 'POST', // or 'PUT'
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
})
    .then((response) => response.json())
    .then((data) => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });