$(()=>{
    utilityClearFlashModalOnHide();
    utilityOpenFlashModal();

    utilitySetCopyRightYear();
});

const utilityOpenFlashModal = () => {
    if($("#flashModalBody").children().length > 0) {
        let flashModal = new bootstrap.Modal(document.getElementById('flashModal'));
        flashModal.show();
    }
}

const utilityClearFlashModalOnHide = () => {
    const modalElem = document.getElementById('flashModal')
    modalElem.addEventListener('hidden.bs.modal', event => {
        $("#flashModalBody").empty();
    })
}

const utilitySetCopyRightYear = () => {
    const dateToday = new Date();
    $(".copy-right-year").text(dateToday.getFullYear());
}