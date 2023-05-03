const onSubmit = (event) => {
    event.preventDefault()

    document.querySelector('.form_wrapper').classList.remove('error')

    let i = 0;

    const target = event.target;

    const fields = {}

    while (target[i] != null) {
        const current = target[i]
        const name = current.name

        if (name.length === 0) {
            i++
            continue
        }

        if (name === 'request') {
            if (current.checked) {
                fields[current.name] = {
                    'value': current.value,
                    'classes': current.classList,
                    'target': current
                }
            }

            i++
            continue
        }

        fields[current.name] = current.value
        i++
    }

    if (fields.url.length === 0 || fields.port.length === 0 || fields.request == null) {
        formNotValid()
        return false
    }

    fetch('http://127.0.0.1:80/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(fields)
    }).then(response => response.then(body => console.log(body)))

    return true
}

const formNotValid = () => {
    document.querySelector('.form_wrapper').classList.add('error')
}

window.addEventListener('load', () => {
    document.querySelector('.form').addEventListener('submit', onSubmit)
})