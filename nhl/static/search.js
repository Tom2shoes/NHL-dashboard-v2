$('#psubmit').click(function(e) {
    e.preventDefault()
    let searchID = $('#psearch').val()
    // console.log(searchID)
    let url = `/searchplayer/${searchID}`
    $.ajax({
        url: url,
        type: "GET"
    }).then(response => {
        $('#playerinfo').append($(`<h1>${response.people[0].fullName}</h1>`))
    })

});
