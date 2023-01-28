$(()=>{
    initTooltip();
    utilityMomentifyDate(".momentify-date");
    utilityClearProgressReportModalOnHide();
    utilityClearFlashModalOnHide();
    utilityOpenFlashModal();
    utilityClearOutgoingItemDeleteModalOnHide();
    utilitySetCopyRightYear();
});


const utilitySetCopyRightYear = () => {
    const dateToday = new Date();
    $(".copy-right-year").text(dateToday.getFullYear());
}

const initTooltip = () => {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
}

const utilityMakeHeightTheSame = classSelector => {
    var unifiedHeight = 0 // initialize a unified height

    // get each element's height and change unifiedHeight if element's height is bigger
    $(classSelector).each(function(e){
        const elementHeight = $(this).height();
        if(elementHeight > unifiedHeight){
            unifiedHeight = elementHeight;
        }
    });

    // change all element's height
    $(classSelector).each(function(e){
        $(this).height(unifiedHeight);
    });
}


/**
 * Calls ajax post request
 * @param {string} token 
 * @param {string} url 
 * @param {string} contentType 
 * @param {JSON} dataJson 
 * @param {function} successCallback 
 * @param {function} errorCallback 
 */
const utilityAjaxPost = (token, url, contentType, dataJson, successCallback, errorCallback) => {
    
    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", token);
            }
        },
        url: url,
        method: "POST",
        contentType: contentType,
        data: dataJson,
        success: successCallback,
        error: errorCallback
    });
}

/**
 * Calls ajax put request
 * @param {string} token 
 * @param {string} url 
 * @param {string} contentType 
 * @param {JSON} dataJson 
 * @param {function} successCallback 
 * @param {function} errorCallback 
 */
const utilityAjaxPut = (token, url, contentType, dataJson, successCallback, errorCallback) => {
    
    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", token);
            }
        },
        url: url,
        method: "PUT",
        contentType: contentType,
        data: dataJson,
        success: successCallback,
        error: errorCallback
    });
}

/**
 * Calls ajax put request
 * @param {string} token 
 * @param {string} url 
 * @param {string} contentType
 * @param {function} successCallback 
 * @param {function} errorCallback 
 */
const utilityAjaxDelete = (token, url, contentType, successCallback, errorCallback) => {
    
    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", token);
            }
        },
        url: url,
        method: "DELETE",
        contentType: contentType,
        success: successCallback,
        error: errorCallback
    });
}


/**
 * Calls ajax put request
 * @param {string} token 
 * @param {string} url 
 * @param {string} contentType
 * @param {function} successCallback 
 * @param {function} errorCallback 
 */
const utilityAjaxGet = (token, url, contentType, successCallback, errorCallback) => {
    
    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", token);
            }
        },
        url: url,
        method: "GET",
        contentType: contentType,
        success: successCallback,
        error: errorCallback
    });
}


const utilityMomentifyDate = elemSelector => {
    $(elemSelector).each(function(e){
        // const value = $(this).data("value");
        const value = $(this).text();
        console.log();
        if(value){
            $(this).text(moment(new Date(value)).format('ll'));
        }
    });
}


const utilityOpenProgressReportModal = () => {
    let progressReportModal = new bootstrap.Modal(document.getElementById('progressReportModal'));
    progressReportModal.show();
}

const utilityClearProgressReportModalOnHide = () => {
    const modalElem = document.getElementById('progressReportModal')
    modalElem.addEventListener('hidden.bs.modal', event => {
        $("#progressReportModalBody").empty();
    })
}

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


const utilityClearOutgoingItemDeleteModalOnHide = () => {
    const modalElem = document.getElementById('outgoingDeleteModal')
    modalElem.addEventListener('hidden.bs.modal', event => {
        $("#outgoingDeleteModalBodyH5").text("");
        $("#outgoingDeleteModalBodyP").text("");
        $("#outgoingDeleteModalBtn").data("url", "");
        $("#outgoingDeleteModalBtn").data("csrf", "");
        $("#outgoingDeleteModalBtn").html("Yes, Delete It");
        $(".outgoing-delete-modal-btns").each(function(){
            $(this).prop("disabled", false);
        });
    })
}

