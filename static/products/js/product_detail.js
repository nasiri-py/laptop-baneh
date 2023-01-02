const one_star = document.getElementById('1star')
const two_star = document.getElementById('2star')
const three_star = document.getElementById('3star')
const four_star = document.getElementById('4star')
const five_star = document.getElementById('5star')

const handleSelect = (selection) => {
    switch (selection) {
        case '1star': {
            one_star.classList.add('text-warning')
            two_star.classList.remove('text-warning')
            three_star.classList.remove('text-warning')
            four_star.classList.remove('text-warning')
            five_star.classList.remove('text-warning')
            return
        }
        case '2star': {
            one_star.classList.add('text-warning')
            two_star.classList.add('text-warning')
            three_star.classList.remove('text-warning')
            four_star.classList.remove('text-warning')
            five_star.classList.remove('text-warning')
            return
        }
        case '3star': {
            one_star.classList.add('text-warning')
            two_star.classList.add('text-warning')
            three_star.classList.add('text-warning')
            four_star.classList.remove('text-warning')
            five_star.classList.remove('text-warning')
            return
        }
        case '4star': {
            one_star.classList.add('text-warning')
            two_star.classList.add('text-warning')
            three_star.classList.add('text-warning')
            four_star.classList.add('text-warning')
            five_star.classList.remove('text-warning')
            return
        }
        case '5star': {
            one_star.classList.add('text-warning')
            two_star.classList.add('text-warning')
            three_star.classList.add('text-warning')
            four_star.classList.add('text-warning')
            five_star.classList.add('text-warning')
            return
        }
    }
}
const handleUnSelect = (unselection) => {
    switch (unselection) {
        case '1star': {
            one_star.classList.remove('text-warning')
            two_star.classList.remove('text-warning')
            three_star.classList.remove('text-warning')
            four_star.classList.remove('text-warning')
            five_star.classList.remove('text-warning')
            return
        }
        case '2star': {
            one_star.classList.remove('text-warning')
            two_star.classList.remove('text-warning')
            three_star.classList.remove('text-warning')
            four_star.classList.remove('text-warning')
            five_star.classList.remove('text-warning')
            return
        }
        case '3star': {
            one_star.classList.remove('text-warning')
            two_star.classList.remove('text-warning')
            three_star.classList.remove('text-warning')
            four_star.classList.remove('text-warning')
            five_star.classList.remove('text-warning')
            return
        }
        case '4star': {
            one_star.classList.remove('text-warning')
            two_star.classList.remove('text-warning')
            three_star.classList.remove('text-warning')
            four_star.classList.remove('text-warning')
            five_star.classList.remove('text-warning')
            return
        }
        case '5star': {
            one_star.classList.remove('text-warning')
            two_star.classList.remove('text-warning')
            three_star.classList.remove('text-warning')
            four_star.classList.remove('text-warning')
            five_star.classList.remove('text-warning')
            return
        }
    }
}
const arr = [one_star, two_star, three_star, four_star, five_star]
arr.forEach(item => item.addEventListener('mouseover', (event) => {
    handleSelect(event.target.id)
}))
arr.forEach(item => item.addEventListener('mouseleave', (event) => {
    handleUnSelect(event.target.id)
}))


const colorBtn = document.getElementsByClassName('btn-color')
for (let i = 0; i < colorBtn.length; i++) {
    colorBtn[i].addEventListener("mouseup", function () {
        const current = document.getElementsByClassName("color-select");
        current[0].className = current[0].className.replace(" color-select", "");
        this.className += " color-select";
    });
}

$(function () {
    $(".comment").slice(0, 4).show();
    $("#loadMoreComment").on('click', function (e) {
        e.preventDefault();
        $(".comment:hidden").slice(0, 4).slideDown();
        if ($(".comment:hidden").length == 0) {
            $("#loadLessComment").fadeIn('slow');
            $("#loadMoreComment").hide();
            // $("#loadMore").text('Load only the first 4');
        }
        $('.review-content').animate({
            scrollTop: $(this).offset().top
        }, 1500);
    });

    $("#loadLessComment").on('click', function (e) {
        e.preventDefault();
        $('.comment:not(:lt(4))').fadeOut();
        $("#loadMoreComment").fadeIn('slow');
        $("#loadLessComment").hide();

        desiredHeight = $(window).height();

        $('.review-content').animate({
            scrollTop: $(this).offset().top + desiredHeight
        }, 1500);
    });

});


const imageZoom = document.getElementsByClassName('imgBox')
const mediaQuery = window.matchMedia('(max-width: 992px)')
if (mediaQuery.matches) {
    imageZoom.classList.remove('imgBox')
}


$(function () {
    $('[data-bs-toggle="tooltip"]').tooltip();
});


$('.product-links-wap a').click(function () {
    const this_src = $(this).children('img').attr('src');
    $('#product-detail').attr('src', this_src);
    $('#product-detail').attr('data-origin', this_src);
    return false;
});

$('.btn-color input').click(function () {
    const this_num = $(this).attr('size');
    $('#product-quantity').attr('max', this_num);
});