function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i< cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);

            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


console.log(window.location.href)

$(".btn-primary").on('click', function(){
    if (!$(".postInpName").val().trim() || !$(".postInpLast").val().trim()) {
        return alert('Заполните поле')
    }
    let newPost = {
        first_name: $(".postInpName").val(),
        last_name: $(".postInpLast").val()
    }
    let name = $(".postInpName").val()
    let last_name = $(".postInpLast").val()
    console.log(name, last_name)
    postNewPost(newPost)
    console.log($(".postInpName").val())
    $(".postInpName").val('')
    $(".postInpLast").val('')
    $('.obnova').html('')

        $('.obnova').append(`
            <h5>Ваше имя: ${name}</h5>
        `)
    $('.obnova2').html('')
     $('.obnova2').append(`
            <h5>Ваша фамилия: ${last_name}</h5>
        `)
})

function postNewPost(newPost) {
    fetch(`${window.location.href}`, {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify(newPost),
        headers: new Headers({
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
      })

    })

}


//async function render() {
//    console.log('loh')
//    let res = await fetch(`${window.location.href}`)
//    let data = await res.json()
//    $('.obnova').html('')
//    data.forEach(item => {
//        list.append(`
//        <div class = "dynamic-div">
//            <li class="dynamic_post" id=${item.id} style="color: white;">
//                ${item.post} <br><br>
//                <div class="dynamic-img"><img src="${item.image}"/></div>
//                <br><br>
//                <button style="margin-right: 10px" id="${item.likes}" class="btn-dynamic btn-like">Like</button><span style="color: white; font-size" class="likes">${item.likes}</span>
//                <button class="btn-dynamic btn-comment">Comment</button>
//                <button  class="btn-dynamic btn-delete">Delete</button>
//                <button  class="btn-dynamic btn-edit">Edit</button>
//            </li>
//        </div>
//        `)
//    });


