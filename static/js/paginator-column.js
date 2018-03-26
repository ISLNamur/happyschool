$(".rpp [value='" + rpp + "']").prop('selected', true);
$(".ens [value='" + ens + "']").prop('selected', true);

$(".rpp").change(function() {
    rpp = $(this).val();
    updateTable();
});

$(".ens").change(function() {
    ens = $(this).val();
    updateTable();
    setTypeahead();
});

function genSortIcon(column) {
    icon = '<i class="glyphicon glyphicon-sort-by-';
    if (column.startsWith('datetime') || column == 'classe') {
        icon += 'order';
    } else {
        icon += 'alphabet';
    }

    if (order == 'asc')
        icon += '-alt';

    icon += '">';
    return icon;
}

$("#column-" + sortBy).append(genSortIcon(sortBy));

function changeSort(column) {
        if (column == sortBy) {
            order = order == 'asc' ? 'desc' : 'asc';
        } else {
            sortBy = column;
        }
        updateTable();
}

function changePage(pageNumb) {
    page = pageNumb;
    updateTable();
}
