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


function procFetch(data) {
    console.log("Processing", data);
    console.log("Got", typeof (data.data.sentences));
    console.log("TEXT***: ", data.data.text);
    counts = {};
    for (let sentence of data.data.sentences) {
        console.log("Sentence no.", sentence);
        console.log("Sentence length", sentence.tokens.length);
        for (let token of sentence.tokens) {
            let key = token.deprel;
            console.log("Got key", key);
            counts[key] = counts[key] ? counts[key] + 1 : 1;
        }

    }
    let plotdata = [
        {
            x: Object.keys(counts),
            y: Object.values(counts),
            type: 'bar'
        }
    ]
    Plotly.newPlot('plot-bar-1', plotdata);
}

fetch('http://nlp.ailab.lv/api/nlp', {
    method: 'POST', // or 'PUT'
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
})
    .then((response) => response.json())
    .then((data) => {
        console.log("Success: got data of type", typeof (data));
        procFetch(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });

// const fakedata = [
//     {
//         x: ['giraffes', 'orangutans', 'monkeys'],
//         y: [20, 14, 23],
//         type: 'bar'
//     }
// ];

// Plotly.newPlot('plot-bar-1', fakedata);