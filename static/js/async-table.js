// The function updateTable() must be defined
updateTable();

$("#myMod").on("show.bs.modal", function(e) {
    var link = $(e.relatedTarget);
    $(this).find(".modal-body").load(link.attr("href"));
});

function getFilterType() {
   filter = $("#filter-select option:selected").val();
}

function getAjaxUrl(filterType) {
    return window.location.href + "get_entries/" + ens + '/' + filterType;
}

function setTypeahead() {
    $('#filter').typeahead('destroy');
    $('#filter').typeahead({
     ajax: getAjaxUrl(filter),
     items: 14,
     onSelect: function (suggestion) {
            data1 = suggestion.text;
            updateTable();
        },
     matcher: function (suggestion) {
            return true;
        }
    });
}

setTypeahead();

$("#filter-date-1").datetimepicker({
    defaultDate: moment(),
    format: 'DD/MM/YYYY',
    locale: 'fr',
    sideBySide: false,
    allowInputToggle: true
});

$("#filter-date-2").datetimepicker({
    defaultDate: moment(),
    format: 'DD/MM/YYYY',
    locale: 'fr',
    sideBySide: false,
    allowInputToggle: true,
    useCurrent: false
});

$("#filter-date-1").on("dp.change", function (e) {
    var data1 = $(this).val();
    // $("#filter-date-2").data("DateTimePicker").date(data1 + ' 12:23:12');
    $("#filter-date-2").data("DateTimePicker").minDate(e.date);
});

$("#filter-date-2").on("dp.change", function (e) {
    $("#filter-date-1").data("DateTimePicker").maxDate(e.date);
    data2 = $(this).val();
});

$('#filter-date').hide();

$('#filter-select').change(function () {
    data1 = '';
    getFilterType();
    active = 0;
    // Format date input
    if ($(this).val().startsWith('datetime_')) {
        $("#filter-date-1").data('DateTimePicker').format('DD/MM/YYYY');
        $("#filter-date-2").data('DateTimePicker').format('DD/MM/YYYY');
    } else if ($(this).val().startsWith('date_')) {
        $("#filter-date-1").data('DateTimePicker').format('MM/YYYY');
        $("#filter-date-2").data('DateTimePicker').format('MM/YYYY');
    }

    if (filter.startsWith("date")) {
        $('#filter-text').hide();
        $('#filter-date').show();
    } else {
        $('#filter-date').hide();
        $('#filter-text').show();
        setTypeahead();
    }
});

function changeModelHeader(title) {
    $(".modal-header h4").text(title);
}

function filterRow() {
    filter = $('#filter-select option:selected').val();
    if (filter.startsWith('date')) {
        data1 = $("#filter-date-1").val();
        data2 = $("#filter-date-2").val();
    } else {
        data1 = $("#filter").val();
    }

    updateTable();
};

$('#filter').keypress(function(e){
  if(e.keyCode==13) {
    filterRow();
  }
});

$("#myMod").on("hidden.bs.modal", function(e) {
    $(".modal-body").empty();
});
