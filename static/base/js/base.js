
const searchInput = document.getElementById('search-input')
const searchButton = document.getElementById('search-button')
const resultsBox = document.getElementById('results-box')
const sendSearchData = (product) => {
    $.ajax({
        type: 'GET',
        url: "{% url 'product:search' %}",
        data: {
            'product': product,
        },
        success: (res) => {
            const data = res.data
            if (Array.isArray(data)) {
                resultsBox.innerHTML = ""
                searchButton.classList.remove('d-none')
                data.forEach(product => {
                    resultsBox.innerHTML += `<li class="list-group-item border-0">
                <a class="row text-dark text-decoration-none" href="{% url 'product:list' %}detail/${product.slug}">
                    <img class="col-2" src="${product.cover}" alt="${product.title}">
                    <h6 class="col-8 my-auto">${product.title}</h6>
                </a>
            </li>
            <hr class="mt-0"/>`
                })
            } else {
                if (searchInput.value.length > 0) {
                    resultsBox.innerHTML = `<h6 class="text-center my-auto py-5">${data}</h6>`
                    if (data === 'محصول موردنظر یافت نشد ...') {
                        searchButton.classList.add('d-none')
                    }
                } else {
                    searchButton.classList.add('d-none')
                    resultsBox.classList.add('d-none')
                }
            }
        },
        error: (err) => {
            console.log(err)
        }
    })
}
searchInput.addEventListener('keyup', e => {
    if (resultsBox.classList.contains('d-none')) {
        resultsBox.classList.remove('d-none')
    }
    sendSearchData(e.target.value)
})