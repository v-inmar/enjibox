$(()=>{
    utilityMakeHeightTheSame(".outgoing-reads-item-list-a");

    outgoingClearTime();
    outgoingOpenNewOptionModal();
    outgoingClearNewOptionModalOnHide();
    outgoingSaveNewOption();
    outgoingSaveItem("post",'#outgoingNewItemForm', outgoingSaveNewItemSuccessCallback, outgoingSaveNewItemErrorCallback);
    outgoingSaveItem("put", "#outgoingUpdateItemForm", outgoingSaveUpdateSuccessCallback, outgoingSaveUpdateErrorCallback);

    outgoingDeleteItemOpenModal();
    outgoingDeleteItem();

    outgoingFilterSubmit();

    outgoingPopulatePresetAnchors();
});

/**
 * Set the urls for the presets
 */
const outgoingPopulatePresetAnchors = () => {
    var urlPrefix = $(".outgoing-read-preset-a").attr("href");
    const pageNumber = 1;

    // Set Today link
    const dateTodayISONoTime = utilityGetDateToday();
    $(".outgoing-read-preset-a-today").attr("href",urlPrefix+"?label=&date_from="+dateTodayISONoTime+"&date_to="+dateTodayISONoTime+"&category=&form=&page="+pageNumber);

    // Set Dates for Week start and Week end
    const dateThisWeekStartISONoTime = utilityGetThisWeekStartDate();
    const dateThisWeekEndISONoTime = utilityGetThisWeekEndDate();
    $(".outgoing-read-preset-a-this-week").attr("href",urlPrefix+"?label=&date_from="+dateThisWeekStartISONoTime+"&date_to="+dateThisWeekEndISONoTime+"&category=&form=&page="+pageNumber);

    // Set Dates for the month start and month end
    const dateThisMonthStartISONoTime = utilityGetThisMonthStartDate();
    const dateThisMonthEndISONoTime = utilityGetThisMonthEndDate();
    $(".outgoing-read-preset-a-this-month").attr("href",urlPrefix+"?label=&date_from="+dateThisMonthStartISONoTime+"&date_to="+dateThisMonthEndISONoTime+"&category=&form=&page="+pageNumber);


    // Set Dates for the year start and year end
    const dateThisYearStartISONoTime = utilityGetThisYearStartDate();
    const dateThisYearEndISONoTime = utilityGetThisYearEndDate();
    $(".outgoing-read-preset-a-this-year").attr("href",urlPrefix+"?label=&date_from="+dateThisYearStartISONoTime+"&date_to="+dateThisYearEndISONoTime+"&category=&form=&page="+pageNumber);


}




const outgoingFilterSubmit = () => {
    $("#outgoingFilterFormElement").on("submit", function(e){
        e.preventDefault();

        $("#outgoingSubmitBtnFilter").prop("disabled", true);
        var urlPrefix = $(this).data("urlprefix");
        const label = $("#outgoingLabelFilter").val();
        const category = $("#outgoingCategoryFilter").val();
        const form = $("#outgoingFormFilter").val();
        const dateTo = $("#outgoingDateToFilter").val();
        const dateFrom = $("#outgoingDateFromFilter").val();

        urlPrefix += "?"
        urlPrefix += "label="+label;
        urlPrefix += "&date_from="+dateFrom;
        urlPrefix += "&date_to="+dateTo;
        urlPrefix += "&category="+category;
        urlPrefix += "&form="+form;
        urlPrefix += "&page=1"

        window.location.href = urlPrefix
    });
}


const outgoingDeleteItemOpenModal = () => {
    $("#outgoingItemDeleteLink").on("click", function(e){
        e.preventDefault();
        $("#outgoingDeleteModalBodyP").text($("#outgoingLabelItem").text());
        $("#outgoingDeleteModalBtn").data("url", $(this).data("url"));
        $("#outgoingDeleteModalBtn").data("csrf", $(this).data("csrf"));
        let deleteItemModal = new bootstrap.Modal(document.getElementById('outgoingDeleteModal'), {backdrop:'static'});
        deleteItemModal.show();
    });
}

const outgoingDeleteItem = () => {
    $("#outgoingDeleteModalBtn").on("click", function(e){
        let url = $(this).data("url");
        let csrf = $(this).data("csrf");
        $(this).html(`
        Deleting...
        <div class="spinner-border spinner-border-sm" role="status">
            <span class="visually-hidden">Saving...</span>
        </div>
        `);

        $(".outgoing-delete-modal-btns").each(function(){
            $(this).prop("disabled", "true");
        });
        utilityAjaxDelete(
            token=csrf,
            url=url,
            contentType="application/json",
            successCallback=outgoingDeleteSuccessCallback,
            errorCallback=outgoingDeleteErrorCallback
        )
    });
}

