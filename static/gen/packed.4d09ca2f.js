function loading(){const data=document.getElementById("data")
if(data!==null){data.style.display='none';}
const spinner=document.getElementById("loadSpinner");spinner.parentElement.style.display='block';spinner.style.display='block';}
(()=>{'use strict'
const forms=document.querySelectorAll('.needs-validation')
Array.from(forms).forEach(form=>{form.addEventListener('submit',event=>{if(!form.checkValidity()){event.preventDefault()
event.stopPropagation()}else{loading();}
form.classList.add('was-validated')},false)})})()