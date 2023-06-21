const signUpModal = document.getElementById('signupModal');
const loginModal = document.getElementById('loginModal');


if (signUpModal) {
  signUpModal.addEventListener('show.bs.modal', event => {
    // Button that triggered the modal
    const button = event.relatedTarget
    // Extract info from data-bs-* attributes
    const recipient = button.getAttribute('data-bs-whatever')
    // If necessary, you could initiate an Ajax request here
    // and then do the updating in a callback.

    // Update the modal's content.
    const modalTitle = signUpModal.querySelector('.modal-title')
    const modalBodyInput = signUpModal.querySelector('.modal-body input')

    // modalTitle.textContent = `New message to ${recipient}`
    modalBodyInput.value = recipient
  })
}

if (loginModal) {
  loginModal.addEventListener('show.bs.modal', event => {
    // Button that triggered the modal
    const button = event.relatedTarget
    // Extract info from data-bs-* attributes
    const recipient = button.getAttribute('data-bs-whatever')
    // If necessary, you could initiate an Ajax request here
    // and then do the updating in a callback.

    // Update the modal's content.
    const modalTitle = loginModal.querySelector('.modal-title')
    const modalBodyInput = loginModal.querySelector('.modal-body input')

    // modalTitle.textContent = `New message to ${recipient}`
    modalBodyInput.value = recipient
  })
}
