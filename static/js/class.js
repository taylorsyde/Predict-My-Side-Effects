$(document).ready(function() {
    console.log("Page Loaded");

    $("#filter").click(function() {
        // alert("button clicked!");
        $("#pre-cloud").html("");
        $("#cloud").html("");
        $('#result').show();
        makePredictions();
    });
});



function makePredictions() {
    var age_group = $("#age_group").val();
    var sex = $("#sex").val();
    var other_meds = $("#other_meds").val();
    var history = $("#history").val();
    var prior_vax = $("#prior_vax").val();
    var allergies = $("#allergies").val();
    var vax_name = $("#vax_name").val();
    var vax_dose = $("#vax_dose").val();
    // create the payload
    var payload = {
        "age_group": age_group,
        "sex": sex,
        "other_meds": other_meds,
        "history": history,
        "prior_vax": prior_vax,
        "allergies": allergies,
        "vax_name": vax_name,
        "vax_dose": vax_dose
    }

    // console.log("payload", payload)

    // Perform a POST request to the query URL
    $.ajax({
        type: "POST",
        url: "/makePredictions",
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({ "data": payload }),
        success: function(returnedData) {
            // print it
            // console.log(returnedData.prediction);

            var pred = returnedData.prediction
            // var words = returnedData[]
            // console.log(pred)

            var word_pred = returnedData.symptoms
            console.log("class word pred", word_pred)

            $("#output").text(pred);

            sessionStorage.setItem("cur_words", returnedData.symptoms);

            anychart.onDocumentReady(function () {
            
                // create a tag (word) cloud chart
                var chart = anychart.tagCloud(word_pred);

                // set a chart title
                chart.title('People Like You Reported the Following Side-Effects:')
                // set an array of angles at which the words will be laid out
                chart.angles([0, 90])
                // enable a color range
                chart.colorRange(true);
                // set the color range length
                chart.colorRange().length('80%');

                chart.textSpacing(.1)

                chart.tooltip().format("{%yPercentOfTotal}%");

                // display the word cloud chart
                chart.container("cloud");
                chart.draw();

                chart.listen("pointClick", function(e){
                var url = "https://www.merriam-webster.com/dictionary/" + e.point.get("x");
                window.open(url, "_blank");
                });

            });

            
            // console.log(pred)
            // console.log(words)

            // $.each(returnedData.return, function(index, item) { 
            //     console.log("Symptom: " + item["x"]);
            //     console.log("Count: " + item["value"]);
            // })
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("Status: " + textStatus);
            alert("Error: " + errorThrown);
        }

    });

};