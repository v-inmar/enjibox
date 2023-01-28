$(()=>{
    homePopulateAnchors();
    homeGetSummary();
});

const homePopulateAnchors = () => {
    const dateToday = new Date();
    const outgoingLinkPrefix = $(".home-summary-link-today").attr("href");
    const pageNumber=1
    // Get Today's Date
    const dateTodayISONoTime = dateToday.toISOString().split("T")[0];
    $(".home-summary-link-today").attr("href",outgoingLinkPrefix+"?label=&date_from="+dateTodayISONoTime+"&date_to="+dateTodayISONoTime+"&category=&form=&page="+pageNumber);


    // Get Dates for Week start and Week end
    // Days starts with 0 - Sunday
    epochWeekBegin = new Date().setDate(dateToday.getDate() - dateToday.getDay()) // Gets the epoch time for start of the week base on today's date
    epochWeekEnd = new Date().setDate(dateToday.getDate() + (6 - dateToday.getDay())); // Gets the epoch time for end the week based on today's date
    const dateThisWeekStartISONoTime = new Date(epochWeekBegin).toISOString().split("T")[0];
    const dateThisWeekEndISONoTime = new Date(epochWeekEnd).toISOString().split("T")[0];
    $(".home-summary-link-this-week").attr("href",outgoingLinkPrefix+"?label=&date_from="+dateThisWeekStartISONoTime+"&date_to="+dateThisWeekEndISONoTime+"&category=&form=&page="+pageNumber);

    // Get Dates for the month start and month end
    const dateThisMonthStartISONoTime = new Date(dateToday.getFullYear(), dateToday.getMonth(), 1).toISOString().split("T")[0];
    const dateThisMonthEndISONoTime = new Date(dateToday.getFullYear(), dateToday.getMonth()+1, 0).toISOString().split("T")[0];
    $(".home-summary-link-this-month").attr("href",outgoingLinkPrefix+"?label=&date_from="+dateThisMonthStartISONoTime+"&date_to="+dateThisMonthEndISONoTime+"&category=&form=&page="+pageNumber);

    // Get Dates for the year start and year end
    const dateThisYearStartISONoTime = new Date(dateToday.getFullYear(), 0, 1).toISOString().split("T")[0];
    const dateThisYearEndISONoTime = new Date(dateToday.getFullYear(), 11, 31).toISOString().split("T")[0];
    $(".home-summary-link-this-year").attr("href",outgoingLinkPrefix+"?label=&date_from="+dateThisYearStartISONoTime+"&date_to="+dateThisYearEndISONoTime+"&category=&form=&page="+pageNumber);

}

const homeGetSummary = () => {
    const csrf = $(".home-container").data("csrf");
    var url = $(".home-container").data("url")
    const date = new Date();

    var monthNumber = date.getMonth()+1 // note +1 since it starts with zero
    var dayNumber = date.getDate()

    if(String(monthNumber).length < 2){
        monthNumber = "0"+String(monthNumber)
    }

    if(String(dayNumber).length < 2){
        dayNumber = "0"+String(dayNumber);
    }

    url += "?year="+date.getFullYear()+"&month="+monthNumber+"&day="+dayNumber;
    utilityAjaxGet(
        token=csrf,
        url=url,
        contentType="application/json",
        successCallback=homeGetSummarySuccessCallback,
        errorCallback = homeGetSummaryErrorCallback
    )
}

const homeGetSummarySuccessCallback = data => {
    
    let payload = data.payload;
    let currency = payload.currency;

    // Amount
    let amountJSON = payload.amount;

    homeGetMakePage(amountJSON.today, currency, "today");

    homeGetMakePage(amountJSON.this_week, currency, "this-week");


    homeGetMakePage(amountJSON.this_month, currency, "this-month");

    
    homeGetMakePage(amountJSON.this_year, currency, "this-year");


    $(".home-loading").css("display", "none");
    $(".home-main").css("display", "block");
    
    utilityMakeHeightTheSame(".home-summary-category-li");
    utilityMakeHeightTheSame(".home-summary-form-li");

    


}

const homeGetSummaryErrorCallback = (jqXHR, textStatus, errorThrown) => {
    console.log(jqXHR);
}

const homeGetMakePage = (amountJSON, currency, sig) => {
    // let amountThisYear = amountJSON.this_year;
    $(".home-summary-amount-"+sig).text(`${currency}${amountJSON.total}`);
    $(".home-summary-items-"+sig).text(`${amountJSON.items} item(s)`);
    let categoryJSON = amountJSON.category;
    let htCategory = categoryJSON.highest_total;
    let muCategory = categoryJSON.most_used;
    homeGetSummaryMakeCategoryAndForm(htCategory, ".home-summary-category-"+sig+"-highest-total", currency);
    homeGetSummaryMakeCategoryAndForm(muCategory, ".home-summary-category-"+sig+"-most-used", false);
    let formJSON = amountJSON.form;
    let htForm = formJSON.highest_total;
    let muForm = formJSON.most_used;
    homeGetSummaryMakeCategoryAndForm(htForm, ".home-summary-form-"+sig+"-highest-total", currency);
    homeGetSummaryMakeCategoryAndForm(muForm, ".home-summary-form-"+sig+"-most-used", false);
}


const homeGetSummaryMakeCategoryAndForm = (theList, elemSelector, currency) => {
    if(theList.length > 0){
        for(let i = 0; i < theList.length; i++){
            
            if(currency){
                $(elemSelector).append(
                    `
                    <div class="home-li-div">
                        <span>${theList[i][0]}</span>
                        
                        <span>${currency}${theList[i][1]}</span>
                    </div>
                    `
                );
            }else{
                $(elemSelector).append(
                    `
                    <div class="home-li-div">
                        <span>${theList[i][0]}</span>
                        
                        <span>Used ${theList[i][1]} time(s)</span>
                    </div>
                    `
                );
            }
            
        }
        
    }else{
        $(elemSelector).append(
            `
            <div class="home-li-div-no-item">
                <span>No Items</span>
            </div>
            `
        );
    }
}