const outgoingDeleteSuccessCallback = data => {
    window.location.replace(data.payload.url);
}

const outgoingDeleteErrorCallback = (jqXHR, textStatus, errorThrown) => {
    $("#outgoingDeleteModalBodyH5").text(jqXHR.status+": "+ jqXHR.responseJSON.msg);
    $("#outgoingDeleteModalBtn").html("Yes, Delete It");
    $(".outgoing-delete-modal-btns").each(function(){
        $(this).prop("disabled", false);
    });
}


const outgoingDisableAllFormElements = (formElemSelector) => {
    $(formElemSelector).find('*').attr('disabled', true);
}

const outgoingEnableAllFormElements = (formElemSelector) => {
    $(formElemSelector).find('*').attr('disabled', false);
}


const outgoingSaveItem = (requestMethod, formElemSelector, successCallback, errorCallback) => {
    $(formElemSelector).on("submit", function(e){
        e.preventDefault();
        let label = $("#outgoingLabelInput").val();
        let amount = $("#outgoingAmountInput").val();
        let category = $("#outgoingCategorySelect").val();
        let form = $("#outgoingFormSelect").val();
        let date = $("#outgoingDateInput").val(); // format from input is yyyy-mm-dd
        let time = $("#outgoingTimeInput").val();
        let comment = $("#outgoingCommentTextarea").val();

        var offset = false;
        if($("#outgoingOffsetCheckbox").is(":checked")){
            offset = true;
        }

        data = {
            "label":label,
            "amount":amount,
            "date":date,
            "category":category,
            "form":form,
            "time":time,
            "comment":comment,
            "offset":offset
        }
        $("#outgoingSaveBtn").html(`
        Saving...
        <div class="spinner-border spinner-border-sm" role="status">
            <span class="visually-hidden">Saving...</span>
        </div>
        `);
        outgoingDisableAllFormElements(formElemSelector);

        if(requestMethod === "post"){
            utilityAjaxPost(
                token=$("#outgoingCSRFTokenInput").val(),
                url=$(this).attr('action'),
                contentType="application/json",
                dataJson=JSON.stringify(data),
                successCallback = successCallback,
                errorCallback = errorCallback
            );
        }else{
            utilityAjaxPut(
                token=$("#outgoingCSRFTokenInput").val(),
                url=$(this).attr('action'),
                contentType="application/json",
                dataJson=JSON.stringify(data),
                successCallback = successCallback,
                errorCallback = errorCallback
            );
        }
        

    });
    
}

const outgoingSaveUpdateSuccessCallback = data => {
    window.location.replace(data.payload.url);
}

const outgoingSaveUpdateErrorCallback = (jqXHR, textStatus, errorThrown) => {
    $("#outgoingSaveBtn").html("Save");
    outgoingEnableAllFormElements('#outgoingUpdateItemForm');

    $("#progressReportModalBody").append(`
        <p class="text-danger">${jqXHR.status}: ${errorThrown} ${jqXHR.responseJSON.msg}</p>
    `);
    utilityOpenProgressReportModal();
}

const outgoingSaveNewItemSuccessCallback = data => {
    $("#progressReportModalBody").append(`
        <p class="text-light">Saved!</p>
    `);
    utilityOpenProgressReportModal();



    $("#outgoingSaveBtn").html("Save");
    outgoingEnableAllFormElements('#outgoingNewItemForm');

    // remove any active class
    $(".list-group-item").each(function(){
        $(this).removeClass("active");
    });

    // prepend the new item
    $("#outgoingNewItemAddedListDiv").prepend(outgoingNewItemTemplate(data.payload));
    
    // Make the element flash to grab attention
    $("#"+data.payload.pid).fadeOut(300).fadeIn(300).fadeOut(300).fadeIn(300).fadeOut(300).fadeIn(300).fadeOut(300).fadeIn(300);

    // increase the count of items
    var currentCount = parseInt($(".outgoing-new-item-added-count").text());
    $(".outgoing-new-item-added-count").text(currentCount+1);

    // Reset the elements
    outgoingSaveNewItemResetElements();
}

