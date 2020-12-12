var startResults = 5;
var numResults = startResults;
var incResults = 5;

var selected_loc_filters = []
var selected_uni_filters = []
var searchTerm = ''

function setCookie(cname, cvalue) {
    document.cookie = cname + "=" + cvalue + ";";
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}


var docDiv = (doc) => {
    const name = doc[0];
    const prev = doc[1];
    const email = doc[2];
    const uni_dept = doc[4] + ', ' + doc[3]
    const fac_name = doc[5]
    const fac_url = doc[6]
    const loc = doc[7] + ', ' + doc[8]
    const phone = doc[9]
    const interests = doc[10]

    let result = ``;
    result = result + `
    <div class="card">
       <div class="card-header">
         <div style="display: flex;">
           <b style="font-size:14pt">${fac_name}</b>`

    let iconBar = `<div style="margin-left: auto;">`;
    if (email != 'None') {
        iconBar += `
           <a style="margin-left:auto;color:black;margin-right:20px;" href='mailto:${email}' "><i class="material-icons">email</i></a>`
    }
    if (phone != 'None') {
        iconBar += `
           <a style="margin-left:auto;color:black;margin-right:20px;" href='tel:${phone}' "><i class="material-icons">phone</i></a>`
    }
    iconBar += `<a style="color:black;" href=${fac_url} target="_blank"><i class="material-icons">launch</i></a>`
    iconBar += `</div>`
    result += iconBar

    result += `
         </div>
         <div class="header-item" style="flex-direction: column;">
            <div class="tag">
            <i class='fas fa-university' ></i>
                  ${uni_dept}
            </div>
            <div class="tag">
            <i class="material-icons">location_on</i>
                  ${loc}
            </div>
            <div class="tag">
            <i class="material-icons">label</i>
                  ${interests}
            </div>
         </div>
    </div>
    <div class="card-body">
        <span id='docPrev-${name}'>${prev}</span>
        <br>
    </div>
    </div>`
    return (result);
}

var doSearch = function() {
    const data = {
        "query": searchTerm,
        "num_results": numResults,
        "selected_loc_filters": selected_loc_filters,
        "selected_uni_filters": selected_uni_filters
    }
    if (searchTerm != '') {
        let newCookie = null;
        var originalCookie = getCookie("history");
        if (originalCookie === "") {
            newCookie = searchTerm;
        } else {
            newCookie = originalCookie + "," + searchTerm;
        }
        console.log("setting new cookie");
        console.log(newCookie);
        setCookie("history", newCookie)

        var num_fetched_res = 0
        fetch("http://localhost:8095/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)
        }).then(response => {
            response.json().then(data => {
                const docs = data.docs;
                $("#docs-div").empty();

                docs.forEach(doc => {
                    $("#docs-div").append(
                        docDiv(doc)
                    );
                    num_fetched_res = num_fetched_res + 1;
                });

                if (num_fetched_res === numResults) {
                    $("#loadMoreButton").css("display", "block")
                } else {
                    $("#loadMoreButton").css("display", "none")
                }
                if (num_fetched_res === 0) {
                    $("#docs-div").append(`<h3 style="text-align: center;margin-top:20px;">No Search Results Found</h3>`);
                }
            })
        });
    }
}

$(window).on("resize", function() {
    $(document.body).css("margin-top", $(".navbar").height() + 5);
    var width = $(".select2-container").width()
    if ((width == 0) || width === undefined) {
        width = 300
    }
    $(".select2-search__field").css('cssText', $(".select2-search__field").attr('style') + 'width: ' + width + 'px !IMPORTANT;');
}).resize();


$(document).ready(function() {
    $('#loc_filter').select2({
        placeholder: "e.g. United States, California"
    });
    $('#uni_filter').select2({
        placeholder: "e.g. Stanford University"
    });
    $(window).trigger('resize');
});

window.onload = async function() {
    for (var i = 0; i < unis.length; i++) {
        var newOption = new Option(unis[i], i, false, false);
        // Append it to the select
        $('#uni_filter').append(newOption).trigger('change');


    }
    selected_uni_filters = unis.slice()
    for (var i = 0; i < locs.length; i++) {
        var newOption = new Option(locs[i], i, false, false);
        // Append it to the select
        $('#loc_filter').append(newOption).trigger('change');
    }
    selected_loc_filters = locs.slice()
    $(window).trigger('resize');

    let history = getCookie("history");
    if (history === "") {
        return;
    }
    let splitList = history.split(",", 5);
    let pastSearches = splitList.reverse();
    console.log("search history");
    console.log(pastSearches);
    $("#docs-div").empty();
    if (pastSearches.length <= 0) {
        return;
    }

    $("#docs-div").append(`<h2 style="font-style: italic; font-size: 23px;">Recommended experts based on your search history...</h2>`);

    for (var i = 0; i < pastSearches.length; i++) {
        var keyword = pastSearches[i];
        $("#docs-div").append(`<h3 style="font-size: 20px;color: #3D9970; font-family: monospace; margin-top: 20px;">search keyword: ${keyword}</h3>`);

        const data = {
            "query": keyword,
            "num_results": 5,
            "selected_loc_filters": selected_loc_filters,
            "selected_uni_filters": selected_uni_filters
        }
        var num_fetched_res = 0
        const response = await fetch("http://localhost:8095/recommend", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)
        });
        const responseJson = await response.json();
        const docs = responseJson.docs;
        docs.forEach(doc => {
            $("#docs-div").append(
                docDiv(doc)
            );
            num_fetched_res = num_fetched_res + 1;
        });
    }
};

function toggleFilter() {
    filters_div = document.getElementById("search-filters")
    filters_div.style.display = filters_div.style.display === 'none' ? 'flex' : 'none';
}

$("#submitButton").click(function() {
    numResults = startResults;
    searchTerm = $('#query').val()
    doSearch();
});

$("#filterButton").click(function() {
    toggleFilter();
});

$('#query').keydown(function(e) {
    searchTerm = $('#query').val()
    if (e.keyCode == 13) {
        numResults = startResults;

        doSearch();
    }
});

$("#applyFilters").click(function() {

    var selected_uni_data = $("#uni_filter").select2("data");
    selected_uni_filters = []
    selected_uni_data.forEach(s => {
        selected_uni_filters.push(s['text']);

    });

    if (selected_uni_filters.length == 0) {
        selected_uni_filters = unis.slice()
    }

    var selected_loc_data = $("#loc_filter").select2("data");
    selected_loc_filters = []
    selected_loc_data.forEach(s => {
        selected_loc_filters.push(s['text']);

    });

    if (selected_loc_filters.length == 0) {
        selected_loc_filters = locs.slice()
    }
    filters_div = document.getElementById("search-filters")
    filters_div.style.display = 'none'
    doSearch();
});

$("#settingsButton").click(function() {
    window.location = "http://localhost:8095/admin"
});

$("#loadMoreButton").click(function() {
    numResults += incResults

    doSearch();
});