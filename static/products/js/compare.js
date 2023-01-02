
const comSearchInput = document.getElementById('compare-search-input')
const comResultsBox = document.getElementById('compare-results-box')
const sendCompareSearchData = (product) => {
    $.ajax({
        type: 'GET',
        url: "{% url 'product:compare-search' %}",
        data: {
            'com_product': product,
        },
        success: (res) => {
            const data = res.data
            if (Array.isArray(data)) {
                comResultsBox.innerHTML = ""
                data.forEach(product => {
                    comResultsBox.innerHTML += `<li class="list-group-item border-0">
                <a class="row text-dark text-decoration-none" href="add/${product.id}">
                    <img class="col-2" src="${product.cover}" alt="${product.title}">
                    <h6 class="col-10 my-auto">${product.title}</h6>
                </a>
            </li>
            <hr class="mt-0"/>`
                })
            } else {
                if (comSearchInput.value.length > 0) {
                    comResultsBox.innerHTML = `<h6 class="text-center my-auto py-5">${data}</h6>`
                } else {
                    comResultsBox.classList.add('d-none')
                }
            }
        },
        error: (err) => {
            console.log(err)
        }
    })
}
comSearchInput.addEventListener('keyup', e => {
    if (comResultsBox.classList.contains('d-none')) {
        comResultsBox.classList.remove('d-none')
    }
    sendCompareSearchData(e.target.value)
})