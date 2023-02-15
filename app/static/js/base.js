$(()=>{
    initTooltip();
    utilityMomentifyDate(".momentify-date");
    utilityClearProgressReportModalOnHide();
    utilityClearFlashModalOnHide();
    utilityOpenFlashModal();
    utilityClearOutgoingItemDeleteModalOnHide();
    utilitySetCopyRightYear();
});

/**
 * Get the today's date
 * @returns String date in the format of yyyy-mm-dd i.e. 1970-12-31
 */
const utilityGetDateToday = () => {
    const dateToday = new Date();
    return dateToday.toISOString().split("T")[0];
}

/**
 * Get this week's start date. Start of the week is Sunday
 * @returns String date in the format of yyyy-mm-dd i.e. 1970-12-31
 */
const utilityGetThisWeekStartDate = () => {
    const dateToday = new Date();
    // Days starts with 0 - Sunday
    weekBegin = new Date().setDate(dateToday.getDate() - dateToday.getDay()) // Gets the epoch time for start of the week base on today's date
    return new Date(weekBegin).toISOString().split("T")[0];
}

/**
 * Get this week's end date
 * @returns String date in the format of yyyy-mm-dd i.e. 1970-12-31
 */
const utilityGetThisWeekEndDate = () => {
    const dateToday = new Date();
    weekEnd = new Date().setDate(dateToday.getDate() + (6 - dateToday.getDay())); // Gets the epoch time for end the week based on today's date
    return new Date(weekEnd).toISOString().split("T")[0];
}

/**
 * Get this month's start date
 * @returns String date in the format of yyyy-mm-dd i.e. 1970-12-31
 */
const utilityGetThisMonthStartDate = () => {
    const dateToday = new Date();
    return new Date(dateToday.getFullYear(), dateToday.getMonth(), 1).toISOString().split("T")[0];
}

/**
 * Get this month's end date
 * @returns String date in the format of yyyy-mm-dd i.e. 1970-12-31
 */
const utilityGetThisMonthEndDate = () => {
    const dateToday = new Date();
    return new Date(dateToday.getFullYear(), dateToday.getMonth()+1, 0).toISOString().split("T")[0];
}

/**
 * Get start of the year date
 * @returns String date in the format of yyyy-mm-dd i.e. 1970-12-31
 */
const utilityGetThisYearStartDate = () => {
    const dateToday = new Date();
    return new Date(dateToday.getFullYear(), 0, 1).toISOString().split("T")[0];
}

/**
 * Get end of the year date
 * @returns String date in the format of yyyy-mm-dd i.e. 1970-12-31
 */
const utilityGetThisYearEndDate = () => {
    const dateToday = new Date();
    // Notice 11 instead of 12, month starts at 0
    return new Date(dateToday.getFullYear(), 11, 31).toISOString().split("T")[0];
}


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

