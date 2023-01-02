// Set the date we're counting down to
var countDownDate = new Date
countDownDate.setMinutes(countDownDate.getMinutes() + 3);

// Update the count down every 1 second
var x = setInterval(function () {

    // Get today's date and time
    var now = new Date().getTime();

    // Find the distance between now and the count down date
    var distance = countDownDate - now;

    // Time calculations for days, hours, minutes and seconds
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // Output the result in an element with id="demo"
    document.getElementById("resend-code").innerHTML = `<p>${seconds} : ${minutes}  مانده تا دریافت مجدد کد</p>`

    // If the count down is over, write some text
    if (distance < 0) {
        clearInterval(x);
        document.getElementById("resend-code").innerHTML = `<form action="{% url 'accounts:resend-code' %}" method="POST">
                                                                        {% csrf_token %}
                                                                        <input class="login-register-link bg-transparent border-0" type="submit"
                                                                        name="access" value='ارسال مجدد کد'>
                                                                    </form>`
    }
}, 1000);



const VerifyInput = document.getElementById('verify-input')
const VerifyButton = document.getElementById('verify-button')
const codeBox = document.getElementById('code-box')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const sendCode = (code) => {
    $.ajax({
        type: 'POST',
        url: "{% url 'accounts:verify-check' %}",
        data: {
            'csrfmiddlewaretoken': csrf,
            'code': code,
        },
        success: (res) => {
            const data = res.data
            if (data === 'TrueAccess') {
                codeBox.classList.add('d-none')
                if (VerifyButton.classList.contains('d-none')) {
                    VerifyButton.classList.remove('d-none')
                }
            } else {
                VerifyButton.classList.add('d-none')
                if (VerifyInput.value.length > 0) {
                    codeBox.innerHTML = `<p class="text-center w-100 border-0 m-auto mt-4">${data}</p>`
                } else {
                    codeBox.classList.add('d-none')
                }
            }
        },
        error: (err) => {
            console.log(err)
        }
    })
}
VerifyInput.addEventListener('keyup', e => {
    if (codeBox.classList.contains('d-none')) {
        codeBox.classList.remove('d-none')
    }
    sendCode(e.target.value)
})