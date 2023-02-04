function loading() {
    const data = document.getElementById("data")
    if(data !== null){
      data.style.display = 'none';
    }
    const spinner = document.getElementById("loadSpinner");
    spinner.parentElement.style.display = 'block';
    spinner.style.display = 'block';
}

// Example starter JavaScript for disabling form submissions if there are invalid fields
(() => {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
      form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        } else {
          loading();
        }
  
        form.classList.add('was-validated')
      }, false)
    })
  })()