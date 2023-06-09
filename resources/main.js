const onSubmit = (event) => {
    event.preventDefault()

    document.querySelector('.form_wrapper').classList.remove('error')

    let i = 0;

    const target = event.target;

    let fields = {}

    while (target[i] != null) {
        const current = target[i]
        const name = current.name

        if (name.length === 0) {
            i++
            continue
        }

        if (name === 'request') {
            if (current.checked)
                fields[current.name] = current.labels[0].innerText

            i++
            continue
        }

        fields[current.name] = current.value
        i++
    }

    if (fields.url.length === 0 || fields.request == null) {
        formNotValid()
        return false
    }

    if (fields.port.length === 0) {
        fields.port = 80
    }

    if (fields.timeout.length === 0) {
        fields.timeout = null
    }
    else
        fields.timeout = Number(fields.timeout)
    fields.headers = parse(fields.headers)
    fields.cookie = parse(fields.cookie)

    const body = JSON.stringify(fields)

    fetch('http://127.0.0.1:8080/', {
        method: 'post',
        headers: {
            'content-type': 'application/json'
        },
        body: body
    })
        .then(response => response.text())
        .then(data => {
            const result_text = document.querySelector('.result__text');
            result_text.textContent = data;

            const result = document.querySelector('.result');

            if (!result.classList.contains('result-active')) {
                result.classList.add('result-active')
            }
        }
    );

    return true
}

const formNotValid = () => {
    document.querySelector('.form_wrapper').classList.add('error')
}

const parse = (headers) => {
    if (headers.length === 0) {
        return {}
    }

    let response = []

    let key = ''
    let value = ''
    let isKey = true

    for (let i = 0; i < headers.length; i++) {
        const currentChar = headers[i]

        if (currentChar === ';') {
            response[key] = value

            key = ''
            value = ''
            isKey = true
        }

        if (currentChar === ':') {
            isKey = false
            continue
        }

        if ((i - 1) >= 0 && currentChar === ' ' && headers[i - 1] === ':')
            continue

        if (isKey) {
            key += currentChar
            continue
        }

        value += currentChar
    }

    return response.length === 0 ? {} : response
}

window.addEventListener('load', () => {
    document.querySelector('.form').addEventListener('submit', onSubmit)
})