const outgoingSaveNewItemErrorCallback = (jqXHR, textStatus, errorThrown) => {
    $("#outgoingSaveBtn").html("Save");
    outgoingEnableAllFormElements('#outgoingNewItemForm');

    $("#progressReportModalBody").append(`
        <p class="text-danger">${jqXHR.status}: ${errorThrown} ${jqXHR.responseJSON.msg}</p>
    `);
    utilityOpenProgressReportModal();
}

const outgoingSaveNewItemResetElements = () => {
    $("#outgoingLabelInput").val("");
    $("#outgoingAmountInput").val("");
    $("#outgoingCategorySelect").val("");
    $("#outgoingFormSelect").val("");
    $("#outgoingDateInput").val(""); // format from input is yyyy-mm-dd
    $("#outgoingTimeInput").val("");
    $("#outgoingCommentTextarea").val("");
    $("#outgoingOffsetCheckbox").prop("checked", false);
}


const outgoingClearTime = () => {
    $(".outgoing-clear-time").on("click", function(e){
        e.preventDefault();

        $('#outgoingTimeInput').val("");
    });
}


const outgoingClearNewOptionModalOnHide = () => {
    const myModalEl = document.getElementById('outgoingNewOptionModal')
    myModalEl.addEventListener('hidden.bs.modal', event => {
        $("#outgoingNewOptionModalError").text("");
        $("#outgoingNewOptionModalHeader").text("");
        $("#outgoingNewOptionModalLabel").text("");
        $("#outgoingNewOptionModalInput").attr("maxlength", "");
        $("#outgoingNewOptionModalInput").val("");
        $("#outgoingNewOptionModalSubmitBtn").data("topic", "");
    })

}

const outgoingOpenNewOptionModal = () => {
    $(".outgoing-new-option").on("click", function(e){
        e.preventDefault();
        

        $("#outgoingNewOptionModalHeader").text($(this).data("title"));
        $("#outgoingNewOptionModalLabel").text($(this).data("label"));
        $("#outgoingNewOptionModalInput").attr("maxlength", $(this).data("maxlength"));
        $("#outgoingNewOptionModalSubmitBtn").data("topic", $(this).data("label"));
        

        let outgoingNewOptionModal = new bootstrap.Modal(document.getElementById('outgoingNewOptionModal'));
        outgoingNewOptionModal.show();
    });
}

const outgoingSaveNewOption = () => {
    $("#outgoingNewOptionModalFormElement").on("submit", function(e){
        e.preventDefault();
        
        // Clear
        $("#outgoingNewOptionModalError").text("");

        let topic = $("#outgoingNewOptionModalSubmitBtn").data("topic");
        var currentOptions = [];
        var classOption = "";
        var idSelect = "";
        if(topic == "Category"){
            classOption = "outgoing-category-option";
            idSelect = "outgoingCategorySelect"
        }else{
            classOption = "outgoing-form-option";
            idSelect = "outgoingFormSelect"
        }

        $("."+classOption).each(function(){
            let optionValue = $(this).val();
            if(!currentOptions.includes(optionValue)){
                currentOptions.push(optionValue);
            }
        });

        let newValue = $("#outgoingNewOptionModalInput").val();

        if(currentOptions.includes(newValue)){
            $("#outgoingNewOptionModalError").text("Already in the list");
        }else{
            $("#"+idSelect).append(`
                <option value="${newValue}" class="${classOption}" selected>${newValue}</option>
            `);

            var myModalEl = document.getElementById('outgoingNewOptionModal');
            var modal = bootstrap.Modal.getInstance(myModalEl)
            modal.hide();

            $("#"+idSelect).fadeOut(300).fadeIn(300).fadeOut(300).fadeIn(300).fadeOut(300).fadeIn(300);
        }
    });
}





const outgoingNewItemTemplate = (data) => {
    return `
    <a id="${data.pid}" href="${data.url}" class="list-group-item list-group-item-action active" aria-current="true">
        <div class="d-flex w-100 justify-content-between">
            ${ data.time != null ? `<h5 class="mb-1">${data.date} ${data.time}</h5>`:`<h5>${data.date}</h5>`}
            ${ data.offset ? `<small><span class="badge text-bg-warning" data-bs-toggle="tooltip" data-bs-placement="bottom" data-bs-title="Offset">${data.currency}${data.amount}</span></small>`:`<small>${data.currency}${data.amount}</small>`}
        </div>
        <div class="row">
            <div class="col text-truncate">${data.label}</div>
        </div>
        <small><span class="badge text-bg-secondary me-1">${ data.category }</span><span class="badge text-bg-info">${ data.form }</span></small>
    </a>
    `
}