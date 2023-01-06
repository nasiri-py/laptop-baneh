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
    colorBtn[i].addEventListener("click", function () {
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


$(function () {
    $('[data-bs-toggle="tooltip"]').tooltip();
});


const productImageWap = document.getElementsByClassName('a-wap')
const productImage = document.getElementById('product-detail')
for (let i = 0; i < productImageWap.length; i++) {
    productImageWap[i].addEventListener("click", function () {
        const this_src = $(this).children('img').attr('src');
        productImage.setAttribute('src', this_src);
        productImage.setAttribute('data-origin', this_src);
    })
}


$('.btn-color input').click(function () {
    const this_num = $(this).attr('size');
    $('#product-quantity').attr('max', this_num);
});

function getPics() {}
const imgZoom = document.getElementById('product-detail');
const fullPage = document.getElementById('fullpage');
const fullImg = document.getElementById('full-image')
imgZoom.addEventListener('click', function () {
    fullImg.style.backgroundImage = 'url(' + imgZoom.src + ')';
    fullPage.style.display = 'block';
